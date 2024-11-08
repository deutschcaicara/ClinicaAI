import os


def listar_arquivos(caminho):
    """Lista todos os arquivos em um diretório e subdiretórios."""
    with open("lista_arquivos.txt", "w") as arquivo_saida:
        for root, _, files in os.walk(caminho):
            for file in files:
                arquivo_saida.write(os.path.join(root, file) + "\n")


if __name__ == "__main__":
    listar_arquivos("/mnt/dados/ClinicaAI/backend/apps/")
    listar_arquivos("/mnt/dados/ClinicaAI/backend/ClinicaAI")
