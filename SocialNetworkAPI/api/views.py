from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrReadOnly

from .models import Post, Like, Profile
from .serializers import UserSerializer, PostSerializer, LikeSerializer, ProfileSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
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

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = Post.objects.get(id=pk)
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            response = {'message': 'Successfully unlike post'}
            return Response(response, status=status.HTTP_200_OK)

        except:
            response = {'message': 'You have not liked this project yet!'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


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


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes(IsAuthenticatedOrReadOnly)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create profile like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update profile like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'You cant delete profile like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class JWTAuthenticationView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        result = super(JWTAuthenticationView, self).post(request)
        try:
            # request_user, data = requests.get_parameters(request)
            # user = requests.get_user_by_username(data['username'])
            # update_last_login(None, user)
            print(request.data)
            user = User.objects.get(username=request.data['username'])
            Profile.objects.filter(user__id=user.id) \
                .update(last_login=timezone.now())
        except Exception as exc:
            print(exc)
        return result
