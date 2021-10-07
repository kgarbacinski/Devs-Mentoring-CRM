"""Devs_Mentoring_CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.forms import SetPasswordForm
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
# from Account_management.forms import ResetPasswordForm
from Account_management.forms import ResetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar/', include('Meetings_calendar.urls')),
    path('', include('Account_management.urls')),
    path('exercises/', include('Exercises_checker.urls')),
    path('files/', include('Files_organizer.urls')),
    path('api/', include('Rest_API.urls')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('login'),
             template_name="Account_management/password_reset_confirm.html",
             form_class = ResetPasswordForm
         ), name='password_reset_confirm',

         ),

]