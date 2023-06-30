from flask import Flask
# banco dados usado com flask pela integração
from flask_sqlalchemy import SQLAlchemy
# criptografar senha - pip install flask-bcrypt
from flask_bcrypt import Bcrypt
# função flask para fazer Login - pip install flask-login
from flask_login import LoginManager
import os
import sqlalchemy

# CONFIGURAÇÃO DO SITE
app = Flask(__name__)

'''entrar no cmd para gerar um token autom. -> digite python
import secret
secret.token_hex(16)
só copiar o token gerado'''

app.config['SECRET_KEY'] = '38d0fbbce56ec6746901d03a202a8435'
# configurar o banco de dados, caminho do banco de dados
if os.getenv("DATABASE_URL"):
    # se tiver no servidor pega o valor dessa variavel
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    # se estiver local esse caminho
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

# criar o banco de dados apartir do app
database = SQLAlchemy(app)
# cria a isntancia do Bcrypt 
bcrypt = Bcrypt(app)
# cria a isntancia do Login
login_manager = LoginManager(app)
# direciona pra pagina login, quando tenta acessar pagina bloqueada
login_manager.login_view = 'login'
# configurar a mensagem e a categoria da mensagem pra exibir no @login_required()
login_manager.login_message = 'Faça o Login pra acessar este conteúdo'
login_manager.login_message_category = 'alert-info'

# criar banco de dados local
# with app.app_context():
#     database.create_all()

# criar banco de dados online
from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
# verificar se no banco de dados tem a tabela Usuario
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()

# TEM QUE SER NO FINAL - pra importar os routes(links) o app tem que estar criado
from comunidadeimpressionadora import routes
