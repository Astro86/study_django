# django 지역(시간) 세팅 수정하기, Post 개선하기 str

## 시간 세팅 수정하기

> mysite/setting.py

```python
TIME_ZONE = 'UTC'
```

```python
TIME_ZONE = 'Asia/Seoul'
```

<image src="../image/post_object.png" width = 450>

## str 추가하기

> blog/model.py

```python
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    # 제목
    title = models.CharField(max_length=30)
    # 내용
    content = models.TextField()

    # 작성 일자
    create = models.DateTimeField()
    # 저자
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 해당 객체를 문자열로 바꿧을 때 어떤 식으로 보여줄 것인지를 결정한다.
    def __str__(self):
        # 작성된 페이지의 제목과 저자를 보여준다.
        return '{} :: {}'.format(self.title, self.author)
```

<image src="../image/post_name.png" width = 450>