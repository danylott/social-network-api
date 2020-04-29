from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Like, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'number_of_likes')
        extra_kwargs = {'author': {'read_only': True, 'required': False}}

    def create(self, validated_data):
        author = self.context['request'].user
        post = Post.objects.create(
            author=author,
            **validated_data
        )
        return post


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'pub_date')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'last_activity', 'last_login')
