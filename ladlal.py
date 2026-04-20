import subprocess
import pyperclip

# 1. Use 'r' antes da string (raw string) para ignorar as barras invertidas
# 2. Adicione aspas duplas em volta do caminho caso haja espaços (como em 'Nova pasta')
caminho = r'"C:\Users\Daise\Desktop\Nova pasta\python\gd\assets"'
comando = f'dir {caminho}'

# Executa o comando
resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)

# 3. Pega apenas a saída de texto (stdout)
saida = resultado.stdout

# 4. Copia a string para o seu clipboard
pyperclip.copy(saida)

print("Saída do comando copiada para a área de transferência!")
print(saida)