# import o banco de dados que foi criado no main.py
from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin


# função carregar usuario
@login_manager.user_loader
def load_usuario(id_usuario):
    # o metodo get() encontra um ususario de acordo com primary Key
    return Usuario.query.get(int(id_usuario))
    

# o flask + SqlAlchemy permite criar as tabelas do database como se fossem classes
# database.model é a super classe do SqlAlchemy
# UserMixin é o parametro que vai gerenciar se o usuario está logado
class Usuario(database.Model, UserMixin):
    # colunas do database
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    cursos = database.Column(database.String, nullable=False,
                             default='Não Informado')
    # relacionar a tabela usuario com a tabela post
    # relationship( tabela relacionamento, backref= nome do usuario na tabela post)
    posts = database.relationship('Post', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False,
                                   default=datetime.utcnow)
    # relacao com a tabela usuario
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),
                                 nullable=False)
