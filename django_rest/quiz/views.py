from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Quiz
from .serializers import QuizSerializer
import random

# Create your views here.

@api_view(['GET'])
def HelloAPI(request):
    return Response("Hello World!");


@api_view(['GET'])
def randomQuiz(request, id):
    totalQuizs = Quiz.objects.all()
    randomQuizs = random.sample(list(totalQuizs), id)
    # many=True은 다량의 데이터에 대해서도 직렬화를 진행한다.
    serializer = QuizSerializer(randomQuizs, many=True)
    return Response(serializer.data)