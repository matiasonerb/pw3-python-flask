from flask import render_template, request, redirect, url_for

# Criando a função para receber o Flask (app)
def init_app(app):
    # Simulando um Banco de Dados
    listaLivro = [{"titulo": "Coraline", "autor": "Neil Gaiman", "ano": 2002}]

    # Criando a rota principal do site
    @app.route('/')
    # def serve para criar funções no Python
    def home():
        return render_template('index.html')

    @app.route('/form')
    def form():
        return render_template('form.html')

    @app.route('/lista', methods=['GET', 'POST'])
    def lista():
        if request.method == 'POST':
            listaLivro.append({
                'titulo': request.form.get('titulo'),
                'autor': request.form.get('autor'),
                'ano': request.form.get('ano')
            })
            return redirect(url_for('lista'))  # ✅ aqui está a correção

        return render_template('lista.html', listaLivro=listaLivro)
        
#         # Criando a rota principal do site
# @app.route('/')
# # def serve para criar funções no Python
# def home():
#     return render_template('index.html')


# @app.route('/lista')
# def lista():
#     return render_template('lista.html')


# @app.route('/form')
# def form():
#     return render_template('form.html')