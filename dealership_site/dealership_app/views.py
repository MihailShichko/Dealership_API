from bisect import insort

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models.car import Car
# from .models.user import DealershipUser
from .permissions.permissions import IsAdminOrReadOnly
from .serializers.car_serializer import CarReadSerializer, CarWriteSerializer

from .serializers.register_serializer import RegisterSerializer

def notification_view(request):
    return render(request, 'notification_template.html')

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'car_notifications',
            {
                'type': 'car_posted',
                'car_data': serializer.data
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CarReadSerializer
        return CarWriteSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#
# class LogoutSerializer:
#     pass



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            205: "Success: Token blacklisted",
            400: "Bad Request: Error occurred"
        },
        operation_description="blacklist a refresh token and log the user out"
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"success": "Token blacklisted successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": f"Error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
