from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:username>/', views.user_detail, name='user-detail'),
    path('post/<str:pk>/', views.post_detail, name='post-detail'),
    path('post/<str:pk>/addcomment/', views.addComment, name='add-comment'),
]

