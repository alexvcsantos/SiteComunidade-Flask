#  ROUTE - TODOS OS LINKS DO SITE

# render_template -> vai carregar autom. a pagina ('nome_pagina.html') na pasta templates
# url_for -> autom os links usando variavel, pega o link da função route
from flask import render_template, redirect, flash, url_for, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image # pip install Pillow - compacta imagem


# decorator -> route('/') -> defini qual link vai abrir essa função
@app.route('/')
def home():
    # pegar os posts ordenado decrescente
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required  # exigi que esteja logado pra entrar nesse link
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


# todo formulario que tiver que enviar info, tem que adicionar o parametro methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    # verifica se login foi validade e se o texto 'botao_submit_login' está na requisição do POST
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # verifica se usuario é valido e compara a senha digitada com a senha cripto do banco
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # remember lembra o usuario logado
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(
                f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            # pegar o parametro next da url, pra poder direcionar pro link que estava acessando
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                # caso seja vazio redirecionar para homepage
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Inválido', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criptografar senha (.decode("utf-8") - pra funcionar no postgres do railway)
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        # pegar dados do usuário
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_crypt)
        # adicionar no banco de dados
        database.session.add(usuario)
        database.session.commit()
        flash(
            f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required  # exigi que esteja logado pra entrar nesse link
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required  # exigi que esteja logado pra entrar nesse link
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required  # exigi que esteja logado pra entrar nesse link
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    # adicionar codigo aleatoria no nome da imagem pra ser unico
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (400, 400) # tamanho da imagem em pixels
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta foto_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuario para o novo nome da imagem
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


# <post_id> - é uma variavel pra gerar o link pra cada post
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        # carregar o titulo e corpo nos campos automat.
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        # se for o autor vai dar erro
        abort(403)