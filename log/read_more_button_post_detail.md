# read more 버튼 동작하게 하기, post_detail 페이지 개선하기

## 버튼 활성화 하기

### id 추가해주기

> blog/templates/blog/post_list.html

```html
<!-- 버튼이 눌렸을 때 이동할 url과 button을 쉽게 찾기 위한 id를 추가한다. -->
<a href="{{ p.get_absolute_url }}" class="btn btn-primary" id="read-more-post-{{ p.pk }}">Read More&rarr;</a>
```

### 테스트 코드부터 작성하기

> blog/tests.py

```python
# button 확인을 위한 코드
post_000_read_more_button = body.find('a', id="read-more-post-{}".format(post_000.pk))
self.assertEqual(post_000_read_more_button['href'], post_000.get_absolute_url())
```

## post_detail 디자인 변경하기

https://startbootstrap.com/previews/blog-post/

## 테스트 코드 작성하기

> blog/tests.py

```python
# post datail의 내용들이 잘 들어갔는지 확인하기 위한 코드
    body = soup.body
    main_div = body.find('div', id='main_div')
    self.assertIn(post_000.title, main_div.text)
    self.assertIn(post_000.author.username, main_div.text)
```

## 부트 스트랩으로 부터 가져오기

> blog/templates/post_detail.html

```django
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}
<!-- Title -->
<h1 class="mt-4">Post Title</h1>

<!-- Author -->
<p class="lead">
  by
  <a href="#">Start Bootstrap</a>
</p>

<hr>

<!-- Date/Time -->
<p>Posted on January 1, 2019 at 12:00 PM</p>

<hr>

<!-- Preview Image -->
<img class="img-fluid rounded" src="http://placehold.it/900x300" alt="">

<hr>

<!-- Post Content -->
<p class="lead">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ducimus, vero, obcaecati, aut, error quam
  sapiente nemo saepe quibusdam sit excepturi nam quia corporis eligendi eos magni recusandae laborum minus inventore?
</p>

<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ut, tenetur natus doloremque laborum quos iste ipsum rerum
  obcaecati impedit odit illo dolorum ab tempora nihil dicta earum fugiat. Temporibus, voluptatibus.</p>

<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eos, doloribus, dolorem iusto blanditiis unde eius illum
  consequuntur neque dicta incidunt ullam ea hic porro optio ratione repellat perspiciatis. Enim, iure!</p>

<blockquote class="blockquote">
  <p class="mb-0">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
  <footer class="blockquote-footer">Someone famous in
    <cite title="Source Title">Source Title</cite>
  </footer>
</blockquote>

<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error, nostrum, aliquid, animi, ut quas placeat totam sunt
  tempora commodi nihil ullam alias modi dicta saepe minima ab quo voluptatem obcaecati?</p>

<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum, dolor quis. Sunt, ut, explicabo, aliquam tenetur
  ratione tempore quidem voluptates cupiditate voluptas illo saepe quaerat numquam recusandae? Qui, necessitatibus, est!
</p>

<hr>

<!-- Comments Form -->
<div class="card my-4">
  <h5 class="card-header">Leave a Comment:</h5>
  <div class="card-body">
    <form>
      <div class="form-group">
        <textarea class="form-control" rows="3"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</div>

<!-- Single Comment -->
<div class="media mb-4">
  <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
  <div class="media-body">
    <h5 class="mt-0">Commenter Name</h5>
    Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio,
    vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia
    congue felis in faucibus.
  </div>
</div>

<!-- Comment with nested comments -->
<div class="media mb-4">
  <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
  <div class="media-body">
    <h5 class="mt-0">Commenter Name</h5>
    Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio,
    vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia
    congue felis in faucibus.

    <div class="media mt-4">
      <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
      <div class="media-body">
        <h5 class="mt-0">Commenter Name</h5>
        Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio,
        vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec
        lacinia congue felis in faucibus.
      </div>
    </div>

    <div class="media mt-4">
      <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
      <div class="media-body">
        <h5 class="mt-0">Commenter Name</h5>
        Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio,
        vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec
        lacinia congue felis in faucibus.
      </div>
    </div>

  </div>
</div>

{% endblock %}
```

## post_detail 수정하기

> blog/templates/post_detail.html

```djagno
{% extends 'blog/base.html' %}
<!-- 포스트의 title을 반영한다. -->
{% block title %}{{ object.title }}{% endblock %}
{% block content %}
<!-- Title -->
<h1>{{ object.title }}</h1>

<!-- Author -->
<p class="lead">
  by
  <a href="#">{{ object.author.username }}</a>
</p>
``` 


## 테스트 코드 추가

> blog/tests.py

```python
# post datail의 내용들이 잘 들어갔는지 확인하기 위한 코드
    body = soup.body
    main_div = body.find('div', id='main_div')
    self.assertIn(post_000.title, main_div.text)
    self.assertIn(post_000.author.username, main_div.text)

    self.assertIn(post_000.content, main_div.text)
```