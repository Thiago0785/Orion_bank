import json
import os
import uuid
from functools import wraps
from datetime import datetime, timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- Configuração Inicial do Flask ---
app = Flask(__name__)
# Chave secreta obrigatória para sessões e mensagens flash
# Mantenha esta chave secreta!
app.secret_key = "uma_chave_secreta_muito_segura_e_longa"
USERS_FILE = "users.json"


# --- Funções de Manipulação de Dados (Simulação de DB) ---


def load_users():
    """Carrega dados dos usuários do arquivo JSON."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users_data):
    """Salva dados dos usuários no arquivo JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=4)


def get_user_data(user_id):
    """Obtém dados de um usuário específico ou admin."""
    users = load_users()
    return users.get(user_id)


def get_system_stats():
    """
    NOVA FUNÇÃO: Calcula estatísticas do sistema a partir do users.json.
    """
    users = load_users()
    total_users = 0
    total_balance = 0.0
    transactions_count = 0
    
    # Lista para armazenar dados resumidos de usuários (para tabela)
    user_list = []

    for user_id, user_data in users.items():
        if user_id == "super_admin":
            continue  # Ignora o admin nos totais de usuários normais
            
        total_users += 1
        
        # Flexibilidade nas chaves de saldo e transações
        balance_key = "balance" if "balance" in user_data else "saldo"
        transactions_key = "transactions" if "transactions" in user_data else "historico"
        
        user_balance = user_data.get(balance_key, 0.0)
        total_balance += user_balance
        
        user_transactions = user_data.get(transactions_key, [])
        transactions_count += len(user_transactions)
        
        user_list.append({
            "id": user_id[:4] + "...", # ID parcial
            "nome": user_data.get("nome", "N/A"),
            "email": user_data.get("email", "N/A"),
            "cpf": user_data.get("cpf", "N/A"),
            "balance": f"R$ {user_balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "transactions_count": len(user_transactions)
        })

    # Estatísticas de exemplo para o card
    active_accounts = int(total_users * 0.8) # Simulação de contas ativas
    
    return {
        "total_users": total_users,
        "active_accounts": active_accounts,
        "total_balance_brl": total_balance,
        "transactions_last_24h": int(transactions_count / 10), # Simulação
        "user_list": user_list
    }


# --- Decoradores de Autenticação ---


def login_required(f):
    """Decorador que verifica se o usuário está logado."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar esta página.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorador que verifica se o usuário logado é um administrador."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session["user_id"] != "super_admin":
            flash("Acesso negado. Apenas administradores podem acessar esta página.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


# --- ROTAS PRINCIPAIS ---


@app.route("/")
def index():
    """Rota da página inicial (Login/Cadastro)."""
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Rota do painel do usuário comum."""
    user_id = session.get("user_id")
    user = get_user_data(user_id)
    if user:
        # Passa o nome para ser exibido no dashboard
        return render_template("dashboard.html", user_name=user.get("nome"))
    flash("Sessão inválida ou usuário não encontrado.", "error")
    return redirect(url_for("index"))


@app.route("/admin_dashboard")
@admin_required
def admin_dashboard():
    """Rota do painel do administrador."""
    user_id = session.get("user_id")
    user = get_user_data(user_id)
    if user:
        # Passa o nome e uma mensagem (opcional)
        return render_template("admin_dashboard.html", 
                               admin_name=user.get("nome"),
                               admin_message="Este é o painel de controle do Super Admin.")
    
    flash("Sessão inválida ou administrador não encontrado.", "error")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    """Rota de logout."""
    session.pop("user_id", None)
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for("index"))


@app.route("/register", methods=["POST"])
def register():
    """Rota para processar o cadastro de novos usuários."""
    # Garante que os dados vieram de um formulário HTML
    if not request.form:
        flash("Erro: O formulário de registro não enviou dados válidos.", "error")
        return redirect(url_for("index"))

    # 1. Coleta de dados
    nome = request.form.get("register_name")
    cpf = request.form.get("register_cpf")
    email = request.form.get("register_email")
    password = request.form.get("register_password")

    users = load_users()

    # 2. Validação de dados
    if not all([nome, cpf, email, password]):
        flash("Todos os campos de cadastro são obrigatórios.", "error")
        return redirect(url_for("index"))

    # Verifica se CPF ou Email já existem
    for user_id, user_data in users.items():
        if user_id != "super_admin" and (user_data.get("cpf") == cpf or user_data.get("email") == email):
            flash("CPF ou Email já cadastrado. Tente fazer login.", "error")
            return redirect(url_for("index"))

    # 3. Criação e salvamento
    user_id = uuid.uuid4().hex  # Gera um ID único para o usuário
    new_user = {
        "email": email,
        "password_hash": generate_password_hash(password),
        "nome": nome,
        "cpf": cpf,
        "is_admin": False,
        "balance": 1000.00,  # Saldo inicial
        "transactions": [],
    }

    users[user_id] = new_user
    save_users(users)

    flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    """Rota para processar o login."""
    if not request.form:
        flash("Erro: O formulário de login não enviou dados válidos.", "error")
        return redirect(url_for("index"))

    # 1. Coleta de dados
    login_id = request.form.get("login_id")  # Pode ser CPF ou Email
    password = request.form.get("password")

    users = load_users()
    user_id = None
    user_found = None

    # 2. Busca o usuário
    # Checa primeiro pelo super_admin (chave 'super_admin') por EMAIL ou CPF
    admin_data = users.get("super_admin")
    if admin_data and (admin_data.get("email") == login_id or admin_data.get("cpf") == login_id):
        user_id = "super_admin"
        user_found = admin_data
    else:
        # Busca por CPF ou Email em usuários normais
        for uid, user_data in users.items():
            # A VERIFICAÇÃO DE SEGURANÇA CHAVE: Garante que o usuário não é o admin
            if uid != "super_admin" and user_data.get("is_admin") is not True and ( 
                user_data.get("email") == login_id or user_data.get("cpf") == login_id
            ):
                user_id = uid
                user_found = user_data
                break

    # 3. Autenticação: Tenta 'senha' para admin, 'password_hash' para usuários normais
    password_hash_key = "senha" if user_id == "super_admin" else "password_hash"

    if user_found and password_hash_key:
        stored_hash = user_found.get(password_hash_key)

        if not stored_hash:
             flash("Erro: Dados de senha do usuário incompletos.", "error")
             return redirect(url_for("index"))
        
        # Verifica a senha
        if check_password_hash(stored_hash, password):
            session["user_id"] = user_id

            # Redirecionamento correto: Se user_id for 'super_admin', vai para o Admin.
            if user_id == "super_admin":
                flash("Login de Administrador realizado com sucesso!", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("dashboard"))

    # 4. Falha na autenticação
    flash("Credenciais inválidas. Verifique seu CPF/Email e senha.", "error")
    return redirect(url_for("index"))
# --- ROTAS DA API (Dashboard) ---


@app.route("/api/user_data", methods=["GET"])
@login_required
def api_user_data():
    """API para obter dados dinâmicos do usuário no Dashboard."""
    user_id = session["user_id"]
    user = get_user_data(user_id)

    if user_id == "super_admin" or not user:
        return jsonify({"success": False, "message": "Usuário não autorizado ou não encontrado."}), 404

    # Prepara os dados para o frontend
    transactions_for_api = []
    
    # Assegura que a lista de transações existe
    if 'transactions' in user:
        # Adiciona o ID da transação (para futuras operações de detalhe, se necessário)
        # E formata a descrição para a tabela
        transactions_for_api = [
            {
                "id": t.get("id", str(uuid.uuid4())),
                "type": t["type"],
                "amount": t["amount"],
                "date": t["timestamp"],
                "recipient_name": t.get("recipient_name", t.get("sender_name", "Desconhecido")),
                # Adiciona flags para a lógica de exibição no Jinja2
                "is_credit": t["type"] == "received", 
                "description": f"PIX Enviado para {t.get('recipient_name', 'N/A')}" if t["type"] == "sent" else f"PIX Recebido de {t.get('sender_name', 'N/A')}",
            }
            for t in user.get("transactions", [])
        ]
        
    # Limita e reverte a ordem para mostrar as mais recentes primeiro
    # Nota: Ordenar por timestamp (string) funciona se o formato for YYYY-MM-DD HH:MM:SS
    recent_transactions = sorted(transactions_for_api, key=lambda x: x['date'], reverse=True)[:5]


    return jsonify(
        {
            "success": True,
            "nome": user.get("nome"),
            "email": user.get("email"),
            "balance": user.get("balance", user.get("saldo", 0.0)), # Flexibilidade na chave de saldo
            "transactions": recent_transactions,
        }
    )


@app.route("/api/transfer", methods=["POST"])
@login_required
def api_transfer():
    """API para realizar transferência bancária."""
    user_id = session["user_id"]
    
    if not request.json:
        return jsonify({"success": False, "message": "Dados da transferência ausentes."}), 400
        
    data = request.json
    # O campo do formulário é 'receiver_cpf', mas a rota espera 'recipient_id' para ser genérica
    recipient_id = data.get("receiver_cpf") 
    amount_str = data.get("amount")
    
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Valor da transferência inválido."}), 400
        
    if amount <= 0:
        return jsonify({"success": False, "message": "O valor deve ser positivo."}), 400

    users = load_users()
    sender = users.get(user_id)
    recipient_found = None
    recipient_key = None

    if not sender or user_id == "super_admin":
        return jsonify({"success": False, "message": "Remetente inválido ou não autorizado."}), 403

    # 1. Busca o destinatário (por CPF ou Email)
    for key, user_data in users.items():
        if key != "super_admin" and (
            user_data.get("cpf") == recipient_id
            or user_data.get("email") == recipient_id
        ):
            recipient_found = user_data
            recipient_key = key
            break

    if not recipient_found:
        return jsonify({"success": False, "message": "Destinatário não encontrado."}), 404
        
    if sender["cpf"] == recipient_found["cpf"]:
        return jsonify({"success": False, "message": "Você não pode transferir para si mesmo."}), 400

    # 2. Validação de Saldo
    sender_balance_key = "balance" if "balance" in sender else "saldo"
    if sender.get(sender_balance_key, 0.0) < amount:
        return jsonify({"success": False, "message": "Saldo insuficiente para esta transação."}), 400

    # 3. Realiza a Transação
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Debita do Remetente
        sender[sender_balance_key] -= amount
        
        # Credita no Destinatário
        recipient_balance_key = "balance" if "balance" in recipient_found else "saldo"
        recipient_found[recipient_balance_key] += amount
        
        # Registra Transação para o Remetente
        sender["transactions"].append({
            "id": uuid.uuid4().hex,
            "type": "sent",
            "amount": amount, # Guarda o valor positivo, o type 'sent' indica débito
            "timestamp": now,
            "recipient_name": recipient_found.get("nome", "Conta Externa"),
            "recipient_id": recipient_key
        })

        # Registra Transação para o Destinatário
        recipient_found["transactions"].append({
            "id": uuid.uuid4().hex,
            "type": "received",
            "amount": amount,
            "timestamp": now,
            "sender_name": sender.get("nome", "Conta Externa"),
            "sender_id": user_id
        })
        
        # Salva as alterações
        users[user_id] = sender
        users[recipient_key] = recipient_found
        save_users(users)
        
        return jsonify({
            "success": True, 
            "message": "Transferência realizada com sucesso!",
            "new_balance": sender[sender_balance_key]
        })

    except Exception as e:
        app.logger.error(f"Erro na transferência: {e}")
        return (
            jsonify({"success": False, "message": "Erro interno ao processar transferência."}),
            500,
        )


@app.route("/api/admin_stats", methods=["GET"])
@admin_required
def api_admin_stats():
    """
    NOVA ROTA: API para obter estatísticas do sistema no Dashboard do Admin.
    """
    stats = get_system_stats()
    return jsonify({"success": True, "stats": stats})
    
# Rota para exclusão de conta (mantida)
@app.route("/api/delete-account", methods=["POST"])
@login_required
def api_delete_account():
    """API para exclusão de conta."""
    user_id = session["user_id"]
    data = request.json
    password = data.get("senha")

    users = load_users()
    user_to_delete = users.get(user_id)

    if not user_to_delete:
        session.pop("user_id", None)
        return jsonify({"success": False, "message": "Sessão expirada. Faça login novamente."}), 401

    # 1. Validação da senha
    hash_key = "senha" if user_id == "super_admin" else "password_hash"
    
    if not check_password_hash(user_to_delete.get(hash_key, ''), password):
        return jsonify({"success": False, "message": "Senha incorreta. Exclusão cancelada."}), 401

    # 2. Exclusão
    try:
        del users[user_id]
        save_users(users)
        session.pop("user_id", None)
        return jsonify({"success": True, "message": "Conta excluída com sucesso."})
    except Exception as e:
        app.logger.error(f"Erro ao deletar conta: {e}")
        return jsonify({"success": False, "message": "Erro interno ao deletar conta."}), 500