from django.urls import path
from django.urls import path
from . import views

app_name = 'receitas'
urlpatterns = [
    path('', views.PostsListView.as_view(), name='index'),
    path('<int:pk>/', views.PostsDetailView.as_view(), name='details'),
    path('create/', views.PostsCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.PostsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.PostsDeleteView.as_view(), name='delete'),
    path('<int:post_id>/comment/', views.create_comment, name='comment'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/create', views.CategoryCreateView.as_view(), name='create-category'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category'),
    
]