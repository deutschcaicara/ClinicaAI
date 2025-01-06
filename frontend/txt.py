import os

def save_frontend_source_code(project_path, output_file):
    # Diretórios e arquivos a excluir
    exclude_dirs = {'node_modules', '.git', 'dist'}
    exclude_extensions = {'.log', '.cache'}
    
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
    # Caminho do frontend e arquivo de saída
    frontend_path = r"C:\ClinicaAI\frontend\src"
    output_file = r"C:\ClinicaAI\codigo_fonte_frontend.txt"
    
    save_frontend_source_code(frontend_path, output_file)
    print(f"Código fonte do frontend salvo em {output_file}")
