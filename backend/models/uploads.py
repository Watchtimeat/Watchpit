from flask import request
from models import fetchone


import os


UPLOAD_FOLDER = '/app/order_files' # diretório onde os arquivos serão salvos
ALLOWED_EXTENSIONS = {'pdf'} # extensões permitidas para os arquivos

def file_upload(purchase_order_id):
    if 'file' not in request.files:
        return {'error': 'no file uploaded'}

    file = request.files['file']
    if file.filename == '':
        return {'error': 'no file selected'}

    if file and allowed_file(file.filename):
        row = fetchone(f"select id, data from watchtime.purchase_orders where id=%s", purchase_order_id)
        status = row[1]['status']
        folder_name = f"{UPLOAD_FOLDER}/{purchase_order_id}"
        
        if status == "draft": 
            status = "Rascunho"
        if status == "confirmed":
            status = "Pedido"
        if status == "approved":
            status = "Proforma"
        filename = f"{status}.pdf"

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        full_path = os.path.join(folder_name, filename)
        i = 1
        while os.path.exists(full_path):
            i += 1
            full_path = os.path.join(folder_name, f"{status}_{i}.pdf")
        file.save(full_path)
        base_url = "https://app.watchtime.com.br/excel_files"
        file_url = f"{base_url}/{purchase_order_id}/{filename}"
        return {'success': file_url}

    else:
        return {'error': 'invalid file type'}
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS