from user_profile.api.views import UserCreateAPIView, UserAuthenticationAPIView, UserActivityRetrieveApiView
from django.urls import path

urlpatterns = [
    path('users/registration/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/auth/', UserAuthenticationAPIView.as_view(), name='user_auth'),
    path('users/<int:id>/activity/', UserActivityRetrieveApiView.as_view(), name='user_activity'),
]
