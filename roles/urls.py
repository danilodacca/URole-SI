from django.urls import path
from django.urls import path
from . import views

app_name = 'roles'
urlpatterns = [
    path('', views.RolesListView.as_view(), name='index'),
    path('<int:pk>/', views.PostsDetailView.as_view(), name='details'),
    path('mytickets/', views.MyTicketsListView, name='mytickets'),
    path('search/', views.search_roles, name='search'),
    path('create/', views.PostsCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.PostsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.PostsDeleteView.as_view(), name='delete'),
    path('<int:pk>/tickets', views.TicketsListView, name='tickets'),
    path('<int:pk>/tickets/create', views.TicketsCreateView.as_view(), name='create_ticket'),
    path('<int:pk>/tickets/<str:type>/update', views.TicketsUpdateView.as_view(), name='update_ticket'),
    path('<int:pk>/tickets/<str:type>/delete', views.TicketsDeleteView.as_view(), name='delete_ticket'),
    path('<int:pk>/tickets/<str:type>/buy', views.TicketsBuyView.as_view(), name='buy_ticket'),
]