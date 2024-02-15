
import models.html as html
import codecs,os,tempfile,asyncio
from pyppeteer import launch
import logging

# Configura o nível de log para WARNING apenas para Pyppeteer e websockets
logging.getLogger('pyppeteer').setLevel(logging.WARNING)
logging.getLogger('websockets').setLevel(logging.WARNING)
logging.getLogger('selectors').setLevel(logging.WARNING)

def gerar_pdf(service,loja,id,fase_atual):
    if fase_atual == '1':
        ht = html.generate_html_via_cliente_ci(service,loja,id)["html"]
    else :
        ht = html.generate_orcamento_cliente_ci(service,loja,id)["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(ht.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'{id}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))
    return pdf_path

def gerar_recibo(os):
    ht = html.generate_receipt(os)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(ht.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'{id}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))
    return pdf_path


async def html_file_to_pdf(html_path, pdf_path):
    browser = await launch(args=['--no-sandbox'],ignoreHTTPSErrors=True)
    page = await browser.newPage()

    # Navega até o caminho do arquivo HTML local
    await page.goto(f'file://{html_path}')

    # Gera o PDF
    await page.pdf({'path': pdf_path, 'format': 'A4','printBackground': 'true','pageRanges': '1'})

    await browser.close()