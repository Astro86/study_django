# Post Detail 페이지 만들기

## 상세 페이지를 보여주기 위한 url을 추가한다.

> blog/urls.py

```python
from django.urls import path, include
from .import views


urlpatterns = [
    # path('', views.index),
    path('<int:pk>/', views.post_detail())
    path('', views.PostList.as_view()),
]
```

## 상세 페이지를 보여주기 위한 view를 위한 코드를 작성

> blog/views.py

```python
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


# 상세 페이지를 보여주기 위한 함수를 추가한다.
def post_detail(request, pk):
    blog_post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'blog_post': blog_post,
        }
    )
```

## 상세 페이지를 위한 html 코드 만들기

> blog/templates/blog/post_detail.html

```django
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>{{blog_post.title}}</title>
  </head>
  <body>
    <h1>{{blog_post.title}}</h1>
    <div>
        {{blog_post.content}}
    </div>
  </body>
</html>
```

## detail 함수를 클래스로 바꿔주기

> blog/views.py

```python
# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post': blog_post,
#         }
#     )

class PostDetail(DetailView):
    model = Post
```

## 클래스로 변경 후 url 수정하기

> blog/urls.py

```python
urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.post_detail),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]
```

## 클래스로 변경 후 html 수정하기

```django
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>{{object.title}}</title>
  </head>
  <body>
    <h1>{{object.title}}</h1>
    <div>
      {{object.content}}
    </div>
  </body>
</html>
```
