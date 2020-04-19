# Comment 작성일 추가하기, edit, delete 버튼 만들기

1. 댓글 작성일 추가하기
2. 본인이 작성한거 수정하거나 지우는 기능 추가하기

## 댓글 작성일 추가하기

> blog/models.py

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 댓글을 쓴 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정한 일자
    modified_at = models.DateTimeField(auto_now=True)

    # markdown을 html로 바꿔준다.
    def get_markdwon_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)
```

### template에 반영하기

> blog/templates/blog/post_detail.html

```django
<!-- Comment -->
<div id="comment-list">
{% for comment in object.comment_set.all %}
  <div class="media mb-4" id="comment-id-{{ comment.pk }}">
    <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
    <div class="media-body">
      <h5 class="mt-0">{{ comment.author }} <small class="text-muted">{{ comment.created_at }}</small></h5>
      {{ comment.get_markdwon_content | safe }}
    </div>
  </div>
{% endfor %}
</div>
```

## 본인이 작성한거 수정하거나 지우는 기능 추가하기

### 테스트 코드 추가하기

> blog/tests.py

```python
# comment-list들을 모두 가져온다.
# 본인이 작성한 comment의 경우 edit와 delete가 보이는지 확인한다.
comment_div = main_div.find('div', id='comment-list')
comment_000_div = comment_div.find('div', id='comment-id-{}'.format(comment_000.pk))
self.assertIn('edit', comment_000_div.text)
self.assertIn('delete', comment_000_div.text)

# 본인이 작성하자ㅣ 않은 comment의 경우 edit와 delete가 보여서는 안된다.
comment_001_div = comment_div.find('div', id='comment-id-{}'.format(comment_001.pk))
self.assertNotIn('edit', comment_001_div.text)
self.assertNotIn('delete', comment_001_div.text)
```

### edit와 delete 버튼을 만들어주기

> blog/templates/blog/post_detail.html

```django
<!-- Comment -->
<div id="comment-list">
{% for comment in object.comment_set.all %}
  <div class="media mb-4" id="comment-id-{{ comment.pk }}">
    <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
    <div class="media-body">
        <!-- edit와 delete button-->
        {% if comment.author == request.user %}
        <button class="btn btn-sm btn-info float-right">edit</button>
        <button class="btn btn-sm btn-warning float-right">delete</button>
        {% endif %}
      <h5 class="mt-0">{{ comment.author }} <small class="text-muted">{{ comment.created_at }}</small></h5>
      {{ comment.get_markdwon_content | safe }}
    </div>
  </div>
{% endfor %}
</div>
```