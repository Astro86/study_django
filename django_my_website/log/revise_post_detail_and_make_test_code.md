# Post Detail 개선사항 도출하고 Test 코드 만들기

1. post에 카테고리 표시하기
2. edit 버튼 만들기
3. post에 그림이 나타나게 해주기
4. 줄바꿈이 적용될 수 있게 바꿔주기 -> 마크다운 이용하기

##  post에 카테고리 표시하기


### 테스트 코드 만들어주기

> blog/tests.py

```python
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
```

> blog/templates/blog/post_detail.html

```python
{% if p.category %}
<!-- badge가 오른쪽에 붙을 수 있게 float-right옵션을 이용한다. -->
<span class="badge badge-primary float-right">{{ p.category }}</span>
{% else %}
<span class="badge badge-primary float-right">미분류</span>
{% endif %}
```

post_list.html로부터 category부분의 내용을 post_detail.html에 붙여준다.


## Edit 버튼 만들기

> blog/templates/blog/post_detail.html

```django
<!-- 로그인 한 사용자가 author와 같으면 EDIT 버튼을 보여준다.-->
{% if request.user == object.author %}
  <span class="badge badge-info float-right">EDIT</span>
{% endif %}
```

## 버튼 형식으로 만들기

> blog/templates/blog/post_detail.html

```django
<!-- 로그인 한 사용자가 author와 같으면 EDIT 버튼을 보여준다.-->
{% if request.user == object.author %}
  <button type="button" class="btn btn-sm btn-secondary float-right">EDIT</button>
{% endif %}
```

## 다른 사람으로 로그인 되는 경우에 대해서 테스트 코드 작성

> blog/tests.py

```python
login_success = self.client.login(username='obama', password='nopassword')  # login을 한 경우에는
self.assertTrue(login_success)

response = self.client.get(post_000_url)
self.assertEqual(response.status_code, 200)

soup = BeautifulSoup(response.content, 'html.parser')
main_div = soup.find('div', id='main-div')

self.assertEqual(post_000.author, self.author_000)  # post.author와 login한 사람이 같으면
self.assertNotIn('EDIT', main_div.text)  # EDIT button이 있다.
```