# 로그인 사용자만 접속 가능하게 하기 

## 테스트 코드 작성

> blog/tests.py

```python
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
```

## 뷰 수정하기

> blog/views.py

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category',
        # 'tags'
    ]

    def form_valid(self, form):
        # 작성자를 가지고 온다.
        current_user = self.request.user

        # 로그인을 한 상태인지 확인을 한다.
        if current_user.is_authenticated:
            # form의 author를 현재 작성중인 사람으로 채워 넣어
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else :
            return redirect('/blog/')
```

PostCreate에서 LoginRequiredMixin을 추가적으로 상속한다.