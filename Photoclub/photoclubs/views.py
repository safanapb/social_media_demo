from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserSerializer, AdminUserSerializer, TagSerializer, PostCreationSerializer, \
    PostListSerializer, UserLikeSerializer
from django.db import IntegrityError
from .models import User, Tag, Post, Photo, UserLike
from .helpers import count_increment


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.data
            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "User already exist"})


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.data
            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Admin created"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "Admin/user already exist"})


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                Tag.objects.create(
                    name=request.data.get('name'),
                    weight=request.data.get('weight'),
                    created_by=request.user
                )
                return Response({"message": "Tag created"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        query_set = Tag.objects.all()
        return Response(self.serializer_class(query_set, many=True).data,
                        status=status.HTTP_200_OK)


class PostCreationViewSet(viewsets.ModelViewSet):
    serializer_class = PostCreationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                ins = Post.objects.create(
                    description=request.data.get('description'),
                    created_by=request.user
                )
                for tag in request.data.getlist('tags'):
                    ins.tags.add(tag)
                for photo in request.FILES.getlist('files'):
                    Photo.objects.create(
                        file=photo,
                        post=ins
                    )
                return Response({"message": "Post created"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_403_FORBIDDEN)


class PostListViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        query_set = Post.objects.all()
        return Response(self.serializer_class(query_set, many=True).data,
                        status=status.HTTP_200_OK)


class UserLikeViewSet(viewsets.ModelViewSet):
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post_id = request.data.get('post')
            like = request.data.get('like')
            obj = Post.objects.filter(id=post_id).first()
            if obj:
                like_obj = UserLike.objects.filter(user=request.user, post=obj).first()
                in_count_obj = Post.objects.get(id=post_id)
                if like_obj:
                    UserLike.objects.update(
                        user=request.user,
                        post=obj,
                        like=like
                    )
                    if like_obj.like != like:
                        count_increment(like, in_count_obj)
                else:
                    if like:
                        UserLike.objects.create(
                            user=request.user,
                            post=obj,
                            like=like
                        )
                        count_increment(like, in_count_obj)
                return Response({"message": "Success"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



