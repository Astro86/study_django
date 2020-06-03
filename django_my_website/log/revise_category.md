# 사소한 문제들 해결: 불필요한 내용 삭제하기; category 복수형 수정하기 (categorys -> categories)

## post_detail에 카테고리 반영하기

> blog/models.py

```python
def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostList, self).get_context_data(**kwargs)
    context['category_list'] = Category.objects.all()
    # Post들 중에서 category가 None인 것의 갯수를 가져온다.
    context['posts_without_category'] = Post.objects.filter(category=None).count()

    return context
```

> blog/tests.py

```python
def check_right_side(self, soup):
    category_card = soup.find('div', id='category-card')

    self.assertIn('미분류(1)', category_card.text)  #### 미분류 (1)이 있어야 한다.
    self.assertIn('정치/사회(1)', category_card.text)  #### 정치/사회(1)이 있어야 한다.

# category가 잘 작동하는지 확인하기
self.check_right_side(soup)
```