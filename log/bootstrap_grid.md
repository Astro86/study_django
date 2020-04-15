# Bootstrap Grid

## container

> blog/templates/blog/post_list.html

```django
<div class="container">
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
</div>
```

## 메인 페이지 디자인 변경하기

> https://startbootstrap.com/templates/blog/

```html
<!-- Page Content -->
<div class="container">
  ...
</div>
<!-- /.row -->
```

bootstrap으로부터 페이지 container 변경을 위해 코드를 가져온다.

## 가져온 페이지 디자인에 콘텐츠 넣어주기

```django
<!-- Blog Entries Column -->
<div class="col-md-8">
  <h1 class="my-4">
    Blog
  </h1>

  <!-- Blog Post -->
  <!-- 포스트의 모든 게시물들을 하나씩 가져온다. -->
  {% for p in object_list %}
  <div class="card mb-4">
    <img
      class="card-img-top"
      src="http://placehold.it/750x300"
      alt="Card image cap"
    />
    <div class="card-body">
      <!-- 제목 -->
      <h2 class="card-title">{{p.title}}</h2>
      <!-- 내용 -->
      <p class="card-text">
        {{p.content}}
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
</div>
```
