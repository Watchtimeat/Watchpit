from models.estoklus.service_orders import get_os_completa
import logging


def generate_html_via_cliente(codigo_estoklus,loja,id):

    data = get_os_completa(codigo_estoklus)[0]
    data["loja"] =loja
    data["id"]= id
    if data["loja"] == 'SP':
        endereco =       """<p>Av Pedroso de Morais, 457 12 andar Cj 1202
                                <br>05419 - 000, Pinheiros, São Paulo - SP
                                <br>Telefone: (11)3031-8551
                                <br>www.watchtime.com.br
                                <br>sac-sp@watchtime.com.br
                            </p>"""
    elif data["loja"] == 'RJ':
        endereco =       """<p>Av. Rio branco, 123, 20 andar Cj 2012
                                <br>20040 - 905, Centro, Rio de Janeiro - RJ
                                <br>Telefone: (21)2526-7085
                                <br>www.watchtime.com.br
                                <br>sac@watchtime.com.br
                            </p>"""
    elif data["loja"] == 'PR':
        endereco =       """<p>Rua Comendador Araújo, 143 13 andar Cj 135
                                <br>80420 - 000, Centro, Curitiba - PR
                                <br>Telefone: (41)3322-1801
                                <br>www.watchtime.com.br
                                <br>sac-ctba@watchtime.com.br
                            </p>"""

    html_content = f"""
  <!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OS - Via Cliente</title>
    <link rel="stylesheet" href="https://app.watchtime.com.br/css/a4.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
        rel="stylesheet">
</head>

<body>
    <div class="page">

        <div class="header mb-5">
            <div class="container">
                <div class="row brand-e-os">
                    <div class="col-6">
                        <div class="brand">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                            <img class="locations" src="https://app.watchtime.com.br/assets/location-city.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6 os-content">
                        <p>Assistência Técnica</p>
                    </div>
                </div>
                <div class="row sub-header">
                    <div class="col-6">
                        <div class="endereco-2">
                            {endereco}
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="endereco-2 text-right float-r">
                            <p>Atendimento
                                <br>Das 10:00 às 17:00
                                <br>De 2ª a 6ª feira.
                                <br>Prazo do orçamento de 3 dias úteis (exceto relógios vintages).
                                <br>Prazo de retirada após conserto 10 dias.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="container info-client mb-3">
                <div class="row pb-3">
                    <div class="col-7 pr-1">
                        <div class="form-destaque">
                            <span>Cliente</span>
                            <p>{data['nome']}</p>
                        </div>
                    </div>
                    <div class="col-2 pl-1 pr-1">
                        <div class="form-destaque">
                            <span>Os Cliente</span>
                            <p>{data["os_loja"]}</p>
                        </div>
                    </div>
                    <div class="col-3 pl-1">
                        <div class="form-destaque">
                            <span>Ordem de serviço</span>
                            <p>{data["id"]}{data["brand_id"]}</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CNPJ / CPF</span>
                            <p>{data["documento"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">E-mail</span>
                            <p>{data["email"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Celular</span>
                            <p>{data["tel_celular"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Inscr / indentidade</span>
                            <p>{data["rg"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Telefone</span>
                            <p>{data["telefone"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Contato</span>
                            <p>{data["contato"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CEP</span>
                            <p>{data["cep"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Endereço</span>
                            <p>{data["logradouro"]}, {data["numero"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Complemento</span>
                            <p>{data["complemento"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Bairro</span>
                            <p>{data["bairro"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Cidade</span>
                            <p>{data["cidade"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Estado</span>
                            <p>{data["uf"]}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container info-produto">
                <div class="row">
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Informações do produto</h4>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card bg-gray b-0">
                                <div class="card-body">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Produto </h6>
                                            <h6 class="font-size-32 text-medium">{data["marca"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Modelo</h6>
                                            <h6 class="font-size-32 text-medium">{data["modelo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Referência</h6>
                                            <h6 class="font-size-32 text-medium">{data["referencia_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Série</h6>
                                            <h6 class="font-size-32 text-medium">{data["serie"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between">
                                            <h6 class="font-size-24 text-regular">Valor estimado</h6>
                                            <h6 class="font-size-32 text-medium">R$ {data["valor_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["nome_reparo"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card b-0">
                                <div class="card-body p-0">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido em</h6>
                                            <h6 class="font-size-32 text-medium">{data["data_os"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Portador</h6>
                                            <h6 class="font-size-32 text-medium">{data["portador"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido por</h6>
                                            <h6 class="font-size-32 text-medium">{data["tecnico_abertura"]} - {data["nome_tecnico"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["codigo_reparo"]} - {data["nome_reparo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Prazo de entrega</h6>
                                            <h6 class="font-size-32 text-medium">{data["prazo_entrega"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Data de análise</h6>
                                            <h6 class="font-size-32 text-medium">{data["data_analise"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Por</h6>
                                            <h6 class="font-size-32 text-medium">{data["tecnico_analise"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Diagnóstico</h6>
                                            <h6 class="font-size-32 text-medium">{data["diagnostico_tecnico"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Acessórios:</h6>
                            <p class="font-size-28b">{data["acessorios"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Defeito reportado:</h6>
                            <p class="font-size-28b">{data["defeito"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Detalhes:</h6>
                            <p class="font-size-28b">{data["detalhes"]}</p>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Observações:</h6>
                            <p class="font-size-28b">Todos os mecanismos de precisão requerem manutenção, e sua
                                frequência depende do modelo, do clima e das condições de uso.
                                Como regra geral, o seu relógio mecânico ou eletromecânico deve passar por uma revisão
                                {data["marca"]} completa a cada 4-6 anos.
                                Todo Relógio precisa passar pelo serviço de manutenção após 2 anos ou após um teste de
                                resistência à água sem sucesso.
                                Enquanto seu relógio estiver conosco, nossos habilidosos relojoeiros concentrarão toda
                                a sua atenção e sua energia à realização da manutenção.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="container">
                
                <div class="row pb-2">
                    <div class="col-12">
                        <div class="terms">
                            <p class="font-size-20 text-semibold pb-1">A AUTENTICIDADE DA MARCA OU PRODUTO SERÁ CONFIRMADA NO ATO DA
                                CONFECÇÃO DO ORÇAMENTO OU DA EXECUÇÃO DO SERVIÇO.</p>
                                
                            <p class="font-size-20 pb-1">As despesas de transporte e embalagem, bem como riscos e
                                seguro, para remessa e devolução do produto enviado para conserto, dentro ou fora da
                                garantia, são de responsabilidade do cliente.</p>

                            <p class="font-size-20 pb-1">Ao assinar a ordem de serviço estou de acordo com o uso e
                                guarda dos meus dados de acordo com a Lei Geral de Proteção de Dados (LGPD- Lei
                                13.709/2018). Autorizo também o uso e tratamento de dados para fins de manutenção de
                                cadastro por parte da empresa Watchtime e seus fornecedores.</p>

                            <p class="font-size-20">A devolução de quaisquer relógio por correios / transportadora obrigatoriamente será
                                feita com seguro contratado, com base no valor do relógio.</p>

                            <p class="font-size-20">Com o objetivo de garantir um serviço de excelência, informamos que qualquer intervenção
                                nos componentes poderá levar à sua deterioração e/ou destruição. Assim, o preço
                                aqui fornecido inclui a destruição por nossa parte de quaisquer dos componentes
                                substituídos, os quais são de nossa propriedade a partir do momento da sua substituição.
                                Ao aceitar este orçamento, o cliente renuncia irrevogavelmente qualquer direito de
                                devolução destes componentes. Isto também se aplica a reparações e/ou substituições
                                realizadas de forma gratuita dentro do prazo de garantia.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="row p-3 pt-2">
                    <div class="col-6 b-1 pt-1 pb-1 br-small">
                        <h6 class="font-size-28b text-medium">Importante</h6>
                        <p class="font-size-20">Só entregamos o relógio mediante a apresentação deste comprovante ou apresentação de documento de identidade original.</p>
                    </div>
                    <div class="col-6 b-1 pt-1 pb-1 bl-small">
                        <h6 class="font-size-28b text-medium">Atenção</h6>
                        <p class="font-size-20">Em caso de não comparecimento pessoal do contratante para a retirada do relógio, seu representante deverá comparecermunido de autorização expressa</p>
                    </div>
                </div>
                <div class="row pb-6 pt-5">
                    <div class="col-12">
                        <div class="signature">
                            <p class="font-size-32 w-50 m-auto text-medium bt-1">Assinatura</p>
                        </div>
                    </div>
                </div>



                <div class="row">
                    <div class="col-6">
                        <div class="d-flex">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="d-flex justify-content-end">
                            <span class="font-size-32 text-medium">{data["data_documento"]}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>
    """

    return{"html": html_content}


def generate_via_interna(codigo_estoklus,loja,id):
    data = get_os_completa(codigo_estoklus)[0]
    data["loja"] =loja
    data["id"]= id
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Via Interna</title>
    <link rel="stylesheet" href="https://app.watchtime.com.br/css/a4.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
        rel="stylesheet">
</head>

<body>
    <div class="page">

        <div class="header mb-5">
            <div class="container">
                <div class="row brand-e-os">
                    <div class="col-4">
                        <div class="brand">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg">
                            <p class="font-size-32 pl-4">Pronto: ______/______/______</p>
                        </div>
                    </div>
                    <div class="col-4 date">
                        <p class="font-size-32 align-items-center">Assistência Técnica</p>
                    </div>
                    <div class="col-4 os-content">
                        
                    </div>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="container info-client mb-3">
                <!-- Dados Principais -->
                <div class="row pb-3">
                    <div class="col-2 pr-1">
                        <div class="form-destaque">
                            <span class="small">Ordem de Serviço</span>
                            <p>{data["id"]}{data["brand_id"]}</p>
                        </div>
                    </div>
                    <div class="col-2 pl-1 pr-1">
                        <div class="form-destaque">
                            <span class="small">Data de Abertura</span>
                            <p>{data["data_os"]}</p>
                        </div>
                    </div>
                    <div class="col-5 pr-1">
                        <div class="form-destaque">
                            <span class="small">Cliente</span>
                            <p>{data["nome"]}</p>
                        </div>
                    </div>
                    <div class="col-2 pr-1">
                        <div class="form-destaque">
                            <span class="small">Nf Entrada</span>
                            <p>{data["nf_entrada"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-destaque">
                            <span class="small">OS da Loja</span>
                            <p>{data["os_loja"]}</p>
                        </div>
                    </div>

                </div>
                <!-- Dados pessoais -->
                <div class="row">
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CNPJ / CPF</span>
                            <p>{data["documento"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">E-mail</span>
                            <p>{data["email"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Celular</span>
                            <p>{data["tel_celular"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Inscr / indentidade</span>
                            <p>{data["rg"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Telefone</span>
                            <p>{data["telefone"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Contato</span>
                            <p>{data["contato"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CEP</span>
                            <p>{data["cep"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Endereço</span>
                            <p>{data["logradouro"]}, {data["numero"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Complemento</span>
                            <p>{data["complemento"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Bairro</span>
                            <p>{data["bairro"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Cidade</span>
                            <p>{data["cidade"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Estado</span>
                            <p>{data["uf"]}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container info-produto">
                <!-- Informações do produto -->
                <div class="row">
                    <!-- Titulo -->
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Informações do produto</h4>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card bg-gray b-0">
                                <div class="card-body">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Produto </h6>
                                            <h6 class="font-size-32 text-medium">{data["marca"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Modelo</h6>
                                            <h6 class="font-size-32 text-medium">{data["modelo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Referência</h6>
                                            <h6 class="font-size-32 text-medium">{data["referencia_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Série</h6>
                                            <h6 class="font-size-32 text-medium">{data["serie"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["codigo_reparo"]} - {data["nome_reparo"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card b-0">
                                <div class="card-body p-0">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido em</h6>
                                            <h6 class="font-size-32 text-medium">{data["data_os"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Portador</h6>
                                            <h6 class="font-size-32 text-medium">{data["portador"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido por</h6>
                                            <h6 class="font-size-32 text-medium">{data["tecnico_abertura"]} - {data["nome_tecnico"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Valor</h6>
                                            <h6 class="font-size-32 text-medium">{data["valor_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Prazo de entrega</h6>
                                            <h6 class="font-size-32 text-medium">{data["prazo_entrega"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Detalhes e observações -->
                <div class="row">
                    <!-- Titulo -->
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Detalhes e observações</h4>
                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Acessórios:</h6>
                            <p class="font-size-28b">{data["acessorios"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Defeito reportado:</h6>
                            <p class="font-size-28b">{data["defeito"]}</p>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Detalhes:</h6>
                            <p class="font-size-28b">{data["detalhes"]}</p>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Observação:</h6>
                            <p class="font-size-28b">{data["observacao"]}</p>
                        </div>
                    </div>
                </div>
				<br>
                <div class="signature">
                            <p class="font-size-32 w-50 m-auto text-medium bt-1">Assinatura</p>
                </div>
                <!-- Análise -->
                <div class="row">
                    <!-- Titulo -->
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Análise</h4>
                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Data da análise:</h6>
                            <p class="font-size-28b">{data["data_analise"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Pelo técnico:</h6>
                            <p class="font-size-28b">{data["tecnico_analise"]}</p>
                        </div>

                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Diagnóstico:</h6>
                            <p class="font-size-28b">{data["diagnostico_tecnico"]}</p>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Observação:</h6>
                            <p class="font-size-28b">{data["observacao_orcamento"]}</p>
                        </div>
                    </div>
                </div>
                <!-- Medidas -->
                <div class="row">
                    <!-- Titulo -->
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Medidas</h4>
                    </div>
                    <div class="col-3">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Cal:</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">E-Uni.Min. (V):</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">S-Uni.Min. (V):</h6>
                            <p class="font-size-28b">  </p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">E-Marcha (s/m):</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">S-Marcha (s/m):</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">E-Consumo (uA):</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">S-Consumo (uA):</h6>
                            <p class="font-size-28b"> </p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="list">
                            <div class="line mb-2">
                                <div class="number font-size-28b">1 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Revisão</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">2 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Mecanismo</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">3 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Circuito</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">4 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Mão de obra</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">5 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Coroa</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">6 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Tubo</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">7 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Pulsador</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">8 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Junta do vidro</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">9 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Junta do fundo</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">10 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Junta</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">11 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Junta</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">12 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Vidro</div>
                                <div class="border"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="list">
                            <div class="line mb-2">
                                <div class="number font-size-28b">13 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Mostrador</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">14 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Ponteiros(s)</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">15 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Pulseira</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">16 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Elo</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">17 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Pino de mola</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="number font-size-28b">18 - </div>
                                <div class="check font-size-28b">
                                    <p>(</p>
                                    <p>)</p>
                                </div>
                                <div class="name font-size-28b mr-1">Polimento</div>
                                <div class="border"></div>
                            </div>
                            <div class="line mb-2">
                                <div class="border"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>
"""
    

    
    return {"html": html_content}



def generate_orcamento_cliente(codigo_estoklus,loja,id):
    data = get_os_completa(codigo_estoklus)[0]
    data["loja"] =loja
    data["id"]= id
    if data["loja"] == 'SP':
        tel = '(11) 3031-8551'
    elif  data["loja"] == 'RJ':
        tel = '(21) 2526-7085'
    elif  data["loja"] == 'PR':
        tel = '(41) 3322-1801'
    else:
        tel = '(11) 3031-8551'
    obrigatorios = ''
    opcionais = ''
    desconto = ''
    desconto_opcionais = ''
    desconto_obrigatorios = ''
    if len(data["itens"]) > 9 or data["brand_id"] in ["CA", "MB", "BA"]:
        data["itens"] = [item for item in data["itens"] if item['valor_cliente'] != '0,00' or item["servico"] == 'S' ]
    valor_pago = f"""                                <div class="card-footer">
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                       <div class="title font-size-32 text-medium">Valor Pago</div>
                                        <div class="valot-total-op font-size-28 text-medium">R$ {data["valor_pago"]}</div>
                                    </div>
                                </div>""" if data["valor_pago"] != '0' else ''
    font = "font-size-36 text-medium"
    if len(data["itens"]) >9:
        font = "font-size-20 text-small"
    if data["desconto"] > 0:
        desconto = f'Desconto {round(data["desconto"],2)}%'
        desconto_opcionais = f'- R$ {data["desconto_opcionais"]}'
        desconto_obrigatorios = f'- R$ {data["desconto_obrigatorios"]}'
    for item in data["itens"]:
        if item["tipo"] == 'N':
            obrigatorios += f"""
<div class="d-flex align-items-start justify-content-between mb-1">
    <div class="quantidade {font} mr-1">{item["quantidade"]}</div>
    <div class="descrição {font}">{item["descricao"]}
    </div>
    <div class="valor {font}">{item["valor_cliente"]}</div>
</div>
"""
        else:
          opcionais += f"""
<div class="d-flex align-items-start justify-content-between mb-1">
    <div class="quantidade {font} mr-1">{item["quantidade"]}</div>
    <div class="descrição {font}">{item["descricao"]}
    </div>
    <div class="valor {font}">{item["valor_cliente"]}</div>
</div>
"""


    texto_orcamento = ''
    if data["intervencao"] == '1' and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Revisão Completa no Relógio Quartz
<br>Inclui: limpeza e lubrificação de todas as peças do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação e bateria"""
    elif data["intervencao"] in ['2','3'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Serviço Parcial do Relógio Quartz (MANUTENÇÃO: troca de bateria + vedações)
<br>Inclui: verificação da resistência à agua e substituição das juntas de vedação e bateria."""
    elif data["intervencao"] in ['8'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Troca da Máquina no Relógio Quartz
<br>Inclui: desmontagem e montagem do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação e bateria."""
    elif data["intervencao"] == '1' and data["tipo_mecanismo"] == '2':
        texto_orcamento = """<br>Revisão Completa no Relógio Automático
<br>Inclui: limpeza e lubrificação de todas as peças do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação."""
    elif data["intervencao"] in ['2','3'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Serviço Parcial do Relógio Automático (MANUTENÇÃO: troca de vedações)
<br>Inclui: verificação da resistência à agua e substituição das juntas de vedação."""

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orçamento Interno</title>
    <link rel="stylesheet" href="https://app.watchtime.com.br/css/a4.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
        rel="stylesheet">
</head>

<body>
    <div class="page">

        <div class="header mb-5">
            <div class="container">
                <div class="row brand-e-os">
                    <div class="col-6">
                        <div class="os-content">
                            <div class="os-numbers">
                                <div class="os-id">
                                    <span>Ordem de serviço</span>
                                    <p>{data["id"]}{data["brand_id"]}</p>
                                </div>
                                <div class="os-cliente">
                                    <span>Os Cliente</span>
                                    <p>{data["os_loja"]}</p>
                                </div>
                                <div class="os-cliente">
                                   <br>
                                    <p class="font-size-32-pt pl-4">Pronto: ______/______/______</p>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="col-6">
                        <div class="brand">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                            <img class="locations" src="https://app.watchtime.com.br/assets/location-city.svg" alt="">
                        </div>
                    </div>

                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="endereco">
                            <p class="font-size-36">{data["nome"]}
                                <br>{data["logradouro"]}, {data["numero"]} {data["complemento"]} 
                                <br>{data["cep"]}, {data["bairro"]}, {data["cidade"]}, {data["uf"]}
                                <br>{data["tel_celular"]} / {data["telefone"]} / {data["email"]}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="container">
                <div class="row">
                    <div class="col-6">
                        <!-- Informações do produto -->
                        <div class="info-produto mb-4">
                            <div class="card bg-gray b-0">
                                <div class="card-body">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list logo-relogio">
                                            <h6 class="font-size-24 text-regular">Marca</h6>
                                            <img src="https://app.watchtime.com.br/assets/{data["brand_id"]}.png" alt="">
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Produto</h6>
                                            <h6 class="font-size-32 text-medium">{data["marca"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Modelo</h6>
                                            <h6 class="font-size-32 text-medium">{data["modelo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Referência</h6>
                                            <h6 class="font-size-32 text-medium">{data["referencia_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Série</h6>
                                            <h6 class="font-size-32 text-medium">{data["serie"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Valor</h6>
                                            <h6 class="font-size-32 text-medium">R$ {data["valor_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["nome_reparo"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Peças e serviços indispensáveis. -->
                        <div class="servicos-indispensaveis pb-4">
                            <div class="card b-0">
                                <div class="card-body p-0 pb-1 bb-1">
                                    <div class="d-flex align-items-center justify-content-between mb-2">
                                        <div class="title font-size-32 text-medium">Peças e serviços indispensáveis.
                                        </div>
                                        <span class="tag text-bold bg-dark color-white p-1">Necessário</span>
                                    </div>
                                    <div class="list pb-1">

                                        <!-- Header Qtd, Descrição e Valor -->
                                        <div class="d-flex align-items-center justify-content-between mb-1">
                                            <div class="quantidade font-size-small mr-1">Qtd.</div>
                                            <div class="descrição font-size-small">Descrição</div>
                                            <div class="valor font-size-small">Valor</div>
                                        </div>

                                            {obrigatorios}

                                    </div>
                                </div>
                                <div class="card-footer">
                                    <!-- Total bruto e Valor -->
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                        <div class="total font-size-28">Total Indispensável Bruto</div>
                                        <div class="valot-total font-size-28 text-medium">R$ {data["bruto_obrigatorios"]}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Peças e serviços opcionais. -->
                        <div class="servicos-opcionais pb-1">
                            <div class="card b-0">
                                <div class="card-body p-0 pb-1 bb-1">
                                    <div class="d-flex align-items-center justify-content-between mb-2">
                                        <div class="title font-size-32 text-medium">Peças e serviços opcionais.</div>
                                        <span class="tag text-bold bg-white color-dark b-1 p-1">Estético</span>
                                    </div>
                                    <div class="list pb-1">

                                        <!-- Header Qtd, Descrição e Valor -->
                                        <div class="d-flex align-items-center justify-content-between mb-1">
                                            <div class="quantidade font-size-small mr-1">Qtd.</div>
                                            <div class="descrição font-size-small">Descrição</div>
                                            <div class="valor font-size-small">Valor</div>
                                        </div>

                                                {opcionais}

                                    </div>
                                </div>
                                <!-- Total bruto e Valor -->
                                <div class="card-footer">
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                        <div class="total font-size-28">Total Opcional bruto</div>
                                        <div class="valot-total-op font-size-28 text-medium">R$ {data["valor_opcionais"]}</div>
                                    </div>
                                </div>
                                {valor_pago}
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="info-detalhes">
                            <div class="card b-0">
                                <div class="card-body p-0">
                                    <div class="d-flex mb-3 w-100">
                                        <div class="recebido w-25">
                                            <h6 class="font-size-24 text-semibold mb-1">Recebido</h6>
                                            <p class="font-size-28b">{data["data_os"]}</p>
                                        </div>
                                        <div class="responsavel w-50">
                                            <h6 class="font-size-24 text-semibold mb-1">Por</h6>
                                            <p class="font-size-28b">{data["nome_tecnico"]}</p>
                                        </div>
                                        <div class="garantia-do-conserto w-25">
                                            <h6 class="font-size-24 text-semibold mb-1">Garantia do conserto</h6>
                                            <p class="font-size-28b">{data["garantia"]}</p>
                                        </div>
                                    </div>
                                    <div class="prazo-de-entrega mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Prazo de entrega</h6>
                                        <p class="font-size-28b">{data["prazo_entrega"]}</p>
                                    </div>
                                    <div class="condicoes-do-relogio mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Condições do relógio:</h6>
                                        <p class="font-size-28b">{data["detalhes"]}</p>
                                    </div>
                                    <div class="defeito-reportado mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Defeito reportado:</h6>
                                        <p class="font-size-28b">{data["defeito"]}</p>
                                    </div>
                                    <div class="observacoes mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Diagnóstico Técnico:</h6>
                                        <p class="font-size-28b">{data["diagnostico_tecnico"]}</p>
                                    </div>
                                    <div class="observacoes mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Observações:</h6>
                                        <p class="font-size-28b">Todos os mecanismos de precisão requerem manutenção, e sua frequência
                                            depende do modelo, do clima e das condições de uso.
                                            Como regra geral, o seu relógio mecânico ou eletromecânico deve passar por
                                            uma revisão {data["marca"]} completa a cada 4-6 anos.
                                            Todo Relógio precisa passar pelo serviço de manutenção após 2 anos ou após
                                            um teste de resistência à água sem sucesso.
                                            Enquanto seu relógio estiver conosco, nossos habilidosos relojoeiros
                                            concentrarão toda a sua atenção e sua energia à realização da manutenção.
                                            </p>
                                            <br/>
                                             <h6 class="font-size-24 text-semibold mb-1">Serviço:</h6>
                                            <p class="font-size-28b">
                                            {texto_orcamento}
                                            </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="container">

                <!-- Valor total e desconto dos serviços -->
                <div class="row mb-5">
                    <div class="col-12 p-0">
                        <div class="title font-size-32 text-medium mb-2">Selecione abaixo os serviços desejados:</div>
                    </div>
                    <!-- Total peças e serviços servicos-indispensaveis -->
                    <div class="col-6 b-1 br-small pt-2 pb-2">
                        <div class="card b-0">
                            <div class="card-body p-0 pb-1 bb-1">
                                <div class="d-flex align-items-start justify-content-between mb-1">
                                    <div class="font-size-28">Peças e serviços indispensáveis.</div>
                                    <div class="font-size-32 text-medium">R$ {data["bruto_obrigatorios"]}</div>
                                </div>
                                <div class="d-flex align-items-start justify-content-between">
                                    <div class="font-size-28">{desconto}</div>
                                    <div class="font-size-32 text-medium">{desconto_obrigatorios}</div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                    <div class="total">Total</div>
                                    <div class="valot-total font-size-44 text-medium">R$ {data["liquido_obrigatorios"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Todos indispensáveis de peças e serviços + opcionais. -->
                    <div class="col-6 b-1 bl-small pt-2 pb-2">
                        <div class="card b-0">
                            <div class="card-body p-0 pb-1 bb-1">
                                <div class="d-flex align-items-start justify-content-between mb-1">
                                    <div class="font-size-28">Todos indispensáveis de peças e serviços + opcionais.</div>
                                    <div class="font-size-32 text-medium">R$ {data["bruto_opcional"]}</div>
                                </div>
                                <div class="d-flex align-items-start justify-content-between">
                                    <div class="font-size-28">{desconto}</div>
                                    <div class="font-size-32 text-medium">{desconto_opcionais}</div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                    <div class="total">Total</div>
                                    <div class="valot-total font-size-44 text-medium">R$ {data["liquido_opcionais"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-5">
                    <div class="col-12">
                        <div class="terms mb-5 pb-5">
                            <p class="font-size-24b pb-1">Ao aceitar esse orçamento, estou de acordo com o uso e guarda dos meus dados de acordo com a Lei Geral de Proteção de Dados (LGPD-Lei 13.709/2018). Autorizo também o uso e tratamento de dados para fins de manutenção de cadastro por parte da empresa Watch Time e seus forncecedores.</p>
                            <p class="font-size-24b pb-1">** Importante: A devolução de quaisquer relógio por correios / transportadora obrigatóriamente será feita com seguro contratado, com base no valor do relógio.</p>
                            <p class="font-size-24b">Com o objetivo de garantir um serviço de excelência, informamos que qualquer intervenção nos componentes poderá levar à sua deterioração e/ou destruição. Assim, o preço aqui fornecido inclui a destruição por nossa parte de quaisquer dos componentes substituídos, os quais são de nossa propriedade a partir do momento da sua substituição. Ao aceitar este orçamento, o cliente renuncia irrevogavelmente qualquer direito de devolução destes componentes. Isto também se aplica a reparações e/ou substituições realizadas de forma gratuita dentro do prazo de garantia.</p>
                        </div>
                        <div class="signature">
                            <p class="font-size-32 w-50 m-auto text-medium bt-1">Assinatura</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="d-flex">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="d-flex justify-content-end">
                            <span class="font-size-32 text-medium">+55 {tel}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</body>

</html>"""
    

    return {"html": html}


def generate_orcamento_cliente_ci(codigo_estoklus,loja,id):
    data = get_os_completa(codigo_estoklus)[0]
    data["loja"] =loja
    data["id"]= id
    if data["loja"] == 'SP':
        tel = '(11) 3031-8551'
    elif  data["loja"] == 'RJ':
        tel = '(21) 2526-7085'
    elif  data["loja"] == 'PR':
        tel = '(41) 3322-1801'
    valor_pago = f"""                                <div class="card-footer">
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                       <div class="title font-size-32 text-medium">Valor Pago</div>
                                        <div class="valot-total-op font-size-28 text-medium">R$ {data["valor_pago"]}</div>
                                    </div>
                                </div>""" if data["valor_pago"] != '0' else ''
    obrigatorios = ''
    opcionais = ''
    desconto = ''
    desconto_opcionais = ''
    desconto_obrigatorios = ''
    if len(data["itens"]) > 9 or data["brand_id"] in ["CA", "MB", "BA"]:
        data["itens"] = [item for item in data["itens"] if item['valor_cliente'] != '0,00' or item["servico"] == 'S' ]

    font = "font-size-36 text-medium"
    if len(data["itens"]) >9:
        font = "font-size-20 text-small"
    if data["desconto"] > 0:
        desconto = f'Desconto {round(data["desconto"],2)}%'
        desconto_opcionais = f'- R$ {data["desconto_opcionais"]}'
        desconto_obrigatorios = f'- R$ {data["desconto_obrigatorios"]}'
    for item in data["itens"]:
        if item["tipo"] == 'N':
            obrigatorios += f"""
<div class="d-flex align-items-start justify-content-between mb-1">
    <div class="quantidade {font} mr-1">{item["quantidade"]}</div>
    <div class="descrição {font}">{item["descricao"]}
    </div>
    <div class="valor {font}">{item["valor_cliente"]}</div>
</div>
"""
        else:
          opcionais += f"""
<div class="d-flex align-items-start justify-content-between mb-1">
    <div class="quantidade {font} mr-1">{item["quantidade"]}</div>
    <div class="descrição {font}">{item["descricao"]}
    </div>
    <div class="valor {font}">{item["valor_cliente"]}</div>
</div>
"""


    texto_orcamento = ''
    if data["intervencao"] == '1' and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Revisão Completa no Relógio Quartz
<br>Inclui: limpeza e lubrificação de todas as peças do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação e bateria"""
    elif data["intervencao"] in ['2','3'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Serviço Parcial do Relógio Quartz (MANUTENÇÃO: troca de bateria + vedações)
<br>Inclui: verificação da resistência à agua e substituição das juntas de vedação e bateria."""
    elif data["intervencao"] in ['8'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Troca da Máquina no Relógio Quartz
<br>Inclui: desmontagem e montagem do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação e bateria."""
    elif data["intervencao"] == '1' and data["tipo_mecanismo"] == '2':
        texto_orcamento = """<br>Revisão Completa no Relógio Automático
<br>Inclui: limpeza e lubrificação de todas as peças do mecanismo, verificação dos parâmetros do movimento e suas funções, verificação da resistência à agua e substituição das juntas de vedação."""
    elif data["intervencao"] in ['2','3'] and data["tipo_mecanismo"] == '1':
        texto_orcamento = """<br>Serviço Parcial do Relógio Automático (MANUTENÇÃO: troca de vedações)
<br>Inclui: verificação da resistência à agua e substituição das juntas de vedação."""

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orçamento Interno</title>
    <link rel="stylesheet" href="https://app.watchtime.com.br/css/a4.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
        rel="stylesheet">
</head>

<body>
    <div class="page-2">
            <div class="image-left">
            <img src="https://app.watchtime.com.br/assets/imgv-1.png" alt="">
        </div>
        <div class="header mb-5">
            <div class="container">
                <div class="row brand-e-os">
                    <div class="col-6">
                        <div class="brand">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                            <img class="locations" src="https://app.watchtime.com.br/assets/location-city.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="os-content">
                            <div class="os-numbers">
                                <div class="os-cliente">
                                    <span>Os Cliente</span>
                                    <p>{data["os_loja"]}</p>
                                </div>
                                <div class="os-id">
                                    <span>Ordem de serviço</span>
                                    <p>{data["id"]}{data["brand_id"]}</p>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <div class="endereco">
                            <p class="font-size-36">{data["nome"]}
                                <br>{data["logradouro"]}, {data["numero"]} {data["complemento"]}
                                <br>{data["cep"]} {data["cidade"]}, {data["uf"]}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="container">
                <div class="row">
                    <div class="col-6">
                        <!-- Informações do produto -->
                        <div class="info-produto mb-4">
                            <div class="card bg-gray b-0">
                                <div class="card-body">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list logo-relogio">
                                            <h6 class="font-size-24 text-regular">Marca</h6>
                                            <img src="https://app.watchtime.com.br/assets/{data["brand_id"]}.png" alt="">
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Produto</h6>
                                            <h6 class="font-size-32 text-medium">{data["marca"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Modelo</h6>
                                            <h6 class="font-size-32 text-medium">{data["modelo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Referência</h6>
                                            <h6 class="font-size-32 text-medium">{data["referencia_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Série</h6>
                                            <h6 class="font-size-32 text-medium">{data["serie"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Valor</h6>
                                            <h6 class="font-size-32 text-medium">R$ {data["valor_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["nome_reparo"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Peças e serviços indispensáveis. -->
                        <div class="servicos-indispensaveis pb-4">
                            <div class="card b-0">
                                <div class="card-body p-0 pb-1 bb-1">
                                    <div class="d-flex align-items-center justify-content-between mb-2">
                                        <div class="title font-size-32 text-medium">Peças e serviços indispensáveis.
                                        </div>
                                        <span class="tag text-bold bg-dark color-white p-1">Necessário</span>
                                    </div>
                                    <div class="list pb-1">

                                        <!-- Header Qtd, Descrição e Valor -->
                                        <div class="d-flex align-items-center justify-content-between mb-1">
                                            <div class="quantidade font-size-small mr-1">Qtd.</div>
                                            <div class="descrição font-size-small">Descrição</div>
                                            <div class="valor font-size-small">Valor</div>
                                        </div>

                                            {obrigatorios}

                                    </div>
                                </div>
                                <div class="card-footer">
                                    <!-- Total bruto e Valor -->
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                        <div class="total font-size-28">Total Indispensável Bruto</div>
                                        <div class="valot-total font-size-28 text-medium">R$ {data["bruto_obrigatorios"]}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Peças e serviços opcionais. -->
                        <div class="servicos-opcionais pb-1">
                            <div class="card b-0">
                                <div class="card-body p-0 pb-1 bb-1">
                                    <div class="d-flex align-items-center justify-content-between mb-2">
                                        <div class="title font-size-32 text-medium">Peças e serviços opcionais.</div>
                                        <span class="tag text-bold bg-white color-dark b-1 p-1">Estético</span>
                                    </div>
                                    <div class="list pb-1">

                                        <!-- Header Qtd, Descrição e Valor -->
                                        <div class="d-flex align-items-center justify-content-between mb-1">
                                            <div class="quantidade font-size-small mr-1">Qtd.</div>
                                            <div class="descrição font-size-small">Descrição</div>
                                            <div class="valor font-size-small">Valor</div>
                                        </div>

                                                {opcionais}

                                    </div>
                                </div>
                                <!-- Total bruto e Valor -->
                                <div class="card-footer">
                                    <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                        <div class="total font-size-28">Total Opcional bruto</div>
                                        <div class="valot-total-op font-size-28 text-medium">R$ {data["valor_opcionais"]}</div>
                                    </div>
                                </div>

                                {valor_pago}
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="info-detalhes">
                            <div class="card b-0">
                                <div class="card-body p-0">
                                    <div class="d-flex mb-3 w-100">
                                        <div class="recebido w-25">
                                            <h6 class="font-size-24 text-semibold mb-1">Recebido</h6>
                                            <p class="font-size-28b">{data["data_os"]}</p>
                                        </div>
                                        <div class="responsavel w-50">
                                            <h6 class="font-size-24 text-semibold mb-1">Por</h6>
                                            <p class="font-size-28b">{data["nome_tecnico"]}</p>
                                        </div>
                                        <div class="garantia-do-conserto w-25">
                                            <h6 class="font-size-24 text-semibold mb-1">Garantia do conserto</h6>
                                            <p class="font-size-28b">{data["garantia"]}</p>
                                        </div>
                                    </div>
                                    <div class="prazo-de-entrega mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Prazo de entrega</h6>
                                        <p class="font-size-28b">{data["prazo_entrega"]}</p>
                                    </div>
                                    <div class="condicoes-do-relogio mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Condições do relógio:</h6>
                                        <p class="font-size-28b">{data["detalhes"]}</p>
                                    </div>
                                    <div class="defeito-reportado mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Defeito reportado:</h6>
                                        <p class="font-size-28b">{data["defeito"]}</p>
                                    </div>
                                    <div class="observacoes mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Diagnóstico Técnico:</h6>
                                        <p class="font-size-28b">{data["diagnostico_tecnico"]}</p>
                                    </div>
                                    <div class="observacoes mb-3">
                                        <h6 class="font-size-24 text-semibold mb-1">Observações::</h6>
                                        <p class="font-size-28b">Todos os mecanismos de precisão requerem manutenção, e sua frequência
                                            depende do modelo, do clima e das condições de uso.
                                            Como regra geral, o seu relógio mecânico ou eletromecânico deve passar por
                                            uma revisão {data["marca"]} completa a cada 4-6 anos.
                                            Todo Relógio precisa passar pelo serviço de manutenção após 2 anos ou após
                                            um teste de resistência à água sem sucesso.
                                            Enquanto seu relógio estiver conosco, nossos habilidosos relojoeiros
                                            concentrarão toda a sua atenção e sua energia à realização da manutenção.
                                            </p>
                                            <br/>
                                             <h6 class="font-size-24 text-semibold mb-1">Serviço:</h6>
                                            <p class="font-size-28b">
                                            {texto_orcamento}
                                            </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer-2">
            <div class="container">

                <!-- Valor total e desconto dos serviços -->
                <div class="row mb-5">
                    <div class="col-12 p-0">
                        <div class="title font-size-32 text-medium mb-2">Selecione abaixo os serviços desejados:</div>
                    </div>
                    <!-- Total peças e serviços servicos-indispensaveis -->
                    <div class="col-6 b-1 br-small pt-2 pb-2">
                        <div class="card b-0">
                            <div class="card-body p-0 pb-1 bb-1">
                                <div class="d-flex align-items-start justify-content-between mb-1">
                                    <div class="font-size-28">Peças e serviços indispensáveis.</div>
                                    <div class="font-size-32 text-medium">R$ {data["bruto_obrigatorios"]}</div>
                                </div>
                                <div class="d-flex align-items-start justify-content-between">
                                    <div class="font-size-28">{desconto}</div>
                                    <div class="font-size-32 text-medium">{desconto_obrigatorios}</div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                    <div class="total">Total</div>
                                    <div class="valot-total font-size-44 text-medium">R$ {data["liquido_obrigatorios"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Todos indispensáveis de peças e serviços + opcionais. -->
                    <div class="col-6 b-1 bl-small pt-2 pb-2">
                        <div class="card b-0">
                            <div class="card-body p-0 pb-1 bb-1">
                                <div class="d-flex align-items-start justify-content-between mb-1">
                                    <div class="font-size-28">Todos indispensáveis de peças e serviços + opcionais.</div>
                                    <div class="font-size-32 text-medium">R$ {data["bruto_opcional"]}</div>
                                </div>
                                <div class="d-flex align-items-start justify-content-between">
                                    <div class="font-size-28">{desconto}</div>
                                    <div class="font-size-32 text-medium">{desconto_opcionais}</div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex align-items-start justify-content-between mb-0 pt-2">
                                    <div class="total">Total</div>
                                    <div class="valot-total font-size-44 text-medium">R$ {data["liquido_opcionais"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-5">
                    <div class="col-12">
                        <div class="terms mb-5 pb-5">
                            <p class="font-size-24b pb-1">Ao aceitar esse orçamento, estou de acordo com o uso e guarda dos meus dados de acordo com a Lei Geral de Proteção de Dados (LGPD-Lei 13.709/2018). Autorizo também o uso e tratamento de dados para fins de manutenção de cadastro por parte da empresa Watch Time e seus forncecedores.</p>
                            <p class="font-size-24b pb-1">** Importante: A devolução de quaisquer relógio por correios / transportadora obrigatóriamente será feita com seguro contratado, com base no valor do relógio.</p>
                            <p class="font-size-24b">Com o objetivo de garantir um serviço de excelência, informamos que qualquer intervenção nos compoentes poderá levar à sua deterioração e/ou destruição. Assim, o preço aqui fornecido inclui a destruição por nossa parte de quaisquer dos componentes substituídos, os quais são de nossa propriedade a partir do momento da sua substituição. Ao aceitar este orçamento, o cliente renuncia irrevogavelmente qualquer direito de devolução destes componentes. Isto também se aplica a reparações e/ou substituições realizadas de forma gratuita dentro do prazo de garantia.</p>
                        </div>
                        <div class="signature">
                            <p class="font-size-32 w-50 m-auto text-medium bt-1">Assinatura</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="d-flex">
                          
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="d-flex justify-content-end">
                            <span class="font-size-32 text-medium">+55 {tel}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</body>

</html>"""

    return {"html": html}



def generate_html_via_cliente_ci(codigo_estoklus,loja,id):

    data = get_os_completa(codigo_estoklus)[0]
    data["loja"] =loja
    data["id"]= id
    if data["loja"] == 'SP':
        endereco =       """<p>Av Pedroso de Morais, 457 12 andar Cj 1202
                                <br>05419 - 000, Pinheiros, São Paulo - SP
                                <br>Telefone: (11)3031-8551
                                <br>www.watchtime.com.br
                                <br>sac-sp@watchtime.com.br
                            </p>"""
    elif data["loja"] == 'RJ':
        endereco =       """<p>Av. Rio branco, 123, 20 andar Cj 2012
                                <br>20040 - 905, Centro, Rio de Janeiro - RJ
                                <br>Telefone: (21)2526-7085
                                <br>www.watchtime.com.br
                                <br>sac@watchtime.com.br
                            </p>"""
    elif data["loja"] == 'PR':
        endereco =       """<p>Rua Comendador Araújo, 143 13 andar Cj 135
                                <br>80420 - 000, Centro, Curitiba - PR
                                <br>Telefone: (41)3322-1801
                                <br>www.watchtime.com.br
                                <br>sac-ctba@watchtime.com.br
                            </p>"""

    html_content = f"""
  <!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OS - Via Cliente</title>
    <link rel="stylesheet" href="https://app.watchtime.com.br/css/a4.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
        rel="stylesheet">
</head>

<body>
    <div class="page">
        <div class="image-top">
            <img src="https://app.watchtime.com.br/assets/img-1.png" alt="">
        </div>

        <div class="header mb-5 mt-large">
            <div class="container">
                <div class="row brand-e-os">
                    <div class="col-6">
                        <div class="brand">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                            <img class="locations" src="https://app.watchtime.com.br/assets/location-city.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6 os-content">
                        <p>Assistência Técnica</p>
                    </div>
                </div>
                <div class="row sub-header">
                    <div class="col-6">
                        <div class="endereco-2">
                            {endereco}
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="endereco-2 text-right float-r">
                            <p>Atendimento
                                <br>Das 10:00 às 17:00
                                <br>De 2ª a 6ª feira.
                                <br>Prazo do orçamento de 3 dias úteis (exceto relógios vintages).
                                <br>Prazo de retirada após conserto 10 dias.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main">
            <div class="container info-client mb-3">
                <div class="row pb-3">
                    <div class="col-7 pr-1">
                        <div class="form-destaque">
                            <span>Cliente</span>
                            <p>{data['nome']}</p>
                        </div>
                    </div>
                    <div class="col-2 pl-1 pr-1">
                        <div class="form-destaque">
                            <span>Os Cliente</span>
                            <p>{data["os_loja"]}</p>
                        </div>
                    </div>
                    <div class="col-3 pl-1">
                        <div class="form-destaque">
                            <span>Ordem de serviço</span>
                            <p>{data["id"]}{data["brand_id"]}</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CNPJ / CPF</span>
                            <p>{data["documento"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">E-mail</span>
                            <p>{data["email"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Celular</span>
                            <p>{data["tel_celular"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Inscr / indentidade</span>
                            <p>{data["rg"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Telefone</span>
                            <p>{data["telefone"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Contato</span>
                            <p>{data["contato"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">CEP</span>
                            <p>{data["cep"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Endereço</span>
                            <p>{data["logradouro"]}, {data["numero"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Complemento</span>
                            <p>{data["complemento"]}</p>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="form-default mb-1">
                            <span class="mb-small">Bairro</span>
                            <p>{data["bairro"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Cidade</span>
                            <p>{data["cidade"]}</p>
                        </div>
                        <div class="form-default mb-1">
                            <span class="mb-small">Estado</span>
                            <p>{data["uf"]}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container info-produto">
                <div class="row">
                    <div class="col-12 mb-2">
                        <h4 class="title font-size-40 text-semibold">Informações do produto</h4>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card bg-gray b-0">
                                <div class="card-body">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Produto </h6>
                                            <h6 class="font-size-32 text-medium">{data["marca"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Modelo</h6>
                                            <h6 class="font-size-32 text-medium">{data["modelo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Referência</h6>
                                            <h6 class="font-size-32 text-medium">{data["referencia_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Série</h6>
                                            <h6 class="font-size-32 text-medium">{data["serie"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between">
                                            <h6 class="font-size-24 text-regular">Valor estimado</h6>
                                            <h6 class="font-size-32 text-medium">R$ {data["valor_produto"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["nome_reparo"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="info-produto mb-4">
                            <div class="card b-0">
                                <div class="card-body p-0">
                                    <div class="list">
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido em</h6>
                                            <h6 class="font-size-32 text-medium">{data["data_os"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Portador</h6>
                                            <h6 class="font-size-32 text-medium">{data["portador"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Recebido por</h6>
                                            <h6 class="font-size-32 text-medium">{data["tecnico_abertura"]} - {data["nome_tecnico"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Tipo de reparo</h6>
                                            <h6 class="font-size-32 text-medium">{data["codigo_reparo"]} - {data["nome_reparo"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Prazo de entrega</h6>
                                            <h6 class="font-size-32 text-medium">{data["prazo_entrega"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Data de análise</h6>
                                            <h6 class="font-size-32 text-medium">{data["data_analise"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Por</h6>
                                            <h6 class="font-size-32 text-medium">{data["tecnico_analise"]}</h6>
                                        </div>
                                        <div class="d-flex align-items-center justify-content-between mb-list-2">
                                            <h6 class="font-size-24 text-regular">Diagnóstico</h6>
                                            <h6 class="font-size-32 text-medium">{data["diagnostico_tecnico"]}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Acessórios:</h6>
                            <p class="font-size-28b">{data["acessorios"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Defeito reportado:</h6>
                            <p class="font-size-28b">{data["defeito"]}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Detalhes:</h6>
                            <p class="font-size-28b">{data["detalhes"]}</p>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="mb-3">
                            <h6 class="font-size-24 text-semibold mb-1">Observações:</h6>
                            <p class="font-size-28b">Todos os mecanismos de precisão requerem manutenção, e sua
                                frequência depende do modelo, do clima e das condições de uso.
                                Como regra geral, o seu relógio mecânico ou eletromecânico deve passar por uma revisão
                                {data["marca"]} completa a cada 4-6 anos.
                                Todo Relógio precisa passar pelo serviço de manutenção após 2 anos ou após um teste de
                                resistência à água sem sucesso.
                                Enquanto seu relógio estiver conosco, nossos habilidosos relojoeiros concentrarão toda
                                a sua atenção e sua energia à realização da manutenção.
                                Serviço: {data["tipo_servico"]} - Intervenção:
                                • Substituição de componentes desgastados e defeituoso.
                                • Montagem e lubrificação dos componentes do movimento.
                                • Regulagem das funções.
                                • Controle de precisão do movimento.
                                • Verificação e controle minucioso de todas as funções durante 48 horas em várias
                                posições.
                                • Remontagem da caixa e substituição de todas as juntas de vedação.
                                • Teste de resistência à água de acordo com as especificações do modelo.
                                A intervenção e/ou peças são indispensáveis para um bom funcionamento do seu relógio!
                                * Substituição de qualquer componente de aço/metal ou vidro hesalite são cobrados
                                adicionalmente. *</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="container">
                
                <div class="row pb-2">
                    <div class="col-12">
                        <div class="terms">
                            <p class="font-size-20 text-semibold pb-1">A AUTENTICIDADE DA MARCA OU PRODUTO SERÁ CONFIRMADA NO ATO DA
                                CONFECÇÃO DO ORÇAMENTO OU DA EXECUÇÃO DO SERVIÇO.</p>
                                
                            <p class="font-size-20 pb-1">As despesas de transporte e embalagem, bem como riscos e
                                seguro, para remessa e devolução do produto enviado para conserto, dentro ou fora da
                                garantia, são de responsabilidade do cliente.</p>

                            <p class="font-size-20 pb-1">Ao assinar a ordem de serviço estou de acordo com o uso e
                                guarda dos meus dados de acordo com a Lei Geral de Proteção de Dados (LGPD- Lei
                                13.709/2018). Autorizo também o uso e tratamento de dados para fins de manutenção de
                                cadastro por parte da empresa Watchtime e seus fornecedores.</p>

                            <p class="font-size-20">A devolução de quaisquer relógio por correios / transportadora obrigatoriamente será
                                feita com seguro contratado, com base no valor do relógio.</p>

                            <p class="font-size-20">Com o objetivo de garantir um serviço de excelência, informamos que qualquer intervenção
                                nos componentes poderá levar à sua deterioração e/ou destruição. Assim, o preço
                                aqui fornecido inclui a destruição por nossa parte de quaisquer dos componentes
                                substituídos, os quais são de nossa propriedade a partir do momento da sua substituição.
                                Ao aceitar este orçamento, o cliente renuncia irrevogavelmente qualquer direito de
                                devolução destes componentes. Isto também se aplica a reparações e/ou substituições
                                realizadas de forma gratuita dentro do prazo de garantia.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="row p-3 pt-2">
                    <div class="col-6 b-1 pt-1 pb-1 br-small">
                        <h6 class="font-size-28b text-medium">Importante</h6>
                        <p class="font-size-20">Só entregamos o relógio mediante a apresentação deste comprovante ou apresentação de documento de identidade original.</p>
                    </div>
                    <div class="col-6 b-1 pt-1 pb-1 bl-small">
                        <h6 class="font-size-28b text-medium">Atenção</h6>
                        <p class="font-size-20">Em caso de não comparecimento pessoal do contratante para a retirada do relógio, seu representante deverá comparecermunido de autorização expressa</p>
                    </div>
                </div>
                <div class="row pb-6 pt-5">
                    <div class="col-12">
                        <div class="signature">
                            <p class="font-size-32 w-50 m-auto text-medium bt-1">Assinatura</p>
                        </div>
                    </div>
                </div>



                <div class="row">
                    <div class="col-6">
                        <div class="d-flex">
                            <img class="logo" src="https://app.watchtime.com.br/assets/logo-dark.svg" alt="">
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="d-flex justify-content-end">
                            <span class="font-size-32 text-medium">{data["data_documento"]}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>
    """

    return{"html": html_content}


def generate_receipt(os):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recibo</title>
<style>
  body {
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
  }
  .receipt-container {
    width: 100%;
    max-width: 300px; /* You might need to adjust this for your thermal printer width */
    margin: 0 auto;
  }
  .title {
    text-align: center;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .content-block {
    margin-bottom: 10px;
  }
  .total {
    font-weight: bold;
    border-top: 1px dashed #000;
    padding-top: 5px;
  }
</style>"""+f"""
</head>
<body>
<div class="receipt-container">
  <div class="title">RECIBO DE PAGAMENTO</div>
  <div class="content-block">
    <strong>Cliente</strong>
    <p>{os["nome"]}</p>
  </div>
  <div class="content-block">
    <strong>Ordem de serviço</strong>
    <p>{os["id"]}{os["brand_id"]}</p>
  </div>
  <div class="content-block">
    <strong>Data do pagamento</strong>
    <p>{os["data_pgto"]}</p>
  </div>
  <div class="content-block">
    <strong>Pagamento via {os["forma_pagto"]}</strong>
    <p>R$ {os["valor_pagamento"]}</p>
  </div>
  <div class="total">
    <strong>Total</strong>
    <p>R$ {os["valor_pagamento"]}</p>
  </div>
</div>
</body>
</html>"""
    
    return html
