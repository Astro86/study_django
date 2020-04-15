# Post List 페이지 테스트 코드 작성하기 part A

## 테스트 실행하기

```shell
python manage.py test
```

## 테스트 코드 작성하기

> blog/tests.py

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from  .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_post_list(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id = 'navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)
```


## 실행 결과

```shell
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.019s

OK
Destroying test database for alias 'default'...
```

## 포스트가 하나도 없는 경우의 test

> blog/tests.py

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from  .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_post_list(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id = 'navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)

        # Blog 포스트가 없는 경우에는 아직 없습니다를 띄어준다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)
```

## 포스트를 추가한 후 test진행하기

> blog/tests.py

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from  .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_post_list(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id = 'navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)

        # Blog 포스트가 없는 경우에는 아직 없습니다를 띄어준다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)


        # test에는 database에 실재 데이터가 담겨 있는지는 고려하지 앟는다.
        # 새로 db를 만들고 그 안에서 test를 진행한다.

        post_000 = Post.objects.create(
            title = "The first post",
            content="Hello World. We are the world.",
            created=timezone.now(),
            author=self.author_000,
        )

        # Blog 포스터가 존재하는 경우
        self.assertGreater(Post.objects.count(), 0)
```

## 데이터 베이스에 제대로 들어가 있는지 확인하기

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from  .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_post_list(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id = 'navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)

        # Blog 포스트가 없는 경우에는 아직 없습니다를 띄어준다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)


        # test에는 database에 실재 데이터가 담겨 있는지는 고려하지 앟는다.
        # 새로 db를 만들고 그 안에서 test를 진행한다.

        post_000 = Post.objects.create(
            title = "The first post",
            content="Hello World. We are the world.",
            created=timezone.now(),
            author=self.author_000,
        )

        # Blog 포스터가 존재하는 경우
        self.assertGreater(Post.objects.count(), 0)


        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        # post_000이 들어가 있는 상태라 아직 게시물이 없습니다가 나오면 안된다.
        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        # post_000이 제대로 들어가 있는지 확인한다.
        self.assertIn(post_000.title, body.text)
```