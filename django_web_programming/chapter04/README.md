# 04장 Django의 핵심 기능

```shell
.
├── db.sqlite3
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── polls
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── polls
│   │       ├── detail.html
│   │       ├── index.html
│   │       └── results.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── templates
    └── admin
        └── base_site.html
```

## Admin 사이트 꾸미기

### 모델 클래스와 Admin UI 간 위젯 매핑
```python
from django.contrib import admin
from polls.models import Question, Choice

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
```

### 필드 순서 변경하기

#### QuestionAdmin 클래스 정의

> admin.py

```python
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
```

### 필드 분리해서 보여주기

> polls/admin.py

```python
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('Question Statement', {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
```

### 필드 접기

> polls/admin.py

```python
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('Question Statement', {'fields': ['question_text']}),
        #('Date Information', {'fields': ['pub_date']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
```


### Question 및 Choice를 한 화면에서 변경하기

> polls/admin.py

```python
from django.contrib import admin
from polls.models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('Question Statement', {'fields': ['question_text']}),
        #('Date Information', {'fields': ['pub_date']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
```

### 테이블 형식으로 보여주기

> polls/admin.py

```python
#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
```

### 레코드 리스트 컬럼 지정하기
> polls/admin.py

```python
inlines = [ChoiceInline]
list_display = ('question_text', 'pub_date')
```

### list_filter 필터

> polls/admin.py

```python
inlines = [ChoiceInline]
list_display = ('question_text', 'pub_date')
list_filter = ['pub_date']
```


### search_fields

> polls/admin.py

```python
inlines = [ChoiceInline]
list_display = ('question_text', 'pub_date')
list_filter = ['pub_date']
search_fields = ['question_text']
```

### polls/admin.py 변경 내역 정리

```python
from django.contrib import admin
from polls.models import Question, Choice


#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('Question Statement', {'fields': ['question_text']}),
        #('Date Information', {'fields': ['pub_date']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
```

### Admin 사이트 템플릿 수정

> template/admin/base_site.html

```django
{% extends "admin/base.html" %}

{% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">SHK Polls Administration</a></h1>
{% endblock %}

{% block nav-global %}{% endblock %}
```

> settings.py

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
```


## 장고 파이썬 쉘로 데이터 조작하기
```python
python manage.py shell
```

### Create - 데이터 생성/입력
```python
from polls.models import Question, Choice
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
```

### Read - 데이터 조회
```python
Question.objects.all()
```

```django
<QuerySet [<Question: What is your hobby ?>, <Question: What do you like best ?>, <Question: Where do you live ?>, <Question: What's new ?>, <Question: What's new?>]>
```

```python
from datetime import date
from datetime import datetime

Question.objects.filter(
    question_text__startswith='What'
).exclude(
    pub_date__gte=date.today()
).filter(
    pub_date__gte=datetime(2005, 1, 30)
)
```

#### 결과
```django
 <QuerySet [<Question: What is your hobby ?>, <Question: What do you like best ?>, <Question: What's new ?>]>
```

```python
one_entry=Question.objects.get(pk=1)
```

### Update - 데이터 수정
```python
q.question_text = "What is your favorite hobby ?"
q.save()
```

#### 여러 개의 객체를 한꺼번에 수정
```python
Question.objects.filter(pub_date__year=2007).update(question_text='Everything is the same')
```

### Delete - 데이터 삭제

```python
Question.objects.filter(pub_date__year=2005).delete()
```

#### Question 테이블의 모든 레코드를 삭제
```python
Question.objects.all().delete()
```

### polls 애플리케이션의 데이터 실습
```python
python manage.py shell

from polls.models import Question, Choice
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()

Question.objects.all()
Choice.objects.all()

q = Question(question_text="What's up?", pub_date=timezone.now())
q.save

q.id

q.question_text
q.pub_date

q.question_text = "What's new ?"
q.save()

Question.objects.all()
exit()
```


### polls 애플리케이션의 데이터 실습 2
```python
python manage.py shell

from polls.models import Question, Choice
Question.objects.filter(id=1)
Question.objects.filter(question_text__startwith='What')


from django.utils import timezone
current_year = timezone.now().year
Question.objects.filter(pub_date__year=current_year)

Question.objects.get(id=5)

Question.objects.get(pk=1)

q = Question.objects.get(pk=2)

q.choice_set.all()

q.choice_set.create(choice_text='Sleeping', votes=0)
q.choice_set.create(choice_text='Eating', votes=0)
c = q.choice_set.create(choice_text='Playing', votes=0)

c.question

q.choice_set.all()

q.choice_set.count()

Choice.objects.filter(question__pub_date__year=current_year)

c = q.choice_set.filter(choice_text__startswith='Sleeping')
c.delete()
```


## 템플릿 시스템

### 템플릿 변수
```django
<!--변수 사용하기-->
{{variable}}
```

### 템플릿 필터
필터란 어떤 객체나 처리 결과에 추가적으로 명령을 적용하여 해당 명령에 맞게 최종 결과를 변경한느 것
```django
{{name|lower}}
```

```django
{{text|escape|linebreaks}}
```

```django
{{bio|truncatewords:30}}
```

```django
{{list|join:" // "}
```

```django
{{value|length}}
```

```django
{{value|striptags}}
```

```django
{{value|pluralize}}
```

```django
{{value|pluralize:"es"}}
{{value|pluralize:"ies}}
```

```django
{{value|add:"2"}}
```

```django
{{first|add:second}}
```

## 템플릿 태그

### {% for %} 태그
```django
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

### {% if %} 태그

```django
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

### {% csrf_token %}태그
```django
<form action="." method="post">{% csrf_token %}
```

### {% url %}태그
```django
<form action="{% url 'polls:vote' question.id %} method='post'>
```
이 태그의 주 목적은 소스에 URL을 하드코딩하는 것을 방지하기 위한 것이다.

> {% url %} 태그를 사용하지 않을 경우

```html
<form action="/polls/3/vote" method="post">
```
이렇게 사용할 경우 /polls/라는 URL을 /blog/로 변경한는 경우 URLconf뿐만 아니라 모든 html을 찾아서 변경해줘야 하는 문제가 발생한다. 또한 /3/은 런타임에 따라 결정되어 항상 변하는 값이므로, 변수 처리를 해줘야 하기 때문에 불편하다.

> {% url 'namespace:view-name' arg1 arg2 %}

- namespace : urls.py 파일의 include()함수 또는 app_name 변수에 정의한 이름 공간이름
- view-name : urls.py 파일에서 정의한 URL 패턴 이름
- argN : 뷰 함수에서 사용하는 인자로, 없을수도 있고 여러개인 경우 빈칸으로 구분한다.

### {% with %}태그
```django
{% with total=business.employees.count %}
    {{ total }} people works at business
{% endwith %}
```

```django
{% with business.employees.count as total %}
    {{ total }} people works at business
{% endwith %}
```

### {% load %}태그
```djang
{% load somelibrary package.otherlibrary %}
```

### 템플릿 주석

#### {# #}

```django
{# greeting #}hello
```

#### {% comment %}

```django
{% comment "Optional note" %}
<p>Commented out text here</p>
{% endcomment %}
```

## HTML 이스케이프

#### {% autoescape off %}
자동 이스케이프를 방지

## 템플릿 상속

### 부모 템플릿

```django
<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="style.css" />
        <title>{% block title %}My amazing site{% endblock %}</title>
    </head>
    <body>
        <div id="sidebar">
            {% block sidebar %}
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
            {% endblock %}
        </div>

        <div id="content">
            {% block content %}{% endblock %}
        </div>
    </body>
</html>
```

### 자식 템플릿 - 템플릿 상속
```django
{% extends 'base.html' %}   

{% block title %}My amazing blog{% endblock  %}
{% block content %}
{% for entry in blog_endtries %}
    <h2>{{entry.title}}</h2>
    <p>{{entry.body}}</p>
{% endfor %}
{% endblock  %}
```

### 템플릿 상속 - 템플릿 처리 결과

```django
<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="style.css" />
        <title>My amazing site</title>
    </head>
    <body>
        <div id="sidebar">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
        </div>

        <div id="content">
            <h2>Entry one</h2>
            <p>This is my first entry.</p>

            <h2>Entry Two</h2>
            <p>This is my second entry.</p>
        </div>
    </body>
</html>
```

## 폼 처리하기

> url.py

```python
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path('about/', MyView.as_view())
]
```

### 클래스형 뷰 - MyView 정의

> view.py

```python
from django.http import httpResponse
from django.views.generic import View

class MyView(view):
    def gef(self, request):
        #뷰 로직 생성
        return HttpResonse('result')
```

## 클래스형 뷰의 장점 - 효율적인 메소드 구분

### 함수형 뷰로 HTTP GET 메소드 코딩

> views.py

```python
from django.http import HttpResponse

def my_view(request):
    if request.method == 'GET':
        # 뷰 로직 작성
        return HttpResponse('result')
```

### 클래스형 뷰로 HTTP GET 메소드 코딩

> views.py

```python
from django.http import HttpResponse
from django.views.generic import View

class MyView(View):
    def get(self, request):
        # 뷰 로직 작성
        return HttpResponse('result')
```

### 클래스형 뷰로 HTTP HEAD 메소드코딩

> view.py

```python
from django.http import HttpResponse
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    model = Book

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response
```

### 클래스형 뷰 작성 - TemplateView 상속

> some_app/urls.py

```python
from django.urls import path
from some_app.views import AboutView

urlpatterns = [
    path('about/', AboutView.as_view())
]
```

> some_app/views.py

```python
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

### 클래스 뷰 작성 - URLconf에 TemplateView 지정

> some_app/urls.py

```python
from django.urls import path
from django.view.generic import TemplateView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name="about.html")),
]
```

### 함수형 뷰로 폼을 처리
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm

def myview(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # cleaned_data로 관련 로직 처리
            return HttpResponseRedirect('/success/')
    else:
        form = MyForm(initial={'key':'value'})

    return render(request, 'form_template.html', {'form':form})
```


### 클래스형 뷰로 폼을 처리
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {'key':'value'}
    template_name = 'form_template.html'

    # 최초의 GET
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

    # 유효한 데이터를 가진 POST
    def POST(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # cleaned_data로 관련 로직 처리
            return HttpResponseRedirect('/success/')
        
        return render(request, self.template_name, {'form':form})
```


### FormView 제네릭 뷰로 폼을 처리

```python
from .froms import MyForm
from django.views.generic.edit import FormView

class MyFormView(FormView):
    form_class = MyForm
    template_name = 'form_template.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        # cleaned_data로 관련 로직 처리
        return super(MyFormView, self).form_valid(form)
```