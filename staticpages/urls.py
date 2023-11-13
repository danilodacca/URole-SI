from django.urls import path

from . import views

urlpatterns = [
    path('receitas/', views.receitas, name='receitas'),
    path('', views.index, name='index'),
]