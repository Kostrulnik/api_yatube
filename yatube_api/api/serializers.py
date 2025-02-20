from rest_framework import serializers
from posts.models import Comment, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Поля:
    group: Использует SlugRelatedField для связи по slug.
    author: Только для чтения, отображает имя автора.
    """
    group = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Group.objects.all(),
                                         required=False)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Поля:
    id: Уникальный идентификатор группы.
    title: Название группы.
    slug: Уникальный slug группы.
    description: Описание группы.
    """
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Поля:
    first_name: Имя пользователя.
    last_name: Фамилия пользователя.
    username: Уникальное имя пользователя.
    email: Электронная почта (обязательное поле).
    password: Пароль (скрыт в ответах API).
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    def create(self, validated_data):
        """Создаёт пользователя с хешированным паролем"""
        user = User.objects.create_user(**validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Поля:
    id: Уникальный идентификатор комментария.
    author: Только для чтения, отображает имя автора.
    post: ID связанного поста (только для чтения, передаётся в URL).
    text: Текст комментария.
    created: Дата и время создания комментария.
    """
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
