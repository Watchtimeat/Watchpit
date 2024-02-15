from flask import Blueprint, request, jsonify, abort,send_file
import asyncio,os,tempfile
from pyppeteer import launch
from models.html import generate_html_via_cliente,generate_orcamento_cliente,generate_via_interna,generate_html_via_cliente_ci,generate_orcamento_cliente_ci,generate_receipt
import logging
logging.getLogger('pyppeteer').setLevel(logging.WARNING)
logging.getLogger('websockets').setLevel(logging.WARNING)
logging.getLogger('selectors').setLevel(logging.WARNING)

blueprint = Blueprint("pdf", __name__, url_prefix="/api/pdf")


async def html_file_to_pdf(html_path, pdf_path):
    browser = await launch(args=['--no-sandbox'],ignoreHTTPSErrors=True)
    page = await browser.newPage()

    # Navega até o caminho do arquivo HTML local
    await page.goto(f'file://{html_path}')

    # Gera o PDF
    await page.pdf({'path': pdf_path, 'format': 'A4','printBackground': 'true','pageRanges': '1'})

    await browser.close()




#html = get_html_puro
@blueprint.route("via_cliente", methods=["POST"])
def generate_pdf_via_cliente():
    data = request.get_json()
    html = generate_html_via_cliente(data["codigo_estoklus"],data["loja"],data["id"])["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    
    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response

@blueprint.route("via_interna", methods=["POST"])
def generate_pdf_via_interna():
    data = request.get_json()
    html = generate_via_interna(data["codigo_estoklus"],data["loja"],data["id"])["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response

@blueprint.route("orcamento_cliente", methods=["POST"])
def generate_pdf_orcamento_cliente():
    data = request.get_json()
    html = generate_orcamento_cliente(data["codigo_estoklus"],data["loja"],data["id"])["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response


@blueprint.route("orcamento_cliente_ci",methods=["POST"])
def generate_orcamento_cliente_ci_handler():
    data = request.get_json()
    html = generate_orcamento_cliente_ci(data["codigo_estoklus"],data["loja"],data["id"])["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response


@blueprint.route("via_cliente_ci",methods=["POST"])
def generate_via_cliente_ci_handler():
    data = request.get_json()
    
    html = generate_html_via_cliente_ci(data["codigo_estoklus"],data["loja"],data["id"])["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response

@blueprint.route("recibo",methods=["POST"])
def generate_recibo_handler():
    data = request.get_json()
    
    html = generate_receipt(data)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(html.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'output{data["id"]}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))

    response = send_file(pdf_path, as_attachment=True, download_name=f'{data["id"]}.pdf', mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"inline; filename={data['id']}.pdf"
    return response


    

