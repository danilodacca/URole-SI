from django.urls import path
from django.urls import path
from . import views

app_name = 'roles'
urlpatterns = [
    path('', views.RolesListView.as_view(), name='index'),
    path('<int:pk>/', views.PostsDetailView.as_view(), name='details'),
    path('search/', views.search_roles, name='search'),
    path('create/', views.PostsCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.PostsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.PostsDeleteView.as_view(), name='delete'),
]