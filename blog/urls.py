from django.urls import path, include
from .import views


urlpatterns = [
    # path('', views.index),
    # path('<int:pk>/', views.post_detail),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]
