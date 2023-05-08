from django.urls import path
from .views import CommentCreateView

urlpatterns = [
    path("products/comment/<int:pk>/", CommentCreateView.as_view()),
]
