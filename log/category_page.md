# Category 페이지 만들기 (slugField)

## Category에 get_absolute_url추가하기
> blog/models.py

```python
# Create your models here.
# 카테고리를 추가한다.
class Category(models.Model):
    # Category의 이름이 유일할 수 있게 unique옵션을 준다.
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    # unicode를 허용한다.
    # slug를 이용하여 url에 카테고리가 뜰 수 있게 해준다.
    slug = models.SlugField(unique=True, allow_unicode=True)

    def get_absoulte_url(self):
        return '/blog/category/{}/'.format(self.slug)

    # 카테고리 이름을 출력해준다.
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
```

## admin에 slug가 자동으로 생성 될 수 있게하기

> blog/admin.py

```python
from django.contrib import admin
from .models import Post, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # 미리 만들어지는 field
    # slug를 자동으로 만들어준다.
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
```

## url 만들어주기

> blog/urls.py

```python
from django.urls import path, include
from .import views


urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.post_detail),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]
```

> blog/models.py

```python
class PostListByCategory(PostList):
    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).
```

## 

> blog/templates/blog/base.html

```html
<!-- title이 있는 경우에 -->
{% if title %}
    {% block title %}{{ title }}{% endblock %}
{% endif %}
{% block content %}
```
내용 추가하기

## view 수정하기

> blog/view.py

```python
class PostListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)

        context['title'] = 'Blog - {}'.format(category.name)
        return context
```

## 카테고리 버튼 활성화 하기

```html
<a href="{{ category.get_absolute_url }}">{{ category.name }}({{ category.post_set.count }})</a>
```

## 제목에 카테고리 표현해 주기

> blog/templates/blog/post_list.html

```html
<h1>Blog {% if category  %} <small>{{ category }}</small>{% endif %}</h1>
```

> blog/views.py

```python
slug = self.kwargs['slug']
    category = Category.objects.get(slug=slug)
    context['category'] = category
```

## 제목 카테고리 하얗게 하기

```html
<h1>Blog {% if category  %} <small class="text-muted">: {{ category }}</small>{% endif %}</h1>
```

## 미분류 활성화 하기

> blog/templates/blog/base.html

```html
<a href="/blog/category/_none/">미분류({{ posts_without_category }})</a>
```

### 테스트 코드 작성하기

> blog/tests.py

```python
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
```

### views.py 수정하기

> blog/views.py

```python
class PostListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        # slug가 none인경우
        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # Post들 중에서 category가 None인 것의 갯수를 가져온다.
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        # slug가 none인경우
        if slug == '_none':
            context['category'] = '미분'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context
```