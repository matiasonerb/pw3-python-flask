from flask import render_template, request, redirect, url_for, flash, session
from models.database import Game, Console, db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup

# Criando a função para receber o Flask (app)
def init_app(app):
    # Simulando um Banco de Dados
    listaGames = [{"titulo": "CS-GO", "ano": 2012, "genero": "FPS"}]

    # Criando a rota principal do site
    @app.route('/')
    # def serve para criar funções no Python
    def home():
        return render_template('index.html')


    @app.route('/games')
    def games():
        # Criando variáveis para passar as informações de um jogo
        titulo = "Silk Song"
        ano = 2025
        genero = "Metroidvania"
        # variavel = chaves do obj = valores do obj
        # chave + valor = item
        
        # Criando um obj Python (dicionário) para representar as propriedades de um jogo
        game = {
            "Título" : "Minecraft",
            "Ano" : 2012,
            "Categoria" : "Sandbox"
        }
        
        # Criando Vetor (Lista)
        jogadores = ['Eduardo','Carlinhos','Breno','Marcele']
        
        return render_template('games.html',
                            titulo=titulo,
                            ano=ano,
                            genero=genero,
                            jogadores=jogadores,
                            game=game)
    # {{ nome da variável }} -> Jinja2 permite exibir variáveis Python no HTML (um pacote do Flask)

    @app.route('/consoles')
    def consoles():
        consoles = ['Playstation 4','Playstation 3','Xbox 360','Xbox One','Nintendo Switch']
        return render_template('consoles.html',
                            consoles=consoles)
    
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            listaGames.append({'titulo': request.form.get('titulo'),
                               'ano': request.form.get('ano'),
                               'genero': request.form.get('genero')})
            # o metodo append adiciona valores a lista
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               listaGames=listaGames)
        
    @app.route('/estoque-jogos', methods=['GET', 'POST'])
    # Criando um parâmetro na rota (ID) para excluir um registro
    @app.route('/estoque-jogo/delete/<int:id>')
    def estoque_jogos(id=None):
        # Verificando se está sendo enviado o parâmetro ID para a rota
        if id:
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        
        # Verificando se a requisição é do tipo POST
        if request.method == "POST":
            # Coletando os dados preenchidos no formulário
            dados_form = request.form.to_dict()
            # Enviando os dados para o Model
            newGame = Game(
                dados_form['titulo'],
                dados_form['ano'],
                dados_form['genero'],
                dados_form['plataforma'],
                dados_form['preco'],
                dados_form['quantidade']
            )
            # Método do SQLAlchemy para gravar os dados no banco
            db.session.add(newGame)
            # Confirmando a operação no banco
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        # Select * from Games
        games = Game.query.all()
        return render_template('estoque-jogos.html',
                               games=games)
        
        
    @app.route('/estoque-consoles', methods=['GET', 'POST'])
    # Criando um parâmetro na rota (ID) para excluir um registro
    @app.route('/estoque-consoles/delete/<int:id>')
    def estoque_consoles(id=None):
        # Verificando se está sendo enviado o parâmetro ID para a rota
        if id:
            console = Console.query.get(id)
            db.session.delete(console)
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
        
        # Verificando se a requisição é do tipo POST
        if request.method == "POST":
            # Coletando os dados preenchidos no formulário
            dados_form = request.form.to_dict()
            # Enviando os dados para o Model
            newConsole = Console(
                dados_form['nome'],
                dados_form['ano'],
                dados_form['fabricante'],
                dados_form['preco'],
                dados_form['quantidade']
            )
            # Método do SQLAlchemy para gravar os dados no banco
            db.session.add(newConsole)
            # Confirmando a operação no banco
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
        # Select * from Console
        consoles = Console.query.all()
        return render_template('estoque-consoles.html',
                               consoles=consoles)
        
    @app.route('/editar-jogos/<int:id>', methods=['GET', 'POST'])
    def editar_jogos(id):
        # Buscando o jogo no banco pelo ID
        game = Game.query.get(id)
        # Verificando se a requisição é POST
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.genero = dados_form['genero']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        return render_template('editar-jogos.html', game=game)
    
    @app.route('/cadastro', methods=['GET','POST'])
    def cadastro():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                msg = Markup("usuario já cadastrado. Faça o <a href='/login'>login</a>")
                flash(msg, 'danger')
                return redirect(url_for('cadastro'))
            
            senha_criptografada = generate_password_hash(senha, method='scrypt')
            
            novo_usuario = Usuario(email=email, senha=senha_criptografada)
            
            db.session.add(novo_usuario)
            db.session.commit()
            msgCad = Markup("Cadastro realizado com sucesso!. Faça o <a href='/login'>login</a>")
            flash(msgCad, 'success')
            return redirect(url_for('cadastro'))
        return render_template('cadastro.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            email = request.form['email']
            senha = request.form['senha']
            # Buscando o usuario no banco
            usuario = Usuario.query.filter_by(email=email).first()
            # Se existir
            if usuario:
                if check_password_hash(usuario.senha, senha):
                    # Criando a sessão
                    session['usuario_id'] = usuario.id
                    session['usuario_email'] = usuario.email
                    
                    msgLogin = "Você foi autenticado com sucesso! Bem vindo!"
                    flash(msgLogin, 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Falha no login. Verifique os dados e tente novamente!', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('O usuário informado não existe!', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html')