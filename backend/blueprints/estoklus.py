from flask import Blueprint, request, jsonify, abort
import json

from blueprints.utils import get_current_user
from models.estoklus.brands import brands
from models.estoklus.service_orders import pedido_por_os , get_service_orders,grupo_estoklus,usuarios_estoklus,orcamento_estoklus,consulta_peca_estoklus,consulta_servico_estoklus,consulta_dados_marca,atualizar_os,get_os_completa,load_cx_marcas,load_dados_entrega
from models.estoklus.importation import create_order_estoklus
from models.estoklus.products import prod_diff,price_update,description_update
from models.estoklus.spareparts import gerar_romaneio,gerar_separacao,consulta_romaneios,baixa_pecas,devolve_peca,baixa_pecas_os
from models.estoklus.services import tracking_id,carrega_dados_devolucao,gerar_nf_remessa,gerar_nf_icms,liberado_execucao,gera_historico,get_forma_pagamentos,reprovar_os,aprovar_os,lanca_financeiro,consulta_financeiro_os,insere_peca_extra
from models.estoklus.services import desativa_peca,remove_peca,libera_os_acessorios,fluxo_conserto
from models.service_orders import update_service_order


blueprint = Blueprint("estoklus", __name__, url_prefix="/api/estoklus")

@blueprint.route("brands_by_so", methods=["GET"])
def get_estoklus_brands_handler():
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    get_current_user()
    return jsonify(brands())

@blueprint.route("order_by_so", methods=["POST"])
def get_estoklus_order_handler():
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    current_user = get_current_user()
    data = request.get_json()
    data["owner"] = current_user["name"]   
    if data:
        return jsonify(pedido_por_os(data["brand_id"],data["agrupa"],data["owner"]))
    abort(403)
   

@blueprint.route("service_orders", methods=["GET"])
def get_service_orders_handler():

    return jsonify(get_service_orders())

@blueprint.route('importation', methods=['POST'])
def create_order_estoklus_handler():
    json_data = request.form['data']
    file = request.files['file']
    
    # Verificar se json_data é uma string JSON e convertê-la em um dicionário, se necessário
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data"}), 400
    
    return jsonify(create_order_estoklus(json_data, file))

 

@blueprint.route('products_importation', methods=['GET'])
def product_diff_handler():

    
    return jsonify(prod_diff())

@blueprint.route('products_name', methods=['PATCH'])

def product_name_handler():

    
    return jsonify(description_update())


@blueprint.route('products_cost', methods=['PATCH'])

def product_cost_handler():

    
    return jsonify(price_update())


@blueprint.route('gerar_romaneio', methods=['POST'])

def gerar_romaneio_handler():
    data = request.get_json()
    
    return jsonify(gerar_romaneio(data["items"],data["unidade_origem"],data["unidade_destino"]))

@blueprint.route('gerar_separacao', methods=['GET'])

def gerar_separacao_handler():
    
    return jsonify(gerar_separacao())

@blueprint.route('grupo/<grupo>', methods=['GET'])

def consultar_grupos_handler(grupo):
    
    return jsonify(grupo_estoklus(grupo))

@blueprint.route('usuarios', methods=['GET'])

def consultar_usuarios_handler():
    
    return jsonify(usuarios_estoklus())


@blueprint.route("tracking/<cliente>", methods=["GET"])
def get_tracking_id_handler(cliente):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(tracking_id(cliente))


@blueprint.route("orc", methods=["GET"])
def get_orcamento_estoklus_handler():
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    referencia = request.args.get('referencia')
    return jsonify(orcamento_estoklus(referencia))


@blueprint.route("pecas", methods=["GET"])
def get_consulta_peca_estoklus_handler():
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    referencia = request.args.get('referencia')
    get_current_user()
    return jsonify(consulta_peca_estoklus(referencia))

@blueprint.route("servicos/<marca>", methods=["GET"])
def get_consulta_servico_estoklus_handler(marca):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(consulta_servico_estoklus(marca))


@blueprint.route("marca/<marca>", methods=["GET"])
def get_consulta_dados_marca_estoklus_handler(marca):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(consulta_dados_marca(marca))


@blueprint.route("atualizar/<sistema>", methods=["GET"])
def get_atualizar_os_handler(sistema):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(atualizar_os(sistema))


@blueprint.route("nf_saida/<cliente>", methods=["GET"])
def get_nf_devolucao_handler(cliente):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(carrega_dados_devolucao(cliente))



@blueprint.route("nf_remessa", methods=["POST"])
def gerar_nf_remessa_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    return jsonify(gerar_nf_remessa(data))


@blueprint.route("nf_icms", methods=["POST"])
def gerar_nf_icms_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    return jsonify(gerar_nf_icms(data))

@blueprint.route("liberado_execucao", methods=["POST"])
def liberado_execucao_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    data["estoklus_id"] = get_current_user()["estoklus_id"]
    return jsonify(liberado_execucao(data))

@blueprint.route("consulta_romaneios", methods=["POST"])
def consulta_romaneios_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    return jsonify(consulta_romaneios(data["code"]))

@blueprint.route("historico", methods=["POST"])
def historico_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    return jsonify(gera_historico(data["texto"],data["os"],data["cliente"],data["titulo"]))

@blueprint.route("pagamentos", methods=["GET"])
def get_forma_pagamentos_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(get_forma_pagamentos())



@blueprint.route("reprovar_os", methods=["POST"])
def reprova_os_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    data["status"] = '3'
    update_service_order(data)
    data["estoklus_id"]= get_current_user()["estoklus_id"]
    return jsonify(reprovar_os(data))

@blueprint.route("aprovar_os", methods=["POST"])
def aprovar_os_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    data["status"] = '4'
    data["estoklus_id"]= get_current_user()["estoklus_id"]
    update_service_order(data)
    return jsonify(aprovar_os(data))


@blueprint.route("get_os_completa/<id>", methods=["GET"])
def get_os_completa_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(get_os_completa(id)[0])

@blueprint.route("financeiro/<id>", methods=["GET"])
def get_financeiro_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(consulta_financeiro_os(id))


@blueprint.route("financeiro/<id>", methods=["POST"])
def post_financeiro_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    data["usuario"] =  get_current_user()["estoklus_id"]
    return jsonify(lanca_financeiro(id,data["valor"],data["forma_pagamento"],data["tipo"],data["usuario"],data["observacao"],data["loja"]))


@blueprint.route("baixa_pecas", methods=["POST"])
def baixa_pecas_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    user = get_current_user()
    return jsonify(baixa_pecas(data["items"],user["estoklus_id"]))


@blueprint.route("peca_extra/<os>", methods=["POST"])
def insere_peca_extra_handler(os):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    user = get_current_user()["estoklus_id"]
    return jsonify(insere_peca_extra(data["item"],os,user,data["loja"]))


@blueprint.route("desativa_peca/<id>", methods=["POST"])
def remove_peca_extra_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """

    return jsonify(desativa_peca(id))


@blueprint.route("exclui_peca/<id>", methods=["POST"])
def exclui_peca_extra(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """

    return jsonify(remove_peca(id))


@blueprint.route("devolve_peca", methods=["POST"])
def devolve_peca_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    user = get_current_user()
    return jsonify(devolve_peca(data["item"],user["estoklus_id"]))


@blueprint.route("baixa_pecas_os", methods=["POST"])
def baixa_pecas_os_handler():
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    user = get_current_user()
    return jsonify(baixa_pecas_os(data["items"],user["estoklus_id"]))

@blueprint.route("libera_acessorio/<id>", methods=["POST"])
def libera_acessorio_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    user = get_current_user()
    return jsonify(libera_os_acessorios(id,user["estoklus_id"]))


@blueprint.route("cx/<id>", methods=["GET"])
def carrega_dados_aux_OS(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(load_cx_marcas(id))


@blueprint.route("dados_entrega/<id>", methods=["GET"])
def carrega_dados_entrega_handler(id):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    return jsonify(load_dados_entrega(id))



@blueprint.route("fluxo_conserto/<fluxo>", methods=["POST"])
def fluxo_conserto_handler(fluxo):
    
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    user= get_current_user()["estoklus_id"]
    return jsonify(fluxo_conserto(data,fluxo,user))






















