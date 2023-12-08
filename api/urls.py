from django.urls import path
from .views import RoleList, RoleDetail

urlpatterns = [
    path('roles/<int:pk>/', RoleDetail.as_view()),
    path('roles/', RoleList.as_view()),
]