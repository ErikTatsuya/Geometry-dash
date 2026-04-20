import os
import subprocess

def list_and_copy_assets():
    # Caminho da pasta assets
    folder_path = os.path.join(os.path.dirname(__file__), 'assets')
    
    if not os.path.exists(folder_path):
        print(f"ERRO: A pasta '{folder_path}' não existe!")
        return

    # Lista os arquivos
    files = os.listdir(folder_path)
    if not files:
        print("A pasta 'assets' está vazia!")
        return

    # Formata a lista para exibição e cópia
    output = "--- ARQUIVOS ENCONTRADOS NA PASTA ASSETS ---\n"
    output += "\n".join(files)
    
    print(output)

    # Copia para a área de transferência (Windows)
    try:
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(input=output.encode('utf-16'))
        print("\n[SUCESSO] A lista acima foi copiada para sua área de transferência!")
        print("Compare os nomes com o seu dicionário IMAGES no settings.py.")
    except Exception as e:
        print(f"\nErro ao copiar: {e}")

if __name__ == "__main__":
    list_and_copy_assets()