from rest_framework import generics

from roles.models import Role
from .serializers import RoleSerializer


class RoleList(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetail(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
