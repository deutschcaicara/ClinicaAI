import os

def save_backend_source_code(project_path, output_file):
    # Diretórios e arquivos a excluir
    exclude_dirs = {'.venv', '__pycache__', '.git', 'migrations', 'node_modules'}
    exclude_extensions = {'.pyc', '.log'}
    
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(project_path):
            # Remove diretórios a excluir da iteração
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # Ignorar arquivos com extensões irrelevantes
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue
                
                # Caminho completo do arquivo
                file_path = os.path.join(root, file)
                
                try:
                    # Ler e salvar o conteúdo do arquivo
                    with open(file_path, 'r', encoding='utf-8') as f:
                        output.write(f"### {file_path} ###\n")
                        output.write(f.read())
                        output.write("\n\n")
                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")

if __name__ == "__main__":
    # Caminho do backend e arquivo de saída
    backend_path = r"C:\ClinicaAI\backend"
    output_file = r"C:\ClinicaAI\codigo_fonte_backend.txt"
    
    save_backend_source_code(backend_path, output_file)
    print(f"Código fonte do backend salvo em {output_file}")
