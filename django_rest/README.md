# 장고를 이용한 rest api 만들기

## settings

> myapi/settings.py

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

정적 파일 root 추가

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz',
    'rest_framework',
]
```

`INSTALLED_APPS`에 `quiz`와 `rest_framework`를 추가해준다.


## 모델 생성하기

> quiz/models.py

```python
from django.db import models

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    answer = models.IntegerField()
```

## 시리얼라이저 생성하기

> quiz/serializers.py

```python
from rest_framework import serializers
from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('title', 'body', 'answer')
```

시리얼라이저는 장고의 model데이터를 JSON형태로 만들어주는 코드이다. api통신이 가능하게 해준다.

## 반환 값 설정하기

> quize/views.py

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Quiz
from .serializers import QuizSerializer

# Create your views here.

@api_view(['GET'])
def HelloAPI(request):
    return Response("Hello World!");
```

## url 설정하기

> quiz/urls.py

```python
from django.urls import path, include
from .views import HelloAPI

urlpatterns = [
    path("hello/", HelloAPI),

]
```

> myapi/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
]
```

## 새로운 API 추가하기

> quiz/views.py

```python
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
```

## url에 추가하기

> quiz/urls.py

```python
from django.urls import path, include
from .views import HelloAPI, randomQuiz

urlpatterns = [
    path("hello/", HelloAPI),
    path("<int:id>/", randomQuiz),
]
```

## admin 페이지에 Quiz모델 추가하기

> quiz/admin.py

```python
from django.contrib import admin
from .models import Quiz

# Register your models here.

admin.site.register(Quiz)
```