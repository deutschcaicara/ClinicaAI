import requests

# Configurações
base_url = "http://127.0.0.1:8000/api"
login_url = f"{base_url}/auth/token/"
pacientes_url = f"{base_url}/pacientes/"
username = "diego"
password = "Mouse2250@#86"

# Fazer login e obter o token
login_response = requests.post(login_url, json={"username": username, "password": password})
login_data = login_response.json()
access_token = login_data.get("access")

if not access_token:
    print("Erro ao obter o token de acesso.")
    exit()

# Usar o token para obter os dados dos pacientes
headers = {"Authorization": f"Bearer {access_token}"}
pacientes_response = requests.get(pacientes_url, headers=headers)

if pacientes_response.status_code == 200:
    pacientes_data = pacientes_response.json()
    print("Dados dos pacientes:", pacientes_data)
else:
    print("Erro ao obter os dados dos pacientes:", pacientes_response.status_code)