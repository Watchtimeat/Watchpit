from os import error
from flask import Blueprint, request, jsonify, abort
from models.wpp import envia_mensagem
import json

blueprint = Blueprint("wpp", __name__,url_prefix="/api/wpp")

@blueprint.route("envia_OS", methods=['POST'])
def envia_os_handler():

    data = request.get_json()
    return jsonify(envia_mensagem(data["nome"],data["codigo_estoklus"],data["loja"],data["id"],data["status"]))

