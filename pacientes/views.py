from django.shortcuts import render

# Arquivo: /mnt/dados/clinicaai/pacientes/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Paciente
from .serializers import PacienteSerializer
from .utils import calcular_risco
from .models.consulta import Consulta
from .models.exame import Exame
from .serializers import ConsultaSerializer, ExameSerializer

class PacienteAPIView(APIView):
    def post(self, request):
        # Serializa os dados do paciente
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            # Salva os dados do paciente
            paciente = serializer.save()

            # Calcula a análise de risco
            risco = calcular_risco(paciente)

            # Atualiza o campo de análise de risco do paciente
            paciente.analise_risco = risco
            paciente.save()

            return Response(PacienteSerializer(paciente).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ConsultaAPIView(APIView):
    def get(self, request):
        consultas = Consulta.objects.all()
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsultaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExameAPIView(APIView):
    def get(self, request):
        exames = Exame.objects.all()
        serializer = ExameSerializer(exames, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)