from django.db import models

from user_profile.models import User


class Post(models.Model):
    author_id = models.IntegerField(db_index=True)
    text = models.TextField(blank=True)


class PostLike(models.Model):
    user_id = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
