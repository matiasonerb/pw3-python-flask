# Importando o Flask na aplicação
from flask import Flask, render_template
from controllers import routes

# Carregando o Flask em uma variável
app = Flask(__name__, template_folder='views')

# __name__ é uma variável de ambiente do Python que tem o nome do módulo atual

# Enviando a variavel app para as rotas
routes.init_app(app)

# Iniciando o servidor web
if __name__ == '__main__':
    app.run(debug=True)