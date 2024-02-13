from rest_framework import serializers
from .models import *

class MainPostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)

    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, instance):
        serializer = MainCommentSerializer(read_only=True)
        return serializer.data

    class Meta:
        model = MainPost
        fields = '__all__'

class MainCommentSerializer(serializer.ModelSerializer):

    #mainpost = serializers.SerializerMethodField()

    class Meta:
        model = MainComment
        fields = '__all__'
        read_only_fields = ['mainpost']

class MainReplySerializer(serializer.ModelSerializer):

    class MEta:
        model = MainReply
        fields = '__all__'
        read_only_fields = ['maincomment']