from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from post.models import Post, PostLike


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author_id',
        )
        extra_kwargs = {
            'author_id': {'write_only': True},
        }


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'id',
            'post',
            'user_id',
        )
        extra_kwargs = {
            'user_id': {'write_only': True},
        }


class PostLikeAnalyticsSerializer(Serializer):
    number_of_likes = IntegerField()
