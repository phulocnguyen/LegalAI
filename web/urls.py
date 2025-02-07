from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name="home"),
    path('chat/', views.chat_with_ai_view, name="chat_with_ai"),
    path('categories/', views.category_list, name='category_list'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('account/', views.account, name="account"),
    path('logout/', views.logout_view, name='logout'),

    path('create_post/', views.create_post, name='create_post'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
