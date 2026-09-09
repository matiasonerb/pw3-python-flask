from controllers import routes
from flask import Flask

app = Flask(__name__, template_folder='views', static_folder='static')

# Inicializa as rotas
routes.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)