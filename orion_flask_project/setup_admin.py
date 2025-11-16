import json
import os
# Importa a função de hashing do Werkzeug para uniformizar a geração de hash
from werkzeug.security import generate_password_hash

# Dados do Super Admin
SUPER_ADMIN_EMAIL = "admin@orion.com"
ADMIN_PASSWORD_RAW = "admin123"

# 1. Gerar o hash da senha usando Werkzeug
# Isso garante que o hash será gerado no formato que check_password_hash espera.
hashed_password = generate_password_hash(ADMIN_PASSWORD_RAW)

# 2. Criar a estrutura inicial do arquivo users.json
admin_data = {
    "email": SUPER_ADMIN_EMAIL,
    # Chave 'senha' com o hash gerado pelo Werkzeug
    "senha": hashed_password,
    "nome": "Orion Super Admin",
    "cpf": "00000000000",
    "is_admin": True,
    "saldo": 1000000.00,
    "contas_ativas": 5,
    "transactions": [] # Incluído para evitar erros no app.py
}

# 3. Salvar no users.json
USERS_FILE = 'users.json'
try:
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        # Sobrescreve o arquivo com a nova estrutura de hash
        json.dump({"super_admin": admin_data}, f, ensure_ascii=False, indent=4)
    print(f"✅ Arquivo '{USERS_FILE}' criado/atualizado com sucesso para o Super Admin.")
    print(f"   Credenciais de Login: Email: {SUPER_ADMIN_EMAIL}")
    print(f"   Senha: {ADMIN_PASSWORD_RAW} (HASH WERKZEUG)")

except IOError as e:
    print(f"❌ Erro ao escrever no arquivo {USERS_FILE}: {e}")