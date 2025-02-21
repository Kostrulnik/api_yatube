from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    UserSerializer,
)



class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления постами (CRUD-операции).

    Только автор поста может редактировать или удалять его.
    Создание поста автоматически связывает его с текущим пользователем.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Автоматически привязывает автора к текущему пользователю."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения информации о конкретной группе."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями к постам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post_id(self):
        """Возвращает ID поста из параметров запроса."""
        return self.kwargs.get("post_id")

    def get_queryset(self):
        """Возвращает все комментарии для конкретного поста."""
        post = get_object_or_404(Post, id=self.get_post_id())
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Создаёт комментарий и автоматически привязывает его
        к текущему пользователю и соответствующему посту.
        """
        post = get_object_or_404(Post, id=self.get_post_id())
        serializer.save(author=self.request.user, post=post)
