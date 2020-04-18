# Post 작성 화면 / 기능 구현하기

## new 버튼 만들기

> blog/templates/post_list.html

```django
<!--로그인 한 사용자에게만 보이게 하기-->
{% if user.is_authenticated %}
    <!-- new post button 만들기 -->
    <button class="btn btn-primary btn-sm float-right"
            onclick="location.href='/blog/create/'">new post</button>
{% endif %}
```

## post_create 만들기

### 테스트 코드 작성

> blog/tests.py

```python
# post_create를 확인하기 위한 테스트 코드
def test_post_create(self):
    response = self.client.get('/blog/create/')
    self.assertEqual(response.status_code, 200)

    # 정상적으로 이루어진 경우 BeautifulSoup을 이용해 html.parser로 파싱한 객체를 생성한다.
    soup = BeautifulSoup(response.content, 'html.parser')
    main_div = soup.find('div', id='main-div')

    # self.assertIn('New Post', main_div.text)
```

### url 추가하기

> blog/urls.py

```python
# 새로운 post를 생성하는 페이지로 넘어가기 위한 url
path('create/', views.PostCreate.as_view()),
```

### view에 반영하기

> blog/views.py

```python
from django.views.generic import CreateView

class PostCreate(CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category',
        # 'tags'
    ]
```

### 자동으로 채워주는 기능 활성화 하기

> blog/models.py

```python
# 작성 일자
    created = models.DateTimeField(auto_now_add=True)
```

### 작성중인 user가져오기

> blog/views.py

```python
def form_valid(self, form):
    current_user = self.request.user
    form.instance.author = current_user
    return super(type(self), self).form_valid(form)
```

## 로그인 한 상태인지 안한 상태인지 확인한 후 redirect하기

> blog/views.py

```python
class PostCreate(CreateView):
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