from django.contrib import admin
from .models import Post, Category, Comment

from markdownx.widgets import AdminMarkdownxWidget
from django.db import models
class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class CategoryAdmin(admin.ModelAdmin):
    # 미리 만들어지는 field
    # slug를 자동으로 만들어준다.
    prepopulated_fields = {'slug': ('name', )}


# Register your models here.
# admin.site.register(Post, MyModelAdmin)
admin.site.register(Post,)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)