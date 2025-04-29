from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ModuleInstance, Professor, Rating
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import (
    ModuleInstanceSerializer, ProfessorRatingSerializer,
    AverageRatingSerializer, RatingSerializer, RegisterSerializer, LoginSerializer
)
import logging
# Set up logging
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class ModuleInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleInstance.objects.all()
    serializer_class = ModuleInstanceSerializer
    permission_classes = []  # Public access

class ProfessorRatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorRatingSerializer
    permission_classes = []  # Public access

class AverageRatingView(APIView):
    permission_classes = []

    def get(self, request):
        professor_id = request.query_params.get('professor_id')
        module_code = request.query_params.get('module_code')
        
        if not (professor_id and module_code):
            return Response(
                {"error": "Both professor_id and module_code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {'professor_id': professor_id, 'module_code': module_code}
        serializer = AverageRatingSerializer(data = data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)