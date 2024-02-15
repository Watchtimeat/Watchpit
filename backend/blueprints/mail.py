from flask import Blueprint, request, jsonify, abort
from functions.mail import envia_email,envia_orcamento,buscar_anexos_os,envia_os_abertura
from blueprints.utils import get_current_user
import base64


blueprint = Blueprint("mail", __name__, url_prefix="/api/mail")




@blueprint.route("via_cliente", methods=["POST"])
def enviar_email_handler():
    data = request.get_json()
    user = get_current_user()
    data["usuario_envio"] = user["email"]
    data["nome_usuario"] = user["name"]    
    envia_email(data)
    return 'OK'

@blueprint.route("orcamento", methods=["POST"])
def enviar_orcamento_handler():
    data = request.get_json()
    user = get_current_user()
    data["usuario_envio"] = user["email"]
    data["nome_usuario"] = user["name"]
    data["usuario_envio"] = get_current_user()["email"]
    envia_orcamento(data)
    return 'OK'


@blueprint.route("listar_fotos", methods=["POST"])
def listar_anexos():
    data = request.get_json()
    os_id = data['codigo_estoklus']
    ano = data['ano']
    mes = data['mes']

    if ano is None or mes is None:
        return jsonify({"error": "Ano e mês são requeridos."}), 400

    codigo_os = str(os_id).zfill(6)  # Assegura zeros à esquerda
    try:
        arquivos = buscar_anexos_os(ano, mes, codigo_os)
        imagens_base64 = []
        for arquivo in arquivos:
            with open(arquivo, 'rb') as imagem:
                encoded_string = base64.b64encode(imagem.read()).decode('utf-8')
                imagens_base64.append(f"data:image/jpg;base64,{encoded_string}")

        return jsonify(imagens_base64)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    


@blueprint.route("via_abertura", methods=["POST"])
def enviar_os_aberta_handler():
    data = request.get_json()
    user = get_current_user()
    data["email_funcionario"] = user["email"]
    envia_os_abertura(data)
    return 'OK'



