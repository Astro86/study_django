# Comment (댓글) 모델 구현하기

## 테스트 코드 작성하기

> blog/tests.py

```python
# commnet를 생성하는 함수
def create_comment(post, text='a comment', author=None):
    if author is None:
        author, is_created = User.objects.get_or_create(
            username='guset',
            password='guestpassword'
        )

    comment = Comment.objects.create(
        post = post,
        text = text,
        author = author
    )

    return comment

    # class test_Model에 추가
    # 댓글 기능에 관한 test
    def test_comment(self):
        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        self.assertEqual(Comment.objects.count(), 0)

        comment_000 = create_comment(
            post=post_000
        )

        comment_001 = create_comment(
            post=post_000,
            text='second comment'
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(post_000.comment_set.count(), 2)

```

## comment 모델 추가하기

> blog/models.py

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```