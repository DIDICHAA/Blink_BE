from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import *

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = obj.get_images()
        return PostImageSerializer(instance=images, many=True, context=self.context).data
    
    def get_writer(self, obj):
        if obj.is_anonymous:  
            return ""
        return obj.writer.id

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['writer']