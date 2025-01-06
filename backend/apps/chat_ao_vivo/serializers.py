from rest_framework import serializers
from .models import Chat_ao_vivoModel


class Chat_ao_vivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat_ao_vivoModel
        fields = "__all__"
