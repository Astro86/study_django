# Post 수정 화면 / 기능 구현하기

## 


## update된 url을 반환하는 함수 만들어 주기

> blog/models.py

```python
# update된 url을 반환하기 위한 함수
def get_update_url(self):
    return self.get_absolute_url() + 'update/'
```

## update된 url로 접속하기

> blog/views.py

```python
from django.views.generic import UpdateView

class PostUpdate(UpdateView):
    model = Post
    # post의 모든 field를 가져와라
    field = '__all__'
```

> blog/urls.py

```python
from django.urls import path, include
from .import views


urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.post_detail),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]
```

## post_form 추가하기

> blog/templates/blog/post_form.html

```django
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}
    {{ form }}
{% endblock %}
```

## update 페이지에 원하는 field만 가져오기

> blog/views.py

```python
class PostUpdate(UpdateView):
    model = Post
    # post의 모든 field를 가져와라
    # fields = '__all__'
    fields = [
        'title', 'content', 'head_image', 'category', 
        # 'tags'
    ]
```

## update 페이지 다듬어 주기

> blog/templates/blog/post_form.html

```django
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}
    <table>
    {{ form.as_table }}
    </table>
{% endblock %}
```

## 실시간으로 변경사항 볼 수 있게하기

> blog/templates/blog/post_form.html

```django
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}

    <form method="POST" action="">{% csrf_token %}
        <table>
            {{ form.as_table }}
        </table>

        <!-- submit 버튼-->
        <button type="submit" class="btn btn-primary float-right">submit</button>
    </form>
    {{ form.media }}
{% endblock %}
```

## Edit 버튼 활성화 하기

> blog/templates/blog/post_detail.html

```django
<button type="button" 
        class="btn btn-sm btn-secondary float-right" 
        onclick="location.href='{{ object.get_update_url }}'">EDIT</button>
```