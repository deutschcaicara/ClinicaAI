from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Endpoint para login
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# Endpoint para logout esse comentado funciona com o pacote rest_framework_simplejwt
#class LogoutView(APIView):
#    def post(self, request):
#        try:
#            # Opcional: implementar lógica de invalidação de token
#            return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
#        except Exception as e:
#            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  # Recupera o token de refresh do payload
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Adiciona o token à lista negra
            return Response({"message": "Logout realizado com sucesso"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)