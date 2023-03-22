from django.contrib.auth import authenticate, get_user_model
from django.utils.timezone import now
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user_profile.api.serialzers import UserCreateSerializer, UserAuthSerializer, UserActivitySerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = UserCreateSerializer


class UserAuthenticationAPIView(APIView):
    permission_classes = ()
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response(
                {'error': 'Username or password is incorrect'},
                status=HTTP_400_BAD_REQUEST
            )
        user.last_login = now()
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                **self.serializer_class(user).data
            }
        )


class UserActivityRetrieveApiView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserActivitySerializer
    queryset = User.objects.all()
    lookup_field = 'id'
