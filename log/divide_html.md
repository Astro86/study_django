# HTML 분리해서 관리하기

> blog/templates/blog/base.html 추가

```html
<div class="container">
    <div class="row">
        <!-- Blog Entries Column -->
        <div class="col-md-8">
            {% block content %}
            {% endblock %}
        </div>
```


> blog/templates/blog/post_list 수정

```html
{% extends 'blog/base.html' %}
{% block content %}
<!-- Blog Post -->
{%if object_list.exists %}
<!-- 포스트의 모든 게시물들을 하나씩 가져온다. -->
{% for p in object_list %}
<div class="card mb-4">
  <!-- <img
              class="card-img-top"
              src="http://placehold.it/750x300"
              alt="Card image cap"
            /> -->

  {% if p.head_image %}
  <img class="card-img-top" src="{{p.head_image.url}}" alt="Card image cap" />
  {% else %}
  <img class="card-img-top" src="https://picsum.photos/seed/picsum/750/300" alt="Card image cap" />
  {% endif %}

  <div class="card-body">
    <!-- 제목 -->
    <h2 class="card-title">{{p.title}}</h2>
    <!-- 내용 -->
    <p class="card-text">
      {{p.content | truncatewords:50}}
    </p>
    <a href="#" class="btn btn-primary">Read More &rarr;</a>
  </div>
  <!-- 작성일과 작성자 -->
  <div class="card-footer text-muted">
    Posted on {{p.created}} by
    <a href="#">{{p.author}}</a>
  </div>
</div>
{%endfor%}
{%else%}
<h3>아직 게시물이 없습니다.</h3>
{%endif%}
{% endblock %}
```

extends와 block을 이용하여 중복되는 템플릿을 삭제한 후 간단하게 만들어 주었다.


> blog/templates/blog/post_detail.html

```django
{% extends 'blog/base.html' %}
{% block content %}
<h1>{{object.title}}</h1>
<div>
  {{object.content}}
</div>
{% endblock %}
```

### 결과
```shell
AssertionError: ' ' != 'Blog'
-  
+ Blog


----------------------------------------------------------------------
Ran 2 tests in 0.031s

FAILED (failures=2)
Destroying test database for alias 'default'...
```
테스트시 오류가 뜬다. 타이틀이 제대로 반영이 안됐기 때문이다.

## title도 제대로 반영이 될 수 있도록 수정하기

> blog/templates/blog/base.html

```django
<head>
    <meta charset="UTF-8" />
    <!-- title이 없는 경우는 Blog를 내보내고 있는 경우는 그것으로 대체한다. -->
    <title>{% block title %}Blog{% endblock %}</title>
```

> blog/templates/blog/post_detail.html

```django
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}
<h1>{{object.title}}</h1>
<div>
  {{object.content}}
</div>
{% endblock %}
```