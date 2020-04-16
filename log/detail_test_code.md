# Post Detail 페이지 테스트 코드 작성하기

## 절대 경로를 얻기 위함 함수 만들기

> blog/models.py

```python
def get_absolute_url(self):
    return '/blog/{}/'.format(self.pk)
```

admin 페이지내의 post에 `view on site`버튼이 활성화 된다.


> blog/tests.py

```python
def create_post(title, content, author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
    )
```

## detail을 확인하기 위한 함수를 생성

> blog/tests.py

```python
 # post detail을 확인하기 위한 함수
def test_post_detail(self):
    post_000 = create_post(
        title="The first post",
        content="Hello World. We are the world.",
        author=self.author_000,
    )

    self.assertGreater(Post.objects.count(), 0)
    post_000_url = post_000.get_absolute_url()
    self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))


    response = self.client.get(post_000_url)
    self.assertEqual(response.status_code, 200)

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title

    self.assertEqual(title.text, '{}'.format(post_000.title))

    self.check_navbar(soup)
```


## 전체 소스 코드

```python
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from  .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.

def create_post(title, content, author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
    )

    return blog_post

class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')


    def check_navbar(self, soup):
        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id='navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)

    def test_post_list(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        # # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        # navbar = soup.find('div', id = 'navbar')
        # # 내용중에서 Blog가 들어가 있는지 확인한다.
        # self.assertIn('Blog', navbar.text)
        # # 내용준에서 About me가 들어가 있는지 확인한다.
        # self.assertIn('About me', navbar.text)

        # Blog 포스트가 없는 경우에는 아직 없습니다를 띄어준다.
        self.assertEqual(Post.objects.count(), 0)
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)


        # test에는 database에 실재 데이터가 담겨 있는지는 고려하지 앟는다.
        # 새로 db를 만들고 그 안에서 test를 진행한다.

        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
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


    # post detail을 확인하기 위한 함수
    def test_post_detail(self):
        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))


        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{}'.format(post_000.title))

        self.check_navbar(soup)
```