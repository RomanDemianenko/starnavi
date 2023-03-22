from django.db.models import Q
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from post.api.serialzers import PostCreateSerializer, PostLikeSerializer, PostLikeAnalyticsSerializer
from post.models import PostLike


class PostCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCreateSerializer

    def post(self, request, *args, **kwargs):
        request.data['author_id'] = request.user.id
        return super().post(request, *args, **kwargs)


class PostLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLikeSerializer

    def post(self, request, *args, **kwargs):
        request.data['user_id'] = request.user.id
        return super().post(request, *args, **kwargs)


class PostLikeDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'

    def get_queryset(self):
        return PostLike.objects.filter(user_id=self.request.user.id)


class PostLikeAnalyticsRetrieveApiView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLikeAnalyticsSerializer
    queryset = PostLike.objects.all()
    lookup_field = 'post_id'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = self.get_queryset().filter(post_id=post_id)

        date_range = Q()
        if start_date:
            date_range &= Q(created_at__gte=start_date)
        if end_date:
            date_range &= Q(created_at__lte=end_date)
        if date_range:
            queryset = queryset.filter(date_range)

        number_of_likes = queryset.distinct().count()
        return {'number_of_likes': number_of_likes}

