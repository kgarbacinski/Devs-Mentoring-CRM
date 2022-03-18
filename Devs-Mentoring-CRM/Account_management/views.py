from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.template.response import TemplateResponse

from Files_organizer.models import SubTopic, Subject
from .forms import LoginForm, ResetRequestForm, PaymentForm
from .models import Student, Mentor, PaymentInfo
from Meetings_calendar.models import Meeting
from payments import RedirectNeeded, get_payment_model


class LoginView(PasswordResetView):
    template_name = 'Account_management/login.html'

    def authenticate_user(self, user):
        user = user.save(commit=False)
        user = User.objects.get(email=user.email)
        login(request=self.request, user=user)
        next_page = self.request.GET.get("next", None)
        if next_page:
            return redirect(next_page)
        return redirect('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return render(request, self.template_name, {'login_form': LoginForm(), "reset_form": ResetRequestForm()})

    def post(self, request, *args, **kwargs):
        if 'sing_in' in request.POST:
            user = LoginForm(request.POST)
            if user.is_valid():
                return self.authenticate_user(user)

        elif 'send_reset' in request.POST:
            reset_form = ResetRequestForm(request.POST)

            if reset_form.is_valid():
                opts = {
                    'use_https': self.request.is_secure(),
                    'token_generator': self.token_generator,
                    'from_email': self.from_email,
                    'email_template_name': self.email_template_name,
                    'subject_template_name': self.subject_template_name,
                    'request': self.request,
                    'html_email_template_name': self.html_email_template_name,
                    'extra_email_context': self.extra_email_context,
                }
                reset_form.save(**opts)

        return render(request, self.template_name,
                      {'login_form': LoginForm(request.POST), "reset_form": ResetRequestForm(request.POST)})


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'Account_management/index.html'
    context_object_name = 'students'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Mentor.objects.filter(student__user__username=user)
        return Student.objects.filter(mentor__user__username=user)


class MentorsSummaryView(LoginRequiredMixin, View):
    template_name = 'Account_management/student-summary.html'
    model = Meeting

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='Moderator').exists():
            template_name = 'Account_management/mentors-summary.html'
            return render(request, template_name, context={'is_moderator': True})
        elif user.groups.filter(name='Mentor').exists():
            return render(request, self.template_name)
        return redirect('index')


class MaterialsSummaryView(LoginRequiredMixin, ListView):
    template_name = 'Account_management/materials-summary.html'
    context_object_name = 'students'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='Moderator').exists():
            return super().get(request, *args, **kwargs)
        return redirect('index')

    def get_queryset(self):
        return Student.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['subtopics'] = SubTopic.objects.all()
        return context


class PaymentView(LoginRequiredMixin, View):
    template_name = 'Account_management/payment.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Mentor').exists():
            return render(request, self.template_name, {'form': PaymentForm()})
        try:
            payment_data = PaymentInfo.objects.get(student=Student.objects.get(user=request.user.id))
            form = PaymentForm(instance=payment_data)
            return render(request, self.template_name, {'form': form})
        except PaymentInfo.DoesNotExist:
            return render(request, self.template_name,
                          {'form': PaymentForm(initial=
                                               {'firstName': request.user.first_name,
                                                'lastName': request.user.last_name,
                                                'email': request.user.email})})

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST)
        form.instance.user = request.user.id
        user = request.user
        if form.is_valid():
            if self.request.user.groups.filter(name='Student').exists():
                PaymentInfo.objects.update_or_create(
                    student=Student.objects.get(user=request.user.id),
                    defaults={'firstName': form.cleaned_data.get('firstName'),
                              'lastName': form.cleaned_data.get('lastName'),
                              'companyName': form.cleaned_data.get('companyName', ''),
                              'nip': form.cleaned_data.get('nip', ''),
                              'street': form.cleaned_data.get('street'),
                              'postCode': form.cleaned_data.get('postCode'),
                              'town': form.cleaned_data.get('town'),
                              'country': form.cleaned_data.get('country'),
                              'phone': form.cleaned_data.get('phone'),
                              'email': form.cleaned_data.get('email'),
                              'comment': form.cleaned_data.get('comment', '')}
                )
            Payment = get_payment_model()
            payment = Payment.objects.create(
                variant="przelewy24",  # this is the variant from PAYMENT_VARIANTS
                description=user.student.path.name,
                total=Decimal(user.student.path.price),
                # total=Decimal(0.1),
                # tax=Decimal(20),
                currency="PLN",
                # delivery=Decimal(10),
                billing_first_name=form.cleaned_data.get('firstName'),
                billing_last_name=form.cleaned_data.get('lastName'),
                billing_address_1=form.cleaned_data.get('street'),
                # billing_address_2="",
                billing_city=form.cleaned_data.get('town'),
                billing_postcode=form.cleaned_data.get('postCode'),
                billing_country_code="PL",
                billing_country_area=form.cleaned_data.get('country'),
                customer_ip_address="127.0.0.1",
                billing_email=form.cleaned_data.get('email'),
                # success_url='Account_management/index.html'
            )
            return redirect(f"/payment_details/{payment.pk}")
        return render(request, self.template_name, {'form': PaymentForm()})


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, "Account_management/confirm-payment.html", {"form": form, "payment": payment})


class SuccessPaymentView(LoginRequiredMixin, View):
    template_name = 'Account_management/success-payment.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class FailurePaymentView(LoginRequiredMixin, View):
    template_name = 'Account_management/failure-payment.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
