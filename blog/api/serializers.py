from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static

from rest_framework import serializers

from blog.models import Comment, Post


User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'is_superuser',
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'url', 'user', 'text', 'created_date', 'approved_comments')

    def get_post(self, obj):
        return obj.post.id
