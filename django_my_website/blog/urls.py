from django.urls import path, include
from .import views


urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.post_detail),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),

    # post를 update하기 위한 페이지로 넘어가기 위한 url
    path('<int:pk>/update/', views.PostUpdate.as_view()),

    # 새로운 post를 생성하는 페이지로 넘어가기 위한 url
    path('create/', views.PostCreate.as_view()),

    # post를 update하기 위한 페이지로 넘어가기 위한 url
    path('<int:pk>/new_comment/', views.new_comment),

]
