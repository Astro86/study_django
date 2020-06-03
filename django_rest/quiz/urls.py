from django.urls import path, include
from .views import HelloAPI, randomQuiz

urlpatterns = [
    path("hello/", HelloAPI),
    path("<int:id>/", randomQuiz),
]