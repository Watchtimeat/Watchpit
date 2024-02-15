import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import models.html as htm
import codecs,os,tempfile,asyncio
from pyppeteer import launch
from models.estoklus import Estoklus
from models.estoklus.service_orders import formatar_nome,get_os_completa
from models.estoklus.services import gera_historico
from models.query import consulta_usuario_cliente_OS
import base64,shutil
from io import BytesIO
import tempfile
import html
import logging
from datetime import datetime

from pkg_resources import resource_filename
import glob

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

def buscar_anexos_os(ano, mes, codigo_os):
    # Formata o mês com dois dígitos
    mes_formatado = f"{mes:02d}"
    # Constrói o caminho do diretório
    dir_path = f"/mnt/my_share/CDSIS/Estoklus/Fotos/{ano}-{mes_formatado}/OS-{codigo_os}"
    
    # Procura por arquivos que iniciam com 'F-' seguido pelo código da OS e terminam com '.jpg'
    pattern = os.path.join(dir_path, f"F-{codigo_os}-*.jpg")
    # Retorna a lista de caminhos dos arquivos encontrados
    return glob.glob(pattern)

smtp_host='smtp.watchtime.com.br'
smtp_port=465
smtp_username = 'enviador@watchtime.com.br'
smtp_password = 'Wt01452918@#'

async def html_file_to_pdf(html_path, pdf_path):
    browser = await launch(args=['--no-sandbox'],ignoreHTTPSErrors=True)
    page = await browser.newPage()

    # Navega até o caminho do arquivo HTML local
    await page.goto(f'file://{html_path}')

    # Gera o PDF
    await page.pdf({'path': pdf_path, 'format': 'A4','printBackground': 'true','pageRanges': '1'})

    await browser.close()

def format_template(template_file, tokens):
    if not template_file.endswith(".html"):
        template_file += ".html"
    # Obtém o caminho do diretório do script atual
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Constrói o caminho completo para o arquivo de template
    template_path = os.path.join(current_directory, template_file)

    # Lê o arquivo de template

    with codecs.open(template_path, 'r', 'utf-8') as f:
        message = f.read()
    for key, value in tokens["attribute"].items():
        token = "{{" + key + "}}"
        if token in message:
            message = message.replace(token, value)
    return message

def send_mail(**kwargs):
    """ Send email based on template, tokens to email_to.

    :param kwargs: {
        "function": function id,
        "to": email to send to
        "subject": email subject
        "template": email template
        "attribute": any addicional attribute to be used by the template
    }
    :return: None
    """
    template_file = "{}.html".format(kwargs["template"])
    message_content = format_template(template_file, kwargs)
    
    email = MIMEMultipart()
    email['Subject'] = kwargs["subject"]
    email['To'] = kwargs["to"]
    email['Bcc'] = kwargs["sender"]

    email.attach(MIMEText(message_content, "html"))
    if "attachments" in kwargs:
        for file_path in kwargs["attachments"]:
            # Abrindo e lendo o arquivo
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            # Codificando o arquivo para base64
            encoders.encode_base64(part)
            
            # Adicionando cabeçalho para o anexo
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}",
            )
            
            email.attach(part)

    if smtp_host and smtp_port and 'sender' in kwargs and smtp_username and smtp_password:
        email['From'] = f"{kwargs['sender_name']} <{kwargs['sender']}>"
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(email)
    else:
        email["From"] = "<FROM>"
        print(email.as_string())


def gerar_pdf(service,loja,id,fase_atual):
    if fase_atual == '1' or fase_atual == 1:
        ht = htm.generate_html_via_cliente_ci(service,loja,id)["html"]
    else :
        ht = htm.generate_orcamento_cliente_ci(service,loja,id)["html"]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
         temp.write(ht.encode())
         html_path = temp.name
    pdf_path = os.path.join(tempfile.gettempdir(), f'{id}.pdf')
    asyncio.get_event_loop().run_until_complete(html_file_to_pdf(html_path, pdf_path))
    return pdf_path
    





def envia_email(os_info):
    query = consulta_usuario_cliente_OS(os_info["codigo_estoklus"])
    estoklus = Estoklus()
    user = estoklus.fetchall(query)[0]

    anexos_adicionais = []
    if os_info.get("envia_pdf", 'S') == 'S':
        pdf_path = gerar_pdf(os_info["codigo_estoklus"], os_info["loja"], os_info["id"], os_info["status"])
        anexos_adicionais.append(pdf_path)

    contador = 1
    for base64_str in os_info.get("anexosBase64", []):
        base64_data = base64_str.split(';base64,')[-1]
        arquivo_bytes = base64.b64decode(base64_data)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(arquivo_bytes)

        nome_amigavel = f"Foto_{contador}.jpg"
        contador += 1

        caminho_amigavel = os.path.join(os.path.dirname(temp_file.name), nome_amigavel)
        shutil.move(temp_file.name, caminho_amigavel)
        anexos_adicionais.append(caminho_amigavel)

    # Formata o texto do usuário com quebras de linha HTML
    texto_usuario = os_info.get("texto_usuario", "")
    texto_usuario_html = html.escape(texto_usuario).replace("\n", "<br>")

    # Envia o e-mail
    send_mail(
        sender_name=f'{formatar_nome(os_info["nome_usuario"])} | Watch Time',
        sender=os_info["usuario_envio"],
        function="any_function_id",
        to=user[3],
        subject=os_info.get("titulo", f"Ordem de Serviço {os_info['id']}"),
        template="custom",
        attribute={
            "name": formatar_nome(user[2]),
            "text": texto_usuario_html  # Passa o texto formatado como um atributo
        },
        attachments=anexos_adicionais
    )

    # Limpeza: remove todos os anexos, incluindo o PDF se ele foi criado
    for arquivo in anexos_adicionais:
        if os.path.exists(arquivo):
            os.remove(arquivo)
    logging.info(f'Enviado e-mail da OS {os_info["id"]}')
    cliente_id = estoklus.fetchone(f"select codigo_cliente from e_assist_tecnica where codigo_os_assist_tecnica = {os_info['codigo_estoklus']}")
    try:
        # Tenta converter status para um inteiro
        status_int = int(os_info.get("status", 0))
    except ValueError:
        # Se a conversão falhar, define status_int como um valor padrão, por exemplo, 0
        status_int = 0
    
    # Agora você pode fazer a comparação usando status_int
    if status_int > 1 and status_int < 4:
            gera_historico(os_info["texto_usuario"],os_info["codigo_estoklus"],cliente_id,'Orçamento Enviado por E-mail')
    elif status_int == 6:
            gera_historico(os_info["texto_usuario"],os_info["codigo_estoklus"],cliente_id,'Avisado Pronto por e-mail')
    


def envia_orcamento(os):
    dados = get_os_completa(os["codigo_estoklus"])[0]
    pdf_path = gerar_pdf(os["codigo_estoklus"],os["loja"],os["id"],os["status"])
    send_mail(sender_name=f'{formatar_nome(os["nome_usuario"])} | Watch Time',
        sender=os["usuario_envio"],
        function="any_function_id",
        to=dados["email"],
        subject=f"Ordem de Serviço {os['id']}",
        template="orcamento",
        attribute={"name": formatar_nome(dados["nome"]),
                   "marca":dados.get("marca",''),
                   "modelo":dados.get("modelo",''),
                   "referencia":dados.get("referencia_produto",''),
                   "serie":dados.get("serie",''),
                   "os":str(dados["codigo_estoklus"]),
                   "diagnostico":dados.get("diagnostico_tecnico",''),
                   "garantia":dados.get("garantia",''),
                   "prazo":dados.get("prazo_entrega",''),
                   "funcionario":dados.get("nome_tecnico",'')

                   },
        attachments=[pdf_path])
    


def envia_os_abertura(os):
    pdf_path = gerar_pdf(os["codigo_estoklus"],os["loja"],os["id"],os["status"])
    send_mail(sender_name=f'{formatar_nome(os["username"])} | Watch Time',
      sender=os["email_funcionario"],
      function="any_function_id",
      to=os["email"],
      subject=f"Ordem de Serviço {os['id']}",
      template="hello",
      attribute={"name": formatar_nome(os['nome'])},
      attachments = [pdf_path]) 

