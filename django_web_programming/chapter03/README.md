# 03장 Django 웹 프레임워크

```shell
ch3
├── db.sqlite3
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── settings.cpython-36.pyc
│   │   ├── urls.cpython-36.pyc
│   │   └── wsgi.cpython-36.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── polls
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   ├── admin.cpython-36.pyc
    │   ├── apps.cpython-36.pyc
    │   ├── models.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── views.cpython-36.pyc
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── __init__.py
    │   └── __pycache__
    │       ├── 0001_initial.cpython-36.pyc
    │       └── __init__.cpython-36.pyc
    ├── models.py
    ├── templates
    │   └── polls
    │       ├── detail.html
    │       ├── index.html
    │       └── results.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## 장고 프로젝트 생성하기

```python
django-admin startproject mysite
```

`django-admin`명령어와 `startproject`옵션을 이용하여 새로운 프로젝트를 생성한다.

> django-admin startproject <프로젝트 이름>

### 결과
```shell
mysite
├── manage.py
└── mysite
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 6 files
```

하위 `mysite`는 프로젝트 디렉토리이고, 상위 `mysite`디렉토리는 프로젝트 관련 디렉토리/파일을 모으는 역할만 하는 디렉토리이다. 따라서 아무런 의미가 없으므로 이름을 변경해도 무방하다.

## 어플리케이션 생성

```shell
python manage.py startapp polls
```

`manage.py`파는 파일과 `startapp`옵션을 이용하여 polls라는 애플리케이션을 만든다.

> python manage.py startapp <애플리케이션 이름>

### 결과

```shell
polls
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-36.pyc
│   ├── admin.cpython-36.pyc
│   ├── apps.cpython-36.pyc
│   ├── models.cpython-36.pyc
│   ├── urls.cpython-36.pyc
│   └── views.cpython-36.pyc
├── admin.py
├── apps.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
│   └── __pycache__
│       ├── 0001_initial.cpython-36.pyc
│       └── __init__.cpython-36.pyc
├── models.py
├── templates
│   └── polls
│       ├── detail.html
│       ├── index.html
│       └── results.html
├── tests.py
├── urls.py
└── views.py

5 directories, 20 files
```

## 프로젝트 설정 파일 변경

> settings.py

### 1. ALLOWD_HOSTS 항목

```python
DEBUG = True

ALLOWED_HOSTS = ['192.168.56.101', 'localhost', '127.0.0.1']	# shkim
```

`DEBUG`옵션이 True일 경우 개발모드로, False경우 운영모드로 인식한다.

### 2. 프로젝트에 포함되는 애플리케이션들을 모두 설정 파일에 등록

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',		# shkim
]
```

방금 생성한 polls 애플리케이션도 등록해야 한다. 어플리케이션을 등록할 때는 간단하게 애플리케이션의 모듈명인 polls만 등록해도 되지만, `애플리케이션 설정 클래스`로 등록하는 것이 더 정확한 방법이다.

### 3. 데이터 베이스 엔진

```python
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 4. 타임존 지정

```python
#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul
```

## 기본 테이블 생성

```python
python manage.py migrate
```

`migrate`명령은 데이터베이스에 변경사항이 있을 때 이를 반영해주는 명령입니다.

## 장고 실행하기

```python
python manage.py runserver
```

## Admin

### Admin사이트 접속하기

```http
http://127.0.0.1:8000/admin
```

### Admin사이트에 접속하기 위한 관리자 만들기

```shell
python manage.py cretesuperuser
```

`createsuperuser`명령어를 이용하여 관리자를 생성한다.

## 테이블 정의

```python
from django.db import models

# models.Model클래스를 상속받아서 클래스를 생성한다.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # 객체를 문자열로 표현할 때 사용하는 함수
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

Question과 Choice 두개의 테이블을 생성하였다.  
장고는 테이블을 하나의 클래스로 정의하고, 테이블의 column은 클래스의 변수로 매핑한다. 테이블 클래스는 `django.db.models.Model`클래스를 상속받아 정의하고, 각 클래스 변수 타입도 장고에서 미리 정의된 필드 클래스를 사용한다.

### Question 테이블 컬럼과 변수 간의 매핑

| 테이블 column이름 | column 타입  | 장고의 클래스 변수 | 장고의 필드 클래스                     |
| :---------------- | ------------ | ------------------ | -------------------------------------- |
|                   |              |                    |                                        |
| id                | integer      | (id)               | (PK는 장고에서 자동으로 생성해준다.)   |
| question_text     | varchar(200) | question_text      | models.CharField(max_length=200)       |
| pub_date          | datetime     | pub_date           | modles.DateTimeField('date published') |

### Choice 테이블 컬럼과 클래스 변수 간의 매핑

| 테이블 column이름 | column 타입  | 장고의 클래스 변수 | 장고의 필드 클래스                   |
| :---------------- | ------------ | ------------------ | ------------------------------------ |
|                   |              |                    |                                      |
| id                | integer      | (id)               | (PK는 장고에서 자동으로 생성해준다.) |
| choice_text       | varchar(200) | choice_text        | models.CharField(max_length=200)     |
| votes             | integer      | votes              | modles.DateTimeField(default=0)      |
| question_id       | integer      | question           | models.ForeighKey(Question)          |

## Admin 사이트에 테이블 반영

> admin.py

```python
from django.contrib import admin
from polls.models import Question, Choice


admin.site.register(Question)
admin.site.register(Choice)
```

`models.py` 모듈에서 정의한 Question, Choice 클래스를 임포트 하고, `admin.site.register()`함수를 이용하여 임포트한 클래스를 Admin 사이트에 등록해준다.

## 테이터베이스 변경사항 반영

```shell
python manage.py makemigrations
python manage.py migrate
```

migration이란 용어는 테이블 및 필드의 생성, 삭제, 변경 등과 같이 데이터베이스에 대한 변경 사항을 알려주는 정보이다.  
물리적으로는 애플리케이션 디렉토리별로 마이크레이션 파일이 존재한다.  
`makemigartions`명령에 의해 마이그레이션 파일들이 생기고, 이 마이그레이션 파일들을 이용해 `migrate`명령으로 데이터 베이스 테이블을 만들어준다.

# 애플리케이션 개발하기 - Veiw 및 Template 코딩

> URLconf설계 - URL과 뷰 매핑

| URL 패턴         | 뷰 이름     | 뷰가 처리하느 내용                              |
| ---------------- | ----------- | ----------------------------------------------- |
| /polls/          | index()     | index.html 템플릿을 보여준다.                   |
| /polls/5/        | detail()    | detail.html 템플릿을 보여준다.                  |
| /polls/5/vote/   | vote()      | detail.html에 있는 폼을 POST 방식으로 처리한다. |
| /polls/5/results | results()   | results.html 템플릿을 보여준다.                 |
| /admin/          | (장고 기능) | Admin 사이트를 보여준다.                        |

## URLconf 코딩

> polls/url.py

```python
from django.urls import path
from polls import views


app_name = 'polls'
urlpatterns = [
    # /polls/로 들어오는 경우 view.index(request)처럼 뷰 함수가 호출 된다.
    # 이 URL 패턴의 이름을 index라고 정한다.
    path('', views.index, name='index'),      # /polls/

    # /polls/5/로 들어오는 경우 아래 라인과 매칭이 된다.
    # view.detail(request, question_id=5)처럼 인자가 대입된다.
    # 이 URL 패턴의 이름을 detail이라고 정한다.
    path('<int:question_id>/', views.detail, name='detail'),

    # /polls/5/results/으로 들어올 경우 아래 라인과 매칭된다.
    # 5는 추출되어 int타입으로 변환된 후
    # 뷰 함수 호출 시 views.results(request, quesiton_id=5)처럼 인자가 대입된다
    # 이 URL 패턴의 이름은 result
    path('<int:question_id>/results/', views.results, name='results'),

     # /polls/5/vote/으로 들어올 경우 아래 라인과 매칭이되고,
     # 5는 추출되어 int로 변환된 뒤에 views.vote(request, qeustion_id=5)로 인자가 대입된다.
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

> mysite/url.py

```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # shkim
    path('polls/', include('polls.urls')),
]
```

### ROOT_URLCONF

mysite/settings.py 파일에 ROOT_URLCONF항목이 정의 된다. 이는 장고가 URL 분석시, 이 항목이 정의된 urls.py 파일을 가장 먼저 분석하기 사작한다는 의미이다.

## 뷰 함수 index() 및 템플릿 작성

> polls/index.html

```django
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

### index() 함수 작성

> polls/views.py

```python
from django.shortcuts import get_object_or_404, render
from polls.models import Choice, Question

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```


## 뷰 함수 detail() 및 폼 템플릿 작성
> polls/detail.html

### form 태그 추가
```django
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

### detail() 함수 작성
```python
from django.shortcuts import get_object_or_404, render
from polls.models import Choice, Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```


## 뷰 함수 vote() 및 리다이렉션 작성

### vote() 함수 작성

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from polls.models import Choice, Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

## 뷰 함수 result() 및 템플릿 작성

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from polls.models import Choice, Question

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```


## result.html 작성
```django
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

