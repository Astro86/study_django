# Comment (댓글) view 구현하기

## 테스트 코드 작성

> blog/tests.py

```python
# Comment를 생성한다.
comment_000 = create_post(post_000,
                            text='a test comment',
                            author=self.author_obama)


    # Comment
    comments_div = main_div.find('div', id='comment-list')
    self.assertIn(comment_000.author.username, comments_div.text)
    self.assertIn(comment_000.text, comments_div.text)
```

## post_detail 수정하기

> blog/templates/blog/post_detail.html

```django
<!-- Comment -->
<div id="comment-list">
{% for comment in object.comment_set.all %}
  <div class="media mb-4">
    <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
    <div class="media-body">
      <h5 class="mt-0">{{ comment.author }}</h5>
      {{ comment.get_markdwon_content | safe }}
    </div>
  </div>
{% endfor %}
</div>
```

## admin 사이트에서 comment확인할 수 있게 반영하기

> blog/admin.py

```python
from django.contrib import admin
from .models import Post, Category, Comment

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # 미리 만들어지는 field
    # slug를 자동으로 만들어준다.
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
```

## markdown 적용해주기

> blog/models.py

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # markdown을 html로 바꿔준다.
    def get_markdwon_content(self):
        return markdown(self.text)
```

