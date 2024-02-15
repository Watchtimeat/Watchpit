import json
import psycopg2
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from flask import Blueprint, jsonify, request

blueprint = Blueprint('excel', __name__)

@blueprint.route('/api/get_excel', methods=['POST'])
def get_excel():
    data = request.json
    purchase_order_id = data['purchase_order_id']

    # Conectar-se à base de dados do PostgreSQL
    conn = psycopg2.connect(database="watchtime", user="postgres", password="%Ekemvm6g", host="172.31.3.114", port="5432")

    # Executar uma consulta SQL na tabela purchase_order_items
    query = f"SELECT * FROM watchtime.purchase_order_items WHERE purchase_order_id = '{purchase_order_id}'"
    df = pd.read_sql_query(query, conn)

    data_dict = [json.loads(json.dumps(data)) for data in df['data']]
    df = pd.DataFrame(data_dict)

    # Criar um arquivo Excel e escrever os dados do DataFrame em uma planilha
    wb = Workbook()
    ws = wb.active
    df_subset = df[['product_code', 'requested_quantity']]
    col_names = ['CODIGO_PRODUTO', 'QTD']

    # Adicionar os cabeçalhos personalizados
    ws.append(col_names)
    for r in dataframe_to_rows(df_subset, index=False, header=False):
        ws.append(r)

    # Salvar o arquivo Excel em um diretório especificado
    filename = f"/app/excel_files/{purchase_order_id}.xlsx"
    wb.save(filename)

    # Retornar o nome do arquivo gerado
    return jsonify({'filename': filename})

