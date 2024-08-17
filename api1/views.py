from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BasicResponseSerializer

class HomeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message": "Redirecting to authenticated home"}, status=status.HTTP_200_OK)
        return Response({"message": "Welcome to Ivory Hospital - Home"}, status=status.HTTP_200_OK)

class AboutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Ivory Hospital - About Us"}, status=status.HTTP_200_OK)

class ServicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Ivory Hospital - Our Services"}, status=status.HTTP_200_OK)

class ContactView(APIView):
    def get(self, request):
        return Response({"message": "Ivory Hospital - Contact Us"}, status=status.HTTP_200_OK)
