Orion: O Banco Digital do Futuro 

🌌 Visão Geral

Orion não é apenas um sistema financeiro, é uma prova de conceito de Arquitetura Full-Stack que simula um Banco Digital de Alto Desempenho, focado em segurança, usabilidade e uma experiência de usuário impecável.
Este projeto demonstra a criação de uma aplicação robusta com autenticação de múltiplos perfis (Usuário Comum e Super Admin), gerenciamento de transações em tempo real e um dashboard administrativo para monitoramento de métricas críticas.

🛠️ Stack Tecnológico:
A espinha dorsal do Orion é construída com tecnologias modernas e confiáveis, garantindo velocidade e estabilidade.
Detalhe de Implementação: 
Backend - 
Python 🐍 (Flask):
* Micro-framework leve, ideal para roteamento rápido e APIs de serviço.

* Segurança

* werkzeug.security & bcrypt

* Hashing robusto de senhas, garantindo que credenciais NUNCA sejam armazenadas em texto simples.

🛠️ Frontend :
* HTML5, JavaScript (Vanilla)
 
* Lógica de interação client-side, chamadas assíncronas (fetch) e manipulação de modais.

* Estilização

* Tailwind CSS

* Design Dark Mode responsivo, moderno e minimalista, focado na marca Orion (cores neon/verde).

* Simulação de DB

* Arquivos .json

* Persistência de dados de usuários e transações para simular o estado do sistema em tempo de execução.

🌟 Funcionalidades de Alto Impacto: 
-O Orion oferece dois painéis de controle distintos, cada um protegido por rigorosos mecanismos de autenticação.
* 👤 Módulo do Usuário Comum (/dashboard)

* Autenticação Segura: Cadastro, Login e Logout protegidos por sessão e criptografia.

* Controle Financeiro em Tempo Real: Visualização dinâmica do saldo e histórico de transações.

* Transferências (Simulação PIX/TED): Funcionalidade para enviar fundos a outros usuários cadastrados via CPF, com validação de saldo instantânea.

* Recurso de Segurança Máxima: Opção de Exclusão de Conta, exigindo re-confirmação de senha para garantir que apenas o proprietário possa encerrar o acesso.

🛡️ Módulo de Super Admin (/admin/dashboard);
Acesso Restrito: Rota isolada, acessível apenas pelo Super Admin, protegido por decorators de autenticação de perfil.

- Monitoramento de KPIs: Dashboard dedicado com métricas vitais para o negócio:

* Total de Usuários e Contas Ativas.

* Volume de Transações (Simulado).

* Status Operacional do Serviço.

* Atualização Dinâmica: As estatísticas são atualizadas via chamadas API a cada 10 segundos, simulando um painel de controle em tempo real.


🚀 Guia de Configuração e Execução

Para colocar o Orion no ar rapidamente, siga estes passos.

- Pré-requisitos

- * Python 3.x

- * pip (Gerenciador de pacotes)

1. Clonagem e Instalação

# 1. Clone o repositório
git clone [LINK_DO_REPOSITORIO]
cd orion-digital-bank

# 2. (Opcional) Crie e ative um ambiente virtual
Comando caso necessario para plolitica
- Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
- python -m venv venv
- .\venv\Scripts\Activate.ps1
- source venv/bin/activate 

# 3. Instale as dependências essenciais
pip install Flask werkzeug bcrypt


2. Configuração Inicial do Admin
-  Cria o arquivo users.json com a conta administrativa
- python setup_admin.py

3. Execução do Servidor
   
É obrigatório rodar o script de setup para criar o arquivo users.json e criptografar a senha inicial do Super Admin.

Cria o arquivo users.json com a conta administrativa
python setup_admin.py



# Inicie o servidor Flask
python app.py
O servidor estará disponível em: http://127.0.0.1:5000

🔑 Credenciais para Demonstração

Use estas credenciais para testar as diferentes funcionalidades do sistema:

Perfil, E-mail, Senha,

Rota de Acesso:  
- Super Admin

* admin@orion.com

* admin123

/admin/dashboard

- Usuário Comum

Deve ser registrado

Qualquer senha

/dashboard
