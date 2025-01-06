import os

# Caminho base para o projeto (ajuste conforme necessário)
base_path = "C:\\ClinicaAI\\frontend"

# Estrutura de pastas e arquivos
estrutura = {
    "src": {
        "components": {
            "atoms": {},
            "molecules": {},
            "organisms": {}
        },
        "pages": {
            "login": {"index.jsx": "", "styles.css": ""},
            "dashboard": {"index.jsx": "", "styles.css": ""},
            "agendamentos": {"index.jsx": "", "styles.css": ""}
        },
        "layouts": {
            "MainLayout.jsx": "",
            "Header.jsx": "",
            "Footer.jsx": ""
        },
        "services": {
            "api.js": "// Aqui ficam as funções de chamada à API"
        },
        "assets": {
            "images": {},
            "fonts": {}
        },
        "styles": {
            "globals.css": "/* Estilos globais */",
            "itcss": {
                "_settings.css": "/* Configurações globais */",
                "_tools.css": "/* Ferramentas utilitárias */",
                "_components.css": "/* Componentes reutilizáveis */"
            }
        },
        "utils": {
            "helpers.js": "// Funções auxiliares",
            "constants.js": "// Constantes globais"
        },
        "index.jsx": "// Ponto de entrada do React",
        "App.jsx": "// Componente principal",
        "App.css": "/* Estilos do App */"
    }
}

# Função para criar as pastas e arquivos
def criar_estrutura(base, estrutura):
    for nome, conteudo in estrutura.items():
        caminho = os.path.join(base, nome)
        if isinstance(conteudo, dict):
            os.makedirs(caminho, exist_ok=True)
            criar_estrutura(caminho, conteudo)
        else:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)

# Criar a estrutura no caminho base
criar_estrutura(base_path, estrutura)
print(f"Estrutura de pastas e arquivos criada em: {base_path}")
