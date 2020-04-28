from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from .models import Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    @action(detail=True, methods=['POST'])
    def like_post(self, request, pk=None):
        post = Post.objects.get(id=pk)
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            serializer = LikeSerializer(like, many=False)
            response = {'message': 'You have already liked this post', 'result': serializer.data}
            return Response(response, status=status.HTTP_304_NOT_MODIFIED)

        except:
            like = Like.objects.create(user=user, post=post)
            serializer = LikeSerializer(like, many=False)
            response = {'message': 'Post have been liked!', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create like like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update like like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'You cant delete like like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
