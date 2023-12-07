from django.urls import path, include
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('post/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('drf-auth', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)