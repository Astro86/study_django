# Comment (댓글) 작성창 구현하기

## forms.py 파일 생성하기

> blog/

해당 돌더에 forms.py 파일을 생성한다.

```python
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'text',}
```

## 테스트 코드 작성하기

> blog/tests.py

```python
# post를 이용하여 서버에 데이터를 보낸다.
response = self.client.post(
    post_000.get_absolute_url() + 'new_comment/',
    {'text':'A test comment for the first comment'},
    follow=True # redirect하는 것까지 확인을 해봐라
)
self.assertEqual(response.status_code, 200)
```

## views.py에 반영하기

> blog/views.py

```python
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()

        return context
```

## 템플릿에 반영하기

> blog/templates/blog/post_detail.html

```django
<!-- Comments Form -->
<div class="card my-4">
  <h5 class="card-header">Leave a Comment:</h5>
  <div class="card-body">
    <form>
      <div class="form-group">
          {{ comment_form }}
        <textarea class="form-control" rows="3"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</div>
```

## crispy-forms 설치히가

> pip install django-crispy-forms

## 설정에 crispy-forms추가하기

> mysite/settings.py

```python
INSTALLED_APPS = [
    'blog',
    'markdownx',
    'crispy_forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

## crispy filter추가하기

> blog/template/post_detail.html

```django
{% load crispy_forms_tags %}
```

## crispy filter반영하기

> blog/templates/blog/post_detail.html

```django
<!-- Comments Form -->
<div class="card my-4">
  <h5 class="card-header">Leave a Comment:</h5>
  <div class="card-body">
    <form method="post" action="{{ object.get_absolute_url }}new_comment/">{% csrf_token %}
      <div class="form-group">
          {{ comment_form | crispy }}
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</div>
```

## 댓글로 focus 맞춰주기

> blog/models.py

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # markdown을 html로 바꿔준다.
    def get_markdwon_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)
```

> blog/templates/blog/post_detail.html

```django
<!-- Comment -->
<div id="comment-list">
{% for comment in object.comment_set.all %}
  <div class="media mb-4" id="comment-id-{{ comment.pk }}">
    <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
    <div class="media-body">
      <h5 class="mt-0">{{ comment.author }}</h5>
      {{ comment.get_markdwon_content | safe }}
    </div>
  </div>
{% endfor %}
</div>
```