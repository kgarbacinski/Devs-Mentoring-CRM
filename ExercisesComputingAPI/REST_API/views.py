from rest_framework.generics import ListAPIView
from .models import ExerciseTest
from .permissions import TokenVerify
from .serializers import ExerciseTestSerializer


class ExerciseView(ListAPIView):
    permission_classes = [TokenVerify]
    serializer_class = ExerciseTestSerializer
    
    def get_queryset(self):
        language = self.request.GET.get('language')
        slug_name = self.request.GET.get('name')
        return ExerciseTest.objects.filter(exercise__language__name=language).filter(exercise__slug=slug_name)
        



        
