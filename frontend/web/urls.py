from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name="home"),
    path('chat/', views.chat, name="chat"),
    path('blog/', views.blog, name="blog"),
    path('categories/', views.category_list, name='category_list'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
]