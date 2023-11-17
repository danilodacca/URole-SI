from django.urls import path
from django.urls import path
from . import views

app_name = 'receitas'
urlpatterns = [
    path('', views.list_receitas, name='index'),
    path('search/', views.search_receitas, name='search'),
    path('<int:receita_id>/', views.detail_receita, name='details'),
    path('create/', views.create_receita, name='create'),
]