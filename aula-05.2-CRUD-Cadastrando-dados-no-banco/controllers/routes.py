from flask import render_template, request, redirect, url_for
from models.database import Game, Console, db

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