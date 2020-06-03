from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown



# Create your models here.
# 카테고리를 추가한다.
class Category(models.Model):
    # Category의 이름이 유일할 수 있게 unique옵션을 준다.
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    # unicode를 허용한다.
    # slug를 이용하여 url에 카테고리가 뜰 수 있게 해준다.
    slug = models.SlugField(unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

    # 카테고리 이름을 출력해준다.
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    # 제목
    title = models.CharField(max_length=30)
    # 내용
    # content = models.TextField()
    # 마크다운을 사용할 수 있게 MarkdownField로 바꿔준다.
    content = MarkdownxField()


    # 이미지 파일 저장을 위한 객체
    # upload된 이미지 파일은 blog에 저장이 된다. blank = True는 공란이여도 된다는 의미이다.
    head_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)

    # 작성 일자
    created = models.DateTimeField(auto_now_add=True)
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

    # update된 url을 반환하기 위한 함수
    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    # markdown을 html로 바꿔준다.
    def get_markdwon_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 댓글을 쓴 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정한 일자
    modified_at = models.DateTimeField(auto_now=True)

    # markdown을 html로 바꿔준다.
    def get_markdwon_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)