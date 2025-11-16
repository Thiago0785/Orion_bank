import json
import os
from bcrypt import hashpw, checkpw, gensalt

# ----------------------------------------------------------------------
# Configurações de Dados e Segurança
# ----------------------------------------------------------------------

# Nome do arquivo que irá armazenar os dados de usuários (simulando um DB)
USERS_FILE = 'users.json' 
# Credenciais iniciais do Super Admin (para o primeiro uso)
INITIAL_ADMIN_EMAIL = 'admin@orion.com'
INITIAL_ADMIN_PASSWORD = 'admin123'
# Gera um salt (semente) aleatório para o hash da senha inicial
INITIAL_SALT = gensalt() 

# ----------------------------------------------------------------------
# Funções Auxiliares de Persistência
# ----------------------------------------------------------------------

def _load_users():
    """Carrega todos os dados de usuários do arquivo JSON."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Retorna um dicionário vazio se o arquivo estiver vazio ou corrompido
        return {}

def _save_users(users):
    """Salva o dicionário de usuários de volta ao arquivo JSON."""
    try:
        with open(USERS_FILE, 'w') as f:
            # Usamos indent=4 para facilitar a leitura do JSON
            json.dump(users, f, indent=4)
        return True
    except IOError:
        print(f"ERRO: Não foi possível escrever no arquivo {USERS_FILE}.")
        return False

# ----------------------------------------------------------------------
# Funções de Serviço para o Backend
# ----------------------------------------------------------------------

def setup_initial_admin():
    """
    Garante que o arquivo de usuários exista e contenha o Super Admin inicial
    se ele ainda não tiver sido criado.
    """
    users = _load_users()

    # Verifica se o admin inicial já está presente na base de dados
    if INITIAL_ADMIN_EMAIL not in users:
        # Codifica a senha em bytes e a hash com o salt gerado
        hashed_password = hashpw(
            INITIAL_ADMIN_PASSWORD.encode('utf-8'), 
            INITIAL_SALT
        ).decode('utf-8') # Decodifica de volta para string para salvar no JSON

        users[INITIAL_ADMIN_EMAIL] = {
            'email': INITIAL_ADMIN_EMAIL,
            'password_hash': hashed_password,
            'role': 'super_admin'  # Define o papel como Super Admin
        }
        _save_users(users)
        print(f"INFO: Super Admin inicial '{INITIAL_ADMIN_EMAIL}' configurado com a senha padrão 'admin123'.")
    else:
        print(f"INFO: O Super Admin inicial já existe.")


def authenticate_admin(email, password):
    """
    Verifica se o email existe e se a senha corresponde ao hash armazenado.
    Permite login apenas para contas com o papel 'super_admin'.
    """
    users = _load_users()
    user_data = users.get(email)

    # 1. Verifica se o usuário existe
    if not user_data:
        return None

    # 2. Verifica se o papel é 'super_admin' (somente Super Admin pode acessar o dashboard)
    if user_data.get('role') != 'super_admin':
        return None
    
    # 3. Verifica a senha
    stored_hash = user_data['password_hash'].encode('utf-8')
    password_bytes = password.encode('utf-8')

    # A função checkpw faz o hashing da senha fornecida e compara com o hash armazenado
    if checkpw(password_bytes, stored_hash):
        # Retorna os dados do usuário se a autenticação for bem-sucedida
        return {'email': user_data['email'], 'role': user_data['role']}
    
    return None # Retorna None se a senha estiver incorreta


def get_system_stats():
    """
    Retorna dados simulados para as estatísticas do dashboard.
    Esta função seria o ponto de integração com um banco de dados real.
    """
    return {
        'total_users': 1540000,
        'active_accounts': 1200000,
        'transactions_last_24h': 450000,
        'total_balance_brl': 123456789.00,
        'user_growth_rate': '+1.5%',
        'service_status': 'Operacional'
    }


def delete_admin_account(email, password):
    """
    Exclui a conta do Super Admin logado após verificar a senha.
    """
    users = _load_users()
    user_data = users.get(email)

    if not user_data or user_data.get('role') != 'super_admin':
        return False, "Conta Super Admin não encontrada."

    # 1. Verifica a senha antes de excluir
    stored_hash = user_data['password_hash'].encode('utf-8')
    password_bytes = password.encode('utf-8')

    if not checkpw(password_bytes, stored_hash):
        return False, "Senha incorreta. Não foi possível excluir a conta."
    
    # 2. Exclui a conta
    del users[email]
    
    # 3. Garante que sempre haja um admin inicial reconfigurando-o
    # Isso evita que o sistema fique sem um Super Admin
    if not users:
        setup_initial_admin()
        return True, "Sua conta foi excluída com sucesso! Uma nova conta admin@orion.com (senha admin123) foi recriada para garantir o acesso ao sistema."
    else:
        _save_users(users)
        return True, "Sua conta foi excluída com sucesso."

# A função setup_initial_admin() é chamada no app.py para garantir
# que o Super Admin inicial seja configurado ao iniciar o servidor.