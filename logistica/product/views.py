from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from logistica import db, app
from logistica.product.models import User
from flask_restful import reqparse


catalog = Blueprint('product', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Bem vindo aa API do truckpad"


class ProductView(MethodView):

    def get(self, id=None, page=1):
        if not id:
            products = User.query.paginate(page, 10).items
            res = {}
            for product in products:
                res[product.id] = {
                    'nome': product.nome,
                    'sexo': product.sexo,
                    'tipoVeiculo': product.tipoVeiculo,
                    'veiculoCarregado': product.veiculoCarregado,
                    'idade': product.idade,
                    'cnh': product.cnh,
                    'possuiVeiculo': product.possuiVeiculo,
                }
        else:
            product = User.query.filter_by(id=id).first()
            if not product:
                abort(404)
            res = {
                'name': product.nome,
                'price': product.sexo,
                'tipoVeiculo': product.tipoVeiculo,
                'veiculoCarregado': product.veiculoCarregado,
                'idade': product.idade,
                'cnh': product.cnh,
                'possuiVeiculo': product.possuiVeiculo,
            }
        return jsonify(res)

    def post(self):
        nome = request.get_json().get('nome')
        sexo = request.get_json().get('sexo')
        tipoVeiculo = request.get_json().get('tipoVeiculo')
        veiculoCarregado = request.get_json().get('veiculoCarregado')
        idade = request.get_json().get('idade')
        cnh = request.get_json().get('cnh')
        possuiVeiculo = request.get_json().get('possuiVeiculo')

        user = User(nome, sexo, tipoVeiculo, veiculoCarregado, idade, cnh, possuiVeiculo)
        db.session.add(user)
        db.session.commit()
        return jsonify({user.id: {
            'nome': user.nome,
            'sexo': user.sexo,
            'tipoVeiculo': user.tipoVeiculo,
            'veiculoCarregado': user.veiculoCarregado,
            'idade': user.idade,
            'cnh': user.cnh,
            'possuiVeiculo': user.possuiVeiculo,
        }})

    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        user = User.query.filter_by(id=id).first()
        if user is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('rate', type=int, help='Rate to charge for this resource')
            args = self.parser.parse_args(strict=True)
            for key, value in args.items():
                if args[key] is not None:
                    setattr(user, key, value)
            db.session.commit()
            return jsonify({user.id: {
                'nome': user.nome,
                'sexo': user.sexo,
                'tipoVeiculo': user.tipoVeiculo,
                'veiculoCarregado': user.veiculoCarregado,
                'idade': user.idade,
                'cnh': user.cnh,
                'possuiVeiculo': user.possuiVeiculo,
            }})
        return ""



    def delete(self, id):
        # Delete the record for the provided id.
        obj = User.query.filter_by(id=id).one()
        db.session.delete(obj)
        db.session.commit()
        return "Usuario deletado com sucesso"


product_view = ProductView.as_view('product_view')
app.add_url_rule(
    '/users/', view_func=product_view, methods=['GET']
)
app.add_url_rule(
    '/new-user/', view_func=product_view, methods=['POST']
)
app.add_url_rule(
    '/user/<int:id>', view_func=product_view, methods=['GET']
)
app.add_url_rule(
    '/delete-user/<int:id>', view_func=product_view, methods=['DELETE']
)
app.add_url_rule(
    '/edit-user/<int:id>', view_func=product_view, methods=['PUT']
)