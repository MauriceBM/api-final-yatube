# yatube_api/api/serializers.py
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'post', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username',
                            read_only=True, required=False)
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            current_user = request.user

            if current_user == data.get('following'):
                raise serializers.ValidationError({
                    "following": "Вы не можете подписаться на самого себя."
                })

            if Follow.objects.filter(user=current_user,
                                     following=data['following']).exists():
                raise serializers.ValidationError({
                    "following": "Вы уже подписаны на этого пользователя."
                })

        return data
