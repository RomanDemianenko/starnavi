from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

User = get_user_model()


class SetLastRequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        user = request.user
        if user.is_authenticated:
            user.last_request = now()
            user.save()

        return response
