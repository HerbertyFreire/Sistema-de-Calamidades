# auth.py

import hashlib
import os
from config import USUARIOS_FILE # Importar o caminho do arquivo de usuários

def criar_arquivo_usuarios():
    """
    Cria o arquivo de usuários se não existir, com credenciais padrão.
    Movida de 'Codigo.py'.
    """
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "w", encoding='utf-8') as f:
            senha_admin = hashlib.sha256("admin123".encode()).hexdigest()
            f.write(f"admin:{senha_admin}:Administrador:2\n")
            senha_user = hashlib.sha256("user123".encode()).hexdigest()
            f.write(f"user:{senha_user}:Usuário Padrão:1\n")

def verificar_login(username, password):
    """
    Verifica as credenciais do usuário.
    Movida de 'Codigo.py'.
    """
    criar_arquivo_usuarios()
    try:
        with open(USUARIOS_FILE, "r", encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(":")
                if len(partes) == 4 and partes[0] == username:
                    senha_hash = hashlib.sha256(password.encode()).hexdigest()
                    if partes[1] == senha_hash:
                        return True, partes[2], int(partes[3])
    except Exception as e:
        print(f"Erro ao verificar login: {str(e)}")
    return False, "", 0