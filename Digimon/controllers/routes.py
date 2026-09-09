from flask import render_template, request
from models.digimodel import DigimonModel

def init_app(app):

    @app.route('/')
    def index():
        termo_busca = request.args.get('busca', '').strip()

        if termo_busca:
            digimon = DigimonModel.obter_detalhes_completos(termo_busca)
            digimons = [digimon] if digimon else []
        else:
            digimons = DigimonModel.obter_todos()

        return render_template('index.html', digimons=digimons, busca=termo_busca)

    @app.route('/digimon/<string:nome>')
    def detalhe(nome):
        digimon = DigimonModel.obter_detalhes_completos(nome)
        if not digimon:
            return "Digimon não encontrado no banco de dados digital.", 404
        return render_template('detalhe.html', digimon=digimon)