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
    return render_template('games.html')


@app.route('/consoles')
def consoles():
    return render_template('consoles.html')


# Iniciando o servidor web
if __name__ == '__main__':
    app.run(debug=True)