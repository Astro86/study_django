# MTV 구조 맛보기 : model, views, templates 사용하기

> mysite/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

> blog/url.py 추가

```python
from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.index),
]
```

> blog/views.py

```python
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(
        request,
        # 템블릿이 되는 html 코드를 작성할 필요가 있다.
        'blog/index.html'
    )
```

> blog/templates/blog/index.html

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>Blog</title>
  </head>
  <body>
    <h1>Blog</h1>
  </body>
</html>
```

> blog/views.py

```python
from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    # Post의 내용들을 전부 다 가져온다.
    posts = Post.objects.all()

    return render(
        request,
        # 템블릿이 되는 html 코드를 작성할 필요가 있다.
        'blog/index.html',
        {
            'posts': posts,
        }
    )
```

> blog/templates/blog

```django
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>Blog</title>
  </head>
  <body>
    <h1>Blog</h1>
    <!-- 포스트의 모든 게시물들을 하나씩 가져온다. -->
    {% for p in posts %}
    <!-- 제목 -->
    <h3>{{p.title}}</h3>
    <!-- 작성일과 작성자 -->
    <h4>{{p.created}} by {{p.author}}</h4>
    <!-- 내용 -->
    <p>{{p.content}}</p>
    {%endfor%}
  </body>
</html>
```
