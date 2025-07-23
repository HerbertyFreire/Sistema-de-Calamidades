# config.py

import os

# Caminho para o seu arquivo CSV original (usado apenas na criação do DB)
ARQUIVO_CSV_ORIGINAL = r'C:\Users\Livia\Desktop\Sistemade calamidades\Dados\tab_cad_01032025_27_20250408.csv'

# Caminho onde o arquivo do banco de dados SQLite será criado/acessado
# Garante que o DB esteja no mesmo diretório do arquivo CSV original, dentro da pasta 'dados'
# ou ajusta para onde você realmente quer que ele fique.
# Por exemplo, para colocar na mesma pasta do script principal:
# ARQUIVO_DB = 'cadunico.db'
# Ou manter no local original se for o preferido
ARQUIVO_DB = os.path.join(os.path.dirname(ARQUIVO_CSV_ORIGINAL), 'cadunico.db')


TABELA_PRINCIPAL = 'pessoas' # Nome da tabela no banco de dados
USUARIOS_FILE = "usuarios.txt" # Arquivo de credenciais de usuários