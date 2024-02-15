import logging
from flask import Blueprint, request, jsonify, abort
from numpy import extract

from blueprints.utils import get_current_user, multidict_to_dict
from datetime import datetime
from blueprints.utils import get_current_user
import os

from models.estoklus import Estoklus
from models.estoklus.pbi import get_reproved_orders,get_repaired_orders,get_openned_orders,get_estimated_orders,get_approved_orders,get_delivered_orders,get_awaiting_estimate,get_awaiting_approval,get_awaiting_start_repair,get_awaiting_finish,get_awaiting_delivery,get_invoiced,brands
from models.estoklus.service_orders import importar_os,get_pecas,get_capa_os
from models.service_orders import create_service_orders,get_service_order,update_service_order,create_service_order,get_service_orders,get_service_orders_summary,get_service_order_items
from models.service_orders import create_customer,create_customers,get_customer,get_customers,calcula_orcamento,create_service_estimate,next_letter_for_os,copy_file_as_root,update_service_order,select_quickview
from models.estoklus.service_orders import importar_clientes,importar_pecas,atualizar_os_single

blueprint = Blueprint("service_orders", __name__, url_prefix="/api/service_orders")

@blueprint.route("repaired_orders", methods=["GET"])
def get_repaired_orders_handler():
     
    get_current_user()
    return jsonify(get_repaired_orders())

@blueprint.route("openned_orders", methods=["GET"])
def get_openned_orders_handler():
     
    get_current_user()
    return jsonify(get_openned_orders())


@blueprint.route("estimated_orders", methods=["GET"])
def get_estimated_orders_handler():
     
    get_current_user()
    return jsonify(get_estimated_orders())


@blueprint.route("approved_orders", methods=["GET"])
def get_approved_orders_handler():
     
    get_current_user()
    return jsonify(get_approved_orders())


@blueprint.route("delivered_orders", methods=["GET"])
def get_delivered_orders_handler():
     
    get_current_user()
    return jsonify(get_delivered_orders())


@blueprint.route("awaiting_estimate", methods=["GET"])
def get_awaiting_estimate_handler():
     
    get_current_user()
    return jsonify(get_awaiting_estimate())


@blueprint.route("waiting_approval", methods=["GET"])
def get_awaiting_approval_handler():
     
    get_current_user()
    return jsonify(get_awaiting_approval())


@blueprint.route("awaiting_start_repair", methods=["GET"])
def get_awaiting_start_repair_handler():
     
    get_current_user()
    return jsonify(get_awaiting_start_repair())


@blueprint.route("awaiting_finish", methods=["GET"])
def awaiting_finish_handler():
     
    get_current_user()
    return jsonify(get_awaiting_finish())


@blueprint.route("awaiting_delivery", methods=["GET"])
def awaiting_delivery_handler():
     
    get_current_user()
    return jsonify(get_awaiting_delivery())

@blueprint.route("invoiced", methods=["GET"])
def get_invoiced_handler():
     
    get_current_user()
    return jsonify(get_invoiced())

@blueprint.route("brands", methods=["GET"])
def get_brands_handler():
     
    get_current_user()
    return jsonify(brands())
@blueprint.route("reproveds", methods=["GET"])
def get_reproveds_handler():
     

    return jsonify(get_reproved_orders())


@blueprint.route("<service_order_id>", methods=["GET"])
def get_service_order_id_handler(service_order_id):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_service_order(service_order_id))


@blueprint.route("", methods=["POST"])
def create_service_order_handler():
    """ create product based on the given data

    POST /products

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_service_orders(data))
    elif isinstance(data, object):
        return jsonify(create_service_order(data))
    abort(400)


@blueprint.route("<service_order>", methods=["PATCH"])
def update_service_order_handler(service_order_id):
    """ update product

    PUT /products/<product_id>

    :body: {
        attribute: value
    }

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_service_order({**request.get_json(), "id": service_order_id}))


@blueprint.route("estoklus/<sistema>", methods=["GET"])
def get_service_orders_estoklus_handler(sistema):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(importar_os(sistema))


@blueprint.route("", methods=["GET"])
def get_service_orders_handler():
    """ get purchase orders

    GET /purchase_orders

    parameters:
        <field>: <value>

    :return: [
        {
            id: product id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_service_orders(filters))


@blueprint.route("summary/<column>", methods=["GET"])
def get_service_orders_summary_handler(column):
    """ get purchase orders summary

    GET /purchase_orders/summary/<column>

    parameters:
        <field>: <value>

    :return: { <column>: number of puchase orders }
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_service_orders_summary(column, filters))


@blueprint.route("pecas_estoklus/<sistema>", methods=["GET"])
def get_service_orders_items_handler(sistema):
    """ get purchase orders summary

    GET /purchase_orders/summary/<column>

    parameters:
        <field>: <value>

    :return: { <column>: number of puchase orders }
    """
    return jsonify(importar_pecas(sistema))

@blueprint.route("pecas", methods=["GET"])
def get_service_order_items_handler():

    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_service_order_items(filters))

@blueprint.route("orc", methods=["POST"])  
def get_calculo_orcamento_handler():
    """ get product

    POST /product/<product_id>  # Aqui trocamos GET por POST

    :return: {
        id: product id
        attribute: value
    }
    """
    data = request.get_json()
    get_current_user()
    return jsonify(calcula_orcamento(data["itens"],data["desconto"]))


@blueprint.route("orcamento", methods=["POST"])
def create_estimate_handler():
    """ create product based on the given data

    POST /products

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    data["status"] = '2'
    update_service_order(data)
    return jsonify(create_service_estimate(data))


@blueprint.route("clientes", methods=["GET"])
def get_clientes_handler():


    return jsonify(importar_clientes())

@blueprint.route("fotos", methods=["POST"])
def upload_files():
    if 'image' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('image')
    os_number = int(request.form.get("os_number"))
    if not os_number:
        return jsonify({"error": "No OS number provided"}), 400
    estoklus = Estoklus()
    # Seu diretório destino
    query =f"""select extract(year from data_os), extract(month from data_os)
    from e_assist_tecnica ast
    where ast.codigo_os_assist_tecnica = {os_number}"""
    retorno = estoklus.fetchall(query)
    mes = str(retorno[0][1]).zfill(2)  # preenche com zero à esquerda se necessário
    ano = retorno[0][0]
    directory = f"/mnt/my_share/CDSIS/Estoklus/Fotos/{ano}-{mes}/OS-{os_number:06}"
        # Supondo que você tem a OS number no form data
    if not os.path.exists(directory):
        os.makedirs(directory)

    saved_files = []
    for file in files:
        next_letter = next_letter_for_os(os_number, directory)
        destination_path = os.path.join(directory, f"F-{os_number:06}-{next_letter}.jpg")
        copy_file_as_root(file, destination_path)
        saved_files.append(destination_path)
    logging.info(f'Foto da OS {os_number} gravada')
    return jsonify({"message": f"Files saved as {', '.join(saved_files)}"}), 200


@blueprint.route("analisar/<service_order_id>", methods=["GET"])
def get_pecas_handler(service_order_id):
    return jsonify(get_pecas(service_order_id))

@blueprint.route("capa/<service_order_id>", methods=["GET"])
def get_capa_os_handler(service_order_id):
    return jsonify(get_capa_os(service_order_id))

@blueprint.route("atualizar/<service_order_id>", methods=["POST"])
def atualizar_os_handler(service_order_id):
    return jsonify(atualizar_os_single(service_order_id))


@blueprint.route("quickview/<documento>", methods=["GET"])
def get_quickview_handler(documento):
    return jsonify(select_quickview(documento))


