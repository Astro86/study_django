# 블로그 post list와 post detail 페이지에 카테고리 추가하기

## 테스트 코드 작성하기

> blog/tests.py

```python
post_001 = create_post(
    title="The second post",
    content="Second Second Second",
    author=self.author_000,
    category=create_category(name='정치/사회')
)

# category card에서
    category_card = body.find('div', id='category-card')
    self.assertIn('미분류(1)', category_card.text) #### 미분류 (1)이 있어야 한다.
    self.assertIn('정치/사회(1)', category_card.text) #### 정치/사회(1)이 있어야 한다.


    main_div = body.find('div', id='main_div')
    self.assertIn('정치/사회', main_div.text) ###'정치/사회' 있어야 함
    self.assertIn(('미분류', main_div.text)) ### '미분류' 있어야 함
```

## id 추가하기

> blog/templates/blog/base.html

```html
<div class="card my-4" id = "category-card">
```

## 카테고리 카드 수정해주기

> blog/views.py

```python
# templates로 추가적인 정보를 넘겨주고 싶을 경우
def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostList, self).get_context_data(**kwargs)
    context['categories_list'] = Category.objects.all()
    # Post들 중에서 category가 None인 것의 갯수를 가져온다.
    context['posts_without_category'] = Post.objects.filter(category=None).count()

    return context
```

## base.html 수정하기

> blog/templates/blog/base.html

```html
<li>
    <a href="#">미분류({{ posts_without_category }})</a>
</li>
{% for category in category_list %}
<li>
    <a href="#">{{ category.name }}({{ category.post_set.count }})</a>
</li>
{% endfor %}
```

## Category코드 수정하기

> blog/models.py

```python
# Create your models here.
# 카테고리를 추가한다.
class Category(models.Model):
    # Category의 이름이 유일할 수 있게 unique옵션을 준다.
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    # 카테고리 이름을 출력해준다.
    def __str__(self):
        return self.name
```

## 카테고리가 없을 경우 미분류로 출력되게 html을 변경해준다.

> blog/templates/blog/post_list.html

```django
<!-- badge를 붙인다. -->
<!-- 카테고리가 있는 경우에는 카테고리를 보여주고, 없는 경우에는 미분류를 보여준다. -->
{% if p.category %}
<!-- badge가 오른쪽에 붙을 수 있게 float-right옵션을 이용한다. -->
<span class="badge badge-primary float-right">{{ p.category }}</span>
{% else %}
<span class="badge badge-primary float-right">미분류</span>
{% endif %}
```

## admin에 category를 등록하기