from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    # 제목
    title = models.CharField(max_length=30)
    # 내용
    content = models.TextField()

    # 작성 일자
    create = models.DateTimeField()
    # 저자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
