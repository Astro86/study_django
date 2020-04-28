# blog 앱 만들기 & Post 모델 만들기 & admin에 추가하기

## 블로그 앱 만들기

```python
python manage.py startapp blog
```

## Post 모델 만들기

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
    author = models.ForeignKey(User)
```

## blog 앱 추가하기

> mysite/setting.py

```python
INSTALLED_APPS = [
    'blog',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## 마이그레이션 하기

```python
python manage.py makemigrations
```

## 오류가 뜸...

```python
TypeError: __init__() missing 1 required positional argument: 'on_delete'
```

## CASCADE 옵션을 주기

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
```

## ForeignKey에 대한 on_delete 옵션

| 옵션                 | 설명                                                                     |
| ------------------ | ---------------------------------------------------------------------- |
| models.CASCADE     | ForeignKeyField가 바라보는 값이 삭제될 때 관련된 모든 row를 삭제한다.                       |
| models.PROTECT     | ForeignKeyField가 바라보는 값이 삭제될 때 삭제가 되지 않도록 ProtectedError를 발생시킨다.       |
| models.SET_NULL    | ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 NULL로 한다.             |
| models.SET_DEFAULT | ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 default로 바꾼다.          |
| models.set()       | ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 SET에 의해 설정된 값으로 설정한다. |
| models.DO_NOTHING  | ForeignKeyField가 바라보는 값이 삭제될 때 아무런 행동을 취하지 않는다.                        |

## admin 계정 만들기

```python
python manage.py createsuperuser
```

<image src="../image/admin.png" width = 350>

## admin 페이지에 blog의 Post를 반영하기

> blog/admin.py

```python
from django.contrib import admin
from .models import Post

# Register your models here.

admin.site.register(Post)
```

<image src="../image/admin_post.png" width = 350>
