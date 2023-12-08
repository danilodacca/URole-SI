from rest_framework import serializers

from roles.models import Role


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['name', 'date', 'start_time', 'end_time', 'address', 'banner_url', 'about']
