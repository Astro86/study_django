# 블로그 post에 카테고리 추가하기

## 테스트 코드 작성하기

> blog/tests.py

```python
# 카테고리 생성을 위한 코드
def create_category(name='life', description=""):
    category, is_created = Category.objects.get_or_create(
        name=name,
        description=description
    )

    return category


# 카테고리를 테스트 하기 위한
class TestModel(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(
            username='smith', password='nopassword')

    def test_category(self):
        category = create_category()

    def test_post(self):
        category = create_category(

        )

        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
            category=category
        )

        # 카테고리에서 포스트를 불러오는 코드
        self.assertEqual(category.post_set.count(), 1)
```

## 카테고리 만들어 주기

> blog/models.py

```python
# 카테고리를 추가한다.
class Category(models.Model):
    name = models.CharField(max_length=25) 
    description = models.TextField(black=True)
```

## 전체 소스 코드

```python
from django.db import models
from django.contrib.auth.models import User




# Create your models here.
# 카테고리를 추가한다.
class Category(models.Model):
    # Category의 이름이 유일할 수 있게 unique옵션을 준다.
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)


class Post(models.Model):
    # 제목
    title = models.CharField(max_length=30)
    # 내용
    content = models.TextField()
    # 이미지 파일 저장을 위한 객체
    # upload된 이미지 파일은 blog에 저장이 된다. blank = True는 공란이여도 된다는 의미이다.
    head_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)

    # 작성 일자
    created = models.DateTimeField()
    # 저자
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 카테고리 객체 추가
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    # 해당 객체를 문자열로 바꿧을 때 어떤 식으로 보여줄 것인지를 결정한다.
    def __str__(self):
        # 작성된 페이지의 제목과 저자를 보여준다.
        return '{} :: {}'.format(self.title, self.author)

    # 포스트의 절대 경로를 얻기 위한 함
    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)
```