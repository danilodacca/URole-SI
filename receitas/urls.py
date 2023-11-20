from django.urls import path
from django.urls import path
from . import views

app_name = 'receitas'
urlpatterns = [
    path('', views.list_posts, name='index'),
    path('search/', views.search_posts, name='search'),
    path('<int:post_id>', views.detail_post, name='details'),
    path('create/', views.create_post, name='create'),
    path('update/<int:post_id>/', views.update_post, name='update'),
    path('delete/<int:post_id>/', views.delete_post, name='delete'),
]