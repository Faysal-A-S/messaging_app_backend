from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserSerializeer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

# Create your views here.


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializeer(data=request.data
                                     )
        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": True, "message": "User registered successfully", "result": {
                "id": user.id,
                "username": user.username
            }})
        return Response({
            "success": False,
            "message": "Registration failed",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username").strip()
        password = serializer.validated_data.get("password").strip()
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "User login successful",
                "result": {
                    "access_token": str(refresh.access_token),
                    "id": user.id,
                    "username": user.username
                },

            }, status=status.HTTP_200_OK,)

        return Response({
            "success": False,
            "message": "User unauthorized",
            "error": serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED,)


class Userlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("user", "")
        users = User.objects.filter(
            username__icontains=query).order_by("username")
        serializer = UserSerializeer(users, many=True)

        return Response({
            "message": "user fetched successfully",
            "result": serializer.data,
            "success": True
        }, status=status.HTTP_200_OK)
