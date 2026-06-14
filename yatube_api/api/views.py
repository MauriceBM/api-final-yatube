# yatube_api/api/views.py
from rest_framework import viewsets, filters, mixins, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Comment, Group
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer
)


class PostPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('group',)
    search_fields = ('text',)
    pagination_class = PostPagination

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required to create posts.")
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied(
                "Authentication required to create comments.")
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConditionalLimitOffsetPagination(LimitOffsetPagination):
    default_limit = None
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):
        if 'limit' in request.query_params or 'offset' in request.query_params:
            return super().paginate_queryset(queryset, request, view)
        return None
