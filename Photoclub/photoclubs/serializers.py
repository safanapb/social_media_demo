from rest_framework import serializers
from .models import User, Photo, Tag, Post
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user


class AdminUserSerializer(UserSerializer):

    def create(self, validated_data):
        user = User.objects.create_superuser(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user


class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    weight = serializers.IntegerField(required=True)


class PostCreationSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField(), required=True)
    tags = serializers.ListField(child=serializers.IntegerField(), required=True)
    description = serializers.CharField(max_length=1000, required=True)


class PhotoListSerializer(serializers.Serializer):
    file = serializers.FileField()


class PostListSerializer(serializers.Serializer):
    files = serializers.SerializerMethodField('get_image_url')
    tags = serializers.SerializerMethodField('get_tags')
    description = serializers.CharField(max_length=1000, required=True)

    def get_image_url(self, obj):
        obj = Photo.objects.filter(post=obj)
        return PhotoListSerializer(obj, many=True).data

    def get_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data


class UserLikeSerializer(serializers.Serializer):
    like = serializers.BooleanField(required=True)
    post = serializers.IntegerField(required=True)