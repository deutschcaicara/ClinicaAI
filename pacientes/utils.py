# Arquivo: /mnt/dados/clinicaai/pacientes/utils.py

def calcular_risco(paciente):
    risco = 0

    # Exemplo de cálculo de risco simples, baseado em fatores de saúde
    if paciente.comorbidades_psiquiatricas:
        risco += 2

    if paciente.medicamentos_em_uso:
        risco += 1

    if paciente.tipo_dependencia and paciente.tipo_dependencia.lower() in ['álcool', 'drogas sintéticas']:
        risco += 3

    # Adicionar outras condições relevantes
    if paciente.doencas_preexistentes:
        risco += 2

    # Normalizar a pontuação de risco para ficar em uma escala de 0 a 10
    risco = min(risco, 10)

    return risco
