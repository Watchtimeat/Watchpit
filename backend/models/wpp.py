import requests,os,shutil,hashlib,time
from models.pdf import gerar_pdf
from models.estoklus import Estoklus
from models.estoklus.service_orders import formatar_nome
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

def envia_mensagem(name,service, loja, id, fase_atual):
    doc = salva_pdf(service, loja, id, fase_atual)
    url = f'https://app.watchtime.com.br/services/{doc}'
    estoklus = Estoklus()
    query = f'SELECT TEL_CELULAR from e_assist_tecnica ast join g_cadastro_geral cg on cg.codigo_cadastro_geral = ast.codigo_cliente where ast.codigo_os_assist_tecnica =  {service}'
    tel = estoklus.fetchone(query)

    # Checa se a consulta não retornou None e se não está vazia
    if tel:
        # Considerando que o retorno é uma string
        tel = tel.strip()

        # Adiciona o código do país '55' antes do número
        tel = '55' + tel

        # Remove caracteres não numéricos (como hífens, espaços, etc.)
        tel_digits = ''.join(filter(str.isdigit, tel))

        # Verifica se o número tem a quantidade de dígitos esperada (12 ou 13 considerando o '55' do Brasil)
        if 12 <= len(tel_digits) <= 13:
                
                
                if fase_atual == '1':
                    caption_text = (f"Olá, {formatar_nome(name)}!\n"
    "Essa mensagem foi enviada para documentar que sua ordem de serviço foi aberta.\n"
    "Para orçamento, informamos que o prazo para envio de orçamento é de até 3 dias úteis.\n"
    "Qualquer dúvida, estamos a disposição!\n")
                else:
                    caption_text = (f"Olá, {formatar_nome(name)}!\n"
    f"Segue acima o orçamento da sua ordem de serviço {id}.\n"
    "Qualquer dúvida, estamos a disposição!\n"
    "\n"
    "Como nossa ferramenta é automatizada, ao responder essa mensagem você será direcionado ao fluxo de atendimento. \n"
    "Para um atendimento mais rápido, selecione a opção 6 (retorno de contato) e informe o número de sua ordem de serviço."
    )           
                logging.info(f'WPP - {id}')
                return send_attachment_message(tel, id, url, caption_text)
        else:
            return {"error": "telefone inválido (tel_celular)"}
    else:
        return {"error": "telefone em branco (tel_celular)"}




def send_attachment_message(destination, filename, file_url, caption):
    # Endpoint da API
    url = "https://api.gupshup.io/sm/api/v1/msg"

    # Headers (cabeçalhos)
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": "nsxtvbpv86hayzh1fqcrhogs20rdfaex",
        "cache-control": "no-cache"
    }

    # Mensagem em formato JSON
    message_content = {
        "type": "file",
        "url": file_url,
        "caption": caption,
        "filename": filename
    }

    # Dados a serem enviados
    data = {
        "channel": "whatsapp",
        "source": "551130318551",
        "destination": destination,
        "message": str(message_content).replace("'", '"'),  # Convertendo dicionário para string JSON
        "src.name": "watchtime01452"
    }

    # Realizar a requisição POST
    response = requests.post(url, headers=headers, data=data)

    # Verificar a resposta
    if response.status_code == 200:
        print("Requisição bem-sucedida!")
        return response.json()
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None


def salva_pdf(service, loja, id, fase_atual):
    origem = gerar_pdf(service, loja, id, fase_atual)
    
    # Gere um nome de arquivo randômico baseado em um hash do tempo atual e do nome do arquivo original
    nome_randomico = hashlib.md5((str(time.time()) + origem).encode()).hexdigest() + ".pdf"
    destino = os.path.join("/app/services", nome_randomico)
    
    # Copie o arquivo da localização temporária para o destino
    shutil.copy2(origem, destino)
    
    return nome_randomico



