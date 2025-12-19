from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView, RegisterAPIView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='post_comments'),
    path('registration/', RegisterAPIView.as_view(), name='registration'),

]

