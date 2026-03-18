# Importando o Flask na aplicação
from flask import Flask, render_template

# Carregando o Flask em uma variável
app = Flask(__name__, template_folder='views')

# __name__ é uma variável de ambiente do Python que tem o nome do módulo atual

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
    
    # Criando Vetor (Lista)
    jogadores = ['Eduardo','Carlinhos','Breno','Marcele']
    
    return render_template('games.html',
                           titulo=titulo,
                           ano=ano,
                           genero=genero,
                           jogadores=jogadores)
# {{ nome da variável }} -> Jinja2 permite exibir variáveis Python no HTML (um pacote do Flask)

@app.route('/consoles')
def consoles():
    consoles = ['Playstation 4','Playstation 3','Xbox 360','Xbox One','Nintendo Switch']
    return render_template('consoles.html',
                           consoles=consoles)


# Iniciando o servidor web
if __name__ == '__main__':
    app.run(debug=True)