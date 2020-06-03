from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Comment
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.

# 카테고리 생성을 위한 코드


def create_category(name='life', description=""):
    category, is_created = Category.objects.get_or_create(
        name=name,
        description=description
    )


    category.slug = category.name.replace(' ', '-').replace('/', '')
    category.save()

    return category


def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
        category=category,
    )

    return blog_post

# commnet를 생성하는 함수
def create_comment(post, text='a comment', author=None):
    if author is None:
        author, is_created = User.objects.get_or_create(
            username='guset',
            password='guestpassword'
        )

    comment = Comment.objects.create(
        post=post,
        text=text,
        author=author
    )

    return comment


# Models.py의 기능을 확인하기 위한 코드
class TestModel(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create(
            username='smith', password='nopassword')

    # 카테고리를 테스트 하기 위한 코드
    def test_category(self):
        category = create_category()

    # post를 확인하기 위한 코드
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



# Views.py를 테스트 하기 위한 코드
class TestView(TestCase):
    def setUp(self):
        # 브라우저 역할을 해준다.
        self.client = Client()
        self.author_000 = User.objects.create_user(username='smith', password='nopassword')
        self.author_obama = User.objects.create_user(username='obama', password='nopassword')

    def check_navbar(self, soup):
        # Beautifulsoup 객체로부터 div 태그를 갖고 id는 navbar를 가진 내용을 가져온다.
        navbar = soup.find('div', id='navbar')
        # 내용중에서 Blog가 들어가 있는지 확인한다.
        self.assertIn('Blog', navbar.text)
        # 내용준에서 About me가 들어가 있는지 확인한다.
        self.assertIn('About me', navbar.text)

    def check_right_side(self, soup):
        category_card = soup.find('div', id='category-card')

        self.assertIn('미분류(1)', category_card.text)  # 미분류 (1)이 있어야 한다.
        self.assertIn('정치/사회(1)', category_card.text)  # 정치/사회(1)이 있어야 한다.


    # 포스트가 없을 때 테스트하기 위한 코드

    def test_post_list_no_post(self):
        # blog로 get요청을 한 후
        response = self.client.get('/blog/')
        # 응답 값이 200이랑 같은지 확인해라
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        # self.assertEqual(title.text, 'Blog')
        self.assertIn(title.text , 'Blog')

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

    # 포스트가 있는 상태에서 테스트하기 위한 코드

    def test_post_list_with_post(self):
        # test에는 database에 실재 데이터가 담겨 있는지는 고려하지 앟는다.
        # 새로 db를 만들고 그 안에서 test를 진행한다.

        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        post_001 = create_post(
            title="The second post",
            content="Second Second Second",
            author=self.author_000,
            category=create_category(name='정치/사회'),
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

        # button 확인을 위한 코드
        post_000_read_more_button = body.find(
            'a', id="read-more-post-{}".format(post_000.pk))
        self.assertEqual(
            post_000_read_more_button['href'], post_000.get_absolute_url())

        # category card에서
        self.check_right_side(soup)

        main_div = soup.find('div', id='main-div')
        self.assertIn('정치/사회', main_div.text)  # '정치/사회' 있어야 함
        self.assertIn('미분류', main_div.text)  # '미분류' 있어야 함

        # category_card = body.find('div', id='category-card')
        # self.assertIn('미분류(1)', category_card.text) #### 미분류 (1)이 있어야 한다.
        # self.assertIn('정치/사회(1)', category_card.text) #### 정치/사회(1)이 있어야 한다.
        #
        #
        # main_div = body.find('div', id='main_div')
        # self.assertIn('정치/사회', main_div.text) ###'정치/사회' 있어야 함
        # self.assertIn('미분류', main_div.text) ### '미분류' 있어야 함

    # post detail을 확인하기 위한 함수

    def test_post_detail(self):
        category_politics = create_category(name='정치/사회')
        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
            category=category_politics
        )

        post_001 = create_post(
            title="The second post",
            content="Second Second Second",
            author=self.author_000,
        )

        # Comment를 생성한다.
        comment_000 = create_comment(post_000,
                                  text='a test comment',
                                  author=self.author_obama)

        comment_001 = create_comment(post_000,
                                  text='a test comment',
                                  author=self.author_000)

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        print(title.text)
        self.assertEqual(title.text, '{}'.format(post_000.title))

        self.check_navbar(soup)

        # post datail의 내용들이 잘 들어갔는지 확인하기 위한 코드
        body = soup.body
        main_div = body.find('div', id='main-div')
        self.assertIn(post_000.title, main_div.text)
        self.assertIn(post_000.author.username, main_div.text)

        self.assertIn(post_000.content, main_div.text)

        # category가 잘 작동하는지 확인하기
        self.check_right_side(soup)

        # Comment
        comments_div = main_div.find('div', id='comment-list')
        self.assertIn(comment_000.author.username, comments_div.text)
        self.assertIn(comment_000.text, comments_div.text)



        self.assertIn(category_politics.name, main_div.text) # category가 main_div에 있다.
        self.assertNotIn('EDIT', main_div.text) # EDIT 버튼이 로그인 하지 않은 경우 보이지 않는다.

        login_success = self.client.login(username='smith', password='nopassword') # login을 한 경우에는
        self.assertTrue(login_success)

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        self.assertEqual(post_000.author, self.author_000) # post.author와 login한 사람이 같으면
        self.assertIn('EDIT', main_div.text) # EDIT button이 있다.


        # 다른 사람인 경우에는 없다.
        login_success = self.client.login(username='obama', password='nopassword')  # login을 한 경우에는
        self.assertTrue(login_success)

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        self.assertEqual(post_000.author, self.author_000)  # post.author와 login한 사람이 같으면
        self.assertNotIn('EDIT', main_div.text)  # EDIT button이 있다.

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



    # 카테고리가 있는 post를 test하기 위한 함수
    def test_post_list_by_category(self):
        category_politics = create_category(name='정치/사회')

        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        post_001 = create_post(
            title="The second post",
            content="Second Second Second",
            author=self.author_000,
            category=category_politics,
        )

        response = self.client.get(category_politics.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title
        # self.assertEqual('Blog - {}'.format(category_politics.name), soup.title.text)

        main_div = soup.find('div', id='main-div')
        self.assertNotIn('미분류', main_div.text)
        self.assertIn(category_politics.name, main_div.text)

    # 미분류 카테고리에 관한 test함수
    def test_post_list_no_category(self):
        category_politics = create_category(name='정치/사회')

        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        post_001 = create_post(
            title="The second post",
            content="Second Second Second",
            author=self.author_000,
            category=category_politics,
        )

        # url이 /blog/category/_none/이다.
        response = self.client.get('/blog/category/_none/')
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title
        # self.assertEqual('Blog - {}'.format(category_politics.name), soup.title.text)

        main_div = soup.find('div', id='main-div')
        self.assertIn('미분류', main_div.text)
        self.assertNotIn(category_politics.name, main_div.text)

    # post_create를 확인하기 위한 테스트 코드
    def test_post_create(self):
        response = self.client.get('/blog/create/')
        # 로그인 하지 않은 상태에서는 create로 접속시에 200이 뜨면 안된다.
        self.assertNotEqual(response.status_code, 200)

        # 로그인을 했을 때만 create로 접속시 200이 뜨게 해야 한다.
        self.client.login(username='smith', password='nopassword')
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        # self.assertIn('New Post', main_div.text)



    # post_update를 확인하기 위한 테스트 코드
    def test_post_update(self):
        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        self.assertEqual(post_000.get_update_url(), post_000.get_absolute_url() + 'update/')

        response = self.client.get(post_000.get_update_url())
        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        # created와 author가 없어야 한다.
        self.assertNotIn('Created', main_div.text)
        self.assertNotIn('Author', main_div.text )

    def test_new_comment(self):
        post_000 = create_post(
            title="The first post",
            content="Hello World. We are the world.",
            author=self.author_000,
        )

        # 로그인 하기
        login_success = self.client.login(username='smith', password='nopassword')
        self.assertTrue(login_success)

        # post를 이용하여 서버에 데이터를 보낸다.
        # redirect하는 것까지 확인을 해봐라
        response = self.client.post(
            post_000.get_absolute_url() + 'new_comment/',
            {'text': 'A test comment for the first comment'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')
        self.assertIn(post_000.title, main_div.text)
        self.assertIn('A test comment', main_div.text)