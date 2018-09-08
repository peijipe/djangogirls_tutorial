from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>', views.detail, name='detail'),
    path('post/new/', views.create, name='create'),
    path('post/<int:pk>/edit/', views.edit, name='edit'),
    path('post/<int:pk>/delete/', views.delete, name='delete'),
    ]