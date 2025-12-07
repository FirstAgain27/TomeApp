from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer
    
    )
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user" : UserProfileSerializer(user).data,
            "resfresh" : str(refresh),
            "access" : str(refresh.access_token),
            "message" : "Регистрация успешна!"
        }, status=status.HTTP_201_CREATED)

