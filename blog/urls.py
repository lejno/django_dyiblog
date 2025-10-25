from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<str:pk>/', views.post_detail, name='post-detail'),
    path('post/<str:pk>/addcomment/', views.addComment, name='add-comment'),
]