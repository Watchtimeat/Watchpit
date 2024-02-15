from flask import Blueprint, request, jsonify, abort
from models.html import generate_receipt,generate_html_via_cliente,generate_orcamento_cliente,generate_via_interna,generate_html_via_cliente_ci,generate_orcamento_cliente_ci
import json





blueprint = Blueprint("html", __name__, url_prefix="/api/html")

@blueprint.route("via_cliente", methods=["POST"])
def generate_html_via_cliente_handler():
    data = request.get_json()
    return jsonify(generate_html_via_cliente(data["codigo_estoklus"],data["loja"],data["id"]))

@blueprint.route("via_interna", methods=["POST"])
def generate_via_interna_handler():
    data = request.get_json()
    return jsonify(generate_via_interna(data["codigo_estoklus"],data["loja"],data["id"]))

@blueprint.route("orcamento_cliente",methods=["POST"])
def generate_orcamento_cliente_handler():
    data = request.get_json()
    return jsonify(generate_orcamento_cliente(data["codigo_estoklus"],data["loja"],data["id"]))

@blueprint.route("recibo",methods=["POST"])
def generate_recibo_handler():
    data = request.get_json()
    return jsonify(generate_receipt(data))


