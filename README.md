# Orion_bank
Orion BANK, banco dogital utilizando python e flask 



Para configurar e executar o projeto, siga os passos abaixo:
Pré-requisitos
Python 3.x
pip (gerenciador de pacotes do Python)
Instalação
Clone o repositório:
git clone [LINK_DO_REPOSITORIO]
cd orion-digital-bank


Crie e ative um ambiente virtual (Recomendado):
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows


Instale as dependências:
pip install Flask werkzeug bcrypt


Configure o Super Admin Inicial:
Execute o script de configuração inicial. Isso criará o arquivo users.json com as credenciais do administrador.
python setup_admin.py


Execução
Inicie o servidor Flask:
python app.py


Acesse a Aplicação:
Abra seu navegador e navegue para: http://127.0.0.1:5000
Credenciais de Teste
Perfil
E-mail
Senha
Rota de Acesso
Super Admin
admin@orion.com
admin123
/admin/dashboard
Usuário Comum
Registre um novo
Sua senha
/dashboard

