from django.urls import path, include, re_path
from . import views
from .views import register_user

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('post/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('drf-auth/', include('rest_framework.urls')), #в гуглі
    path('register/', register_user, name='register_user'), # в postman
    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),


]

urlpatterns = format_suffix_patterns(urlpatterns)