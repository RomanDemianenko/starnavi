from post.api.views import PostCreateAPIView, PostLikeCreateAPIView, PostLikeDeleteAPIView, \
    PostLikeAnalyticsRetrieveApiView
from django.urls import path

urlpatterns = [
    path('posts/', PostCreateAPIView.as_view(), name='post_create'),
    path('post-likes/', PostLikeCreateAPIView.as_view(), name='post_like_create'),
    path('post-likes/<int:id>/', PostLikeDeleteAPIView.as_view(), name='post_like_delete'),
    path('post-likes/<int:post_id>/analytics/', PostLikeAnalyticsRetrieveApiView.as_view(), name='post_like_analytics'),
]
