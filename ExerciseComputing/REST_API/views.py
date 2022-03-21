from rest_framework.views import APIView
from .computing import CodeComputing
from .permissions import TokenVerify


class ExerciseView(APIView):
    permission_classes = [TokenVerify] 

    def post(self, *args, **kwargs):
        print(self.request.data)
        computing = CodeComputing(header_token=self.request.META.get('HTTP_AUTHORIZATION', None), data=self.request.data)
        return computing.execute_computing()
            

                
                

