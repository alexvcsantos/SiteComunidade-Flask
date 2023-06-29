from flask import Flask
# banco dados usado com flask pela integração
from flask_sqlalchemy import SQLAlchemy
# criptografar senha - pip install flask-bcrypt
from flask_bcrypt import Bcrypt
# função flask para fazer Login - pip install flask-login
from flask_login import LoginManager

# CONFIGURAÇÃO DO SITE

app = Flask(__name__)

'''entrar no cmd para gerar um token autom. -> digite python
import secret
secret.token_hex(16)
só copiar o token gerado'''

app.config['SECRET_KEY'] = '38d0fbbce56ec6746901d03a202a8435'
# configurar o banco de dados, caminho do banco de dados, no mesmo local do main.py
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


# TEM QUE SER NO FINAL - pra importar os routes(links) o app tem que estar criado
from comunidadeimpressionadora import routes

# criar banco de dados
# with app.app_context():
#     database.create_all()