from rest_framework import serializers
from .models import *

class MainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Main
        fields = '__all__'