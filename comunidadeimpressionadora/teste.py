# arquivo só pra testes do banco de dados
# o projeto não usa esse arquivo

from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario, Post

# with é uma regra do flask pra comandos database
with app.app_context():
    database.create_all()


with app.app_context():
    # cria usuario
    usuario = Usuario(username="Alex", email="alex@gmail.com", senha="123456")
    usuario2 = Usuario(username="Joao", email="joao@gmail.com", senha="123456")
    # adiciona usuario na seção
    database.session.add(usuario)
    database.session.add(usuario2)
    # faz o commit
    database.session.commit()

# pegar todos os usuarios
with app.app_context():
    meus_usuarios = Usuario.query.all()
    print(meus_usuarios)
    primeiro_usuario = Usuario.query.first()
    print(primeiro_usuario.id)
    print(primeiro_usuario.username)
    print(primeiro_usuario.email)
    print(primeiro_usuario.senha)
    # pegar usuario com uma condição
    usuario_teste = Usuario.query.filter_by(id=2).first()
    print(usuario_teste.email)

# criando Post
with app.app_context():
    meu_post = Post(id_usuario=1, titulo="Primeiro Post do Alex",
                    corpo="Alex programador")
    database.session.add(meu_post)
    database.session.commit()


# with app.app_context():
    meus_post = Post.query.first()
    print(meus_post.titulo)
    print(meus_post.autor.email)
