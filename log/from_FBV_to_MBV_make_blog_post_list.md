# FBV -> MBV : 블로그 포스트 리스트

> blog/view.py

> 변경전

```python
from django.shortcuts import render
from .models import Post

def index(request):
    # Post의 내용들을 전부 다 가져온다.
    posts = Post.objects.all()

    return render(
        request,
        # 템블릿이 되는 html 코드를 작성할 필요가 있다.
        'blog/index.html',
        # index.html에서 사용하도록 객체를 넘겨주고 있다.
        # template에 전해주고 싶은 것들을 적어주면 된다.
        {
            'posts': posts,
        }
    )
```

> 변경후

```python
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView


# Create your views here.


class PostList(ListView):
    model = Post
```

> blog/urls.py

```python
urlpatterns = [
    path('', views.index),
]
```

```python
urlpatterns = [
    path('', views.PostList.as_view()),
]
```

> blog/templates/blog/post_list.html 생성

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
    {% for p in object_list %}
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

## 역순으로 보이게 하기

```django
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView


# Create your views here.


# List로 보여줄 때는 django.views.generic의
# ListView를 상속하여 보여주면 간단하게 보여줄 수 있다.
class PostList(ListView):
    model = Post

    def get_queryset(self):
        # 역순으로 보여주기 위해 -로 붙인다.
        return Post.objects.order_by('-created')
```