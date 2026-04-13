# config.py

import os
import glob

BASE_DIR = os.path.dirname(__file__)
DADOS_DIR = os.path.join(BASE_DIR, "dados")

# Busca automaticamente o arquivo de dados tab_cad_* mais recente em dados/.
csv_files = glob.glob(os.path.join(DADOS_DIR, "tab_cad_*.csv"))
if csv_files:
    csv_files.sort(key=os.path.getmtime, reverse=True)
    ARQUIVO_CSV_ORIGINAL = csv_files[0]
else:
    ARQUIVO_CSV_ORIGINAL = os.path.join(DADOS_DIR, "tab_cad_01032025_27_20250408.csv")

# Caminho onde o arquivo do banco de dados SQLite será criado/acessado
ARQUIVO_DB = os.path.join(DADOS_DIR, 'cadunico.db')

TABELA_PRINCIPAL = 'pessoas' # Nome da tabela no banco de dados
USUARIOS_FILE = "usuarios.txt" # Arquivo de credenciais de usuários
