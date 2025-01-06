from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def dashboard_data(request):
    data = {
        "cards": [
            {"title": "Pacientes Ativos", "value": 25},
            {"title": "Agendamentos do Dia", "value": 15},
            {"title": "Exames Pendentes", "value": 7},
        ]
    }
    return Response(data)
