from sre_constants import SUCCESS
import pytz
from datetime import datetime,timedelta
from models.estoklus import Estoklus,Estoklus1
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

def campo_auxiliar_os(codigo_campo,dado,nome_campo,os):
    estoklus = Estoklus()
    if(dado.get(nome_campo,'') != ''):
        if (estoklus.fetchone(f"select codigo_campo_auxiliar from E_ASSIST_TECNICA_CAMPO_AUXILIAR where codigo_os_assist_tecnica = {os} and codigo_campo_auxiliar = {codigo_campo}")):
            estoklus.update(f'E_ASSIST_TECNICA_CAMPO_AUXILIAR',['RESPOSTA'],[dado[nome_campo]],[f"codigo_os_assist_tecnica = {os} and codigo_campo_auxiliar = {codigo_campo}"],False)
        else: 
            estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',['CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'],[(codigo_campo,os,dado[nome_campo],'Cockpit')])
def campo_auxiliar_cg(codigo_campo,dado,nome_campo,cliente):
    estoklus = Estoklus()
    if(dado.get(nome_campo,'') != ''):
        if (estoklus.fetchone(f"select codigo_campo_auxiliar from g_cadastro_geral_campo_auxiliar where codigo_cadastro_geral = '{cliente}' and codigo_campo_auxiliar = {codigo_campo}")!= None):
            estoklus.update(f'g_cadastro_geral_campo_auxiliar',['RESPOSTA'],[dado[nome_campo]],[f"codigo_cadastro_geral = '{cliente}' and codigo_campo_auxiliar = {codigo_campo}"],False)
        else: 
            estoklus.insert('g_cadastro_geral_campo_auxiliar',['CODIGO_CAMPO_AUXILIAR','codigo_cadastro_geral','RESPOSTA','INCLUSAO_POR'],[(codigo_campo,cliente,dado[nome_campo],'Cockpit')])
def atualizar_preco(codigo_produto,valor,tipo):
    estoklus = Estoklus()
    if(valor != '0'):
        if (estoklus.fetchone(f"select preco from e_produto_preco where codigo_produto = {codigo_produto} and codigo_tipo_preco = {tipo}")):
            estoklus.update(f'e_produto_preco',['preco'],[valor],[f"codigo_produto = {codigo_produto} and codigo_tipo_preco = {tipo}"],False)
        else: 
            estoklus.insert('e_produto_preco',['codigo_produto','codigo_tipo_preco','preco','INCLUSAO_POR'],[(codigo_produto,tipo,valor,'Cockpit')])
def atualizar_descricao(codigo_produto,descricao):
    estoklus = Estoklus()
    estoklus.update(f'e_produto',['DESCRICAO_PRODUTO'],[descricao],[f"codigo_produto = {codigo_produto}"],False)


def criar_os_estoklus(os):

    required_fields = ['estoklus_id', 'cliente_id', 'tipo_reparo', 'modelo', 'descricao', 'defeito', 'loja', 'referencia_produto', 'brand_id', 'marca']
    validation = []

    for field in required_fields:
        if field not in os:
            validation.append(field)

    if validation:
        return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}



    produtos_os = [
{"code":"0021774","marca":"Alpina","id":"AL"},
{"code":"0178357","marca":"AP","id":"AU"},
{"code":"0067866","marca":"Baume","id":"BA"},
{"code":"0174143","marca":"Breguet","id":"BR"},
{"code":"0208523","marca":"Breitling","id":"BE"},
{"code":"0178446","marca":"Bvlgari","id":"BV"},
{"code":"0067864","marca":"Cartier","id":"CA"},
{"code":"0178454","marca":"Chopard","id":"CH"},
{"code":"0172014","marca":"Diversas","id":""},	
{"code":"0021736","marca":"Frederique C.","id":"FC"},
{"code":"0178390","marca":"Graham","id":"GR"},
{"code":"0020646","marca":"Hamilton","id":"HA"},
{"code":"0174093","marca":"Hublot","id":"HU"},
{"code":"0130880","marca":"IWC","id":"IW"},
{"code":"0178365","marca":"JLC","id":"JC"},
{"code":"0018643","marca":"Longines","id":"LO"},
{"code":"0174086","marca":"Mido","id":"MI"},
{"code":"0067867","marca":"Montblanc","id":"MB"},
{"code":"0174111","marca":"Omega","id":"OM"},
{"code":"0130766","marca":"Panerai","id":"OP"},
{"code":"0178373","marca":"Parmigiani","id":"PA"},
{"code":"0154240","marca":"Piaget","id":"PI"},
{"code":"0018644","marca":"Rado","id":"RA"},
{"code":"0174969","marca":"Swatch","id":"SW"},
{"code":"0178489","marca":"TAG Heuer","id":"TH"},
{"code":"0174079","marca":"Tissot","id":"TI"},
{"code":"0174129","marca":"Ulysse Nardin","id":"UL"},
{"code":"0149147","marca":"Vacheron","id":"VC"},
{"code":"0178411","marca":"Zenith","id":"ZE"}]
    
    for item in produtos_os:
        if item["id"] == os["brand_id"]:
            os["codigo_produto"] = item["code"]
        
    if os.get('codigo_produto','') == '':
        os["codigo_produto"] = '0172014'

    if os.get('serie','') == '':
        os["serie"] = ''
     
    estoklus = Estoklus()
    codigo_os = estoklus.fetchone("select GEN_ID(GEN_E_ASSIST_TECNICA,1) from RDB$DATABASE")    
    valores_os = [(codigo_os,
               os["estoklus_id"],
               os["cliente_id"],
               os["tipo_reparo"],
               os.get("os_loja",''),
               os["modelo"],
               os["serie"],
               os["descricao"],
               os.get("acessorios",''),
               os["defeito"],
               os.get("observacao",''),
               os.get("valor_produto",0),
               '01',
               os["loja"],
               os["estoklus_id"],
                1,
               'today',
               os["referencia_produto"],
               os["brand_id"],
               'now',
               os["marca"],
               os["codigo_produto"])]
    colunas_os = ['CODIGO_OS_ASSIST_TECNICA',
                  'TECNICO_RESPONSAVEL',
                  'CODIGO_CLIENTE',
                  'TIPO_REPARO',
                  'REFERENCIA_OS_CLIENTE',
                  'MODELO',
                  'SERIE',
                  'DETALHES',
                  'ACESSORIOS',
                  'DEFEITO',
                  'OBSERVACAO_PRODUTO',
                  'VALOR_PRODUTO',
                  'STATUS_OS',
                  'LOJA_OS',
                  'INCLUSAO_POR',
                  'FASE_ATUAL',
                  'DATA_OS',
                  'REFERENCIA_PRODUTO',
                  'GRUPO_OS_ASSIST_TECNICA',
                  'inclusao_data','produto','codigo_produto']
    estoklus.insert('E_ASSIST_TECNICA',colunas_os,valores_os)
    #campos auxiliares
    if (os.get("codigo_rastreio",'') != ''):
        estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',('CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'),[(3,codigo_os,os["codigo_rastreio"],'Cockpit')])
    if (os.get("os_loja_anterior",'') != ''):
        estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',['CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'],[(8,codigo_os,os["os_loja_anterior"],'Cockpit')])
    if (os["tipo_reparo"] != 9):
         campo_auxiliar_os(12,os,'calibre',codigo_os) 
         campo_auxiliar_os(56,os,'tipo_movimento',codigo_os) 
         campo_auxiliar_os(57,os,'complicacao',codigo_os)
    if (os.get("nf_entrada",'') != ''):
        estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',['CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'],[(5,codigo_os,os["nf_entrada"],'Cockpit')])    
    campo_auxiliar_os(9,os,'data_nf',codigo_os)
    campo_auxiliar_os(87,os,'codigo_produto_nf',codigo_os)
    #TAG HEUER
    if os["brand_id"] == 'TH':
        estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',['CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'],[(20,codigo_os,os["defect_tag"],'Cockpit')])
        if os["tipo_reparo"]== 2 or os["tipo_reparo"] == 7:  
           campo_auxiliar_os(24,os,'warranty_tag',codigo_os) 
           campo_auxiliar_os(25,os,'country_tag',codigo_os) 

    
    #Breitling         
    elif os["brand_id"] == 'BE':
        campo_auxiliar_os(32,os,'tracking_id_breitling',codigo_os)
        campo_auxiliar_os(29,os,'defect_bre',codigo_os)
        
        if os["tipo_reparo"] == 2 or os["tipo_reparo"] == 7:
            campo_auxiliar_os(31,os,'ultimo_conserto_bre',codigo_os)
            campo_auxiliar_os(30,os,'pais_bre',codigo_os)
            campo_auxiliar_os(2,os,'data_compra_bre',codigo_os)
        if os["tipo_reparo"] == 9:
            estoklus.insert('E_ASSIST_TECNICA_CAMPO_AUXILIAR',['CODIGO_CAMPO_AUXILIAR','CODIGO_OS_ASSIST_TECNICA','RESPOSTA','INCLUSAO_POR'],[(46,codigo_os,'S','Cockpit')])
    elif os["brand_id"] == 'BV':
        campo_auxiliar_os(34,os,'codigo_sap_bv',codigo_os)
        campo_auxiliar_os(36,os,'codigo_v02_bv_1',codigo_os)
        campo_auxiliar_os(35,os,'codigo_v02_bv_2',codigo_os)
        campo_auxiliar_os(37,os,'codigo_v01_bv_1',codigo_os)
        campo_auxiliar_os(38,os,'codigo_v01_bv_2',codigo_os)


    return {"success":str(os["loja"])+str(codigo_os)}



def gerar_nf_entrada(os,sTipoEntradaSaida):
    if os["tipo_reparo"] != 9 and os.get("nf_entrada",'') == '':
        loja=os["loja"]
        valor = os["valor_produto"]
        cliente_id = os["cliente_id"]
        estoklus = Estoklus()
        codigo_nf = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_REGISTRO_NF_C,1) from RDB$DATABASE") 
        sOrigemControle = 'NF08'
        cg_loja = "'*L-"+os["loja"]+"'"
        if sTipoEntradaSaida == 'E':
            movimento = '91'
            cfop = estoklus.fetchone("""select CASE WHEN CG.UF = CG1.UF THEN '1915'
ELSE '2915'  end

from g_cadastro_geral cg
left join g_cadastro_geral cg1 on cg.codigo_cadastro_geral = '"""+cliente_id+"""' and cg1.codigo_cadastro_geral = """+cg_loja+

""" where cg.codigo_cadastro_geral = '"""+ cliente_id +"""' AND CG1.codigo_cadastro_geral = """+cg_loja)
        else:
            movimento= '90'
            cfop = estoklus.fetchone("""select CASE WHEN CG.UF = CG1.UF THEN '5916'
ELSE '6916'  end

from g_cadastro_geral cg
left join g_cadastro_geral cg1 on cg.codigo_cadastro_geral = '"""+cliente_id+"""' and cg1.codigo_cadastro_geral = """+cg_loja+

""" where cg.codigo_cadastro_geral = '"""+ cliente_id +"""' AND CG1.codigo_cadastro_geral = """+cg_loja)

    
        textonf = """RELÓGIO """+os["marca"]+""" REFERÊNCIA: """+os["referencia_produto"]+' SÉRIE: '+os["serie"]+' MODELO:'+os["modelo"]+' OS: '+os["id"]

        querycfop ="""Select First 1
    Trim(cfop.descricao_cfop) 
  From E_CFOP cfop
  Where cfop.codigo_cfop = 1915"""
        natureza = estoklus.fetchone(querycfop)
        natureza = natureza.strip()
        if loja == 'PR':
            cst = '50'
            informacoes_complementares = """Suspensão nos termos do o artigo 334 do RICMS/PR"""
        if loja== 'SP':
            cst = '41'
            informacoes_complementares = """Sem incidência do ICMS, conforme artigo 7°, inciso X, do RICMS/SP."""
        if loja =='RJ':
            cst = '50'
            informacoes_complementares = """Suspensão nos termos do inciso I do artigo 52º do Livro I Decreto 27.427/00 - RICMS/RJ"""
        proxima_nf = estoklus.fetch_from_stored_proc('retornar_numero_nf',loja,'02')
        proxima_nf = proxima_nf[0][2]

        campos_insert = ['codigo_registro_nf_controle', 'codigo_loja', 'codigo_loja_fiscal', 'numero_nf_controle',
                                     'serie', 'data', 'e_s', 'codigo_tipo_movimento', 'codigo_cfop', 'natureza_operacao',
                                     'valor_total_produto', 'base_icms', 'valor_icms', 'base_icms_substituicao',
                                     'valor_icms_substituicao', 'valor_ipi', 'base_iss', 'valor_iss', 'valor_frete', 'valor_seguro',
                                     'valor_outras_despesas', 'valor_total_nf', 'percentual_desconto', 'valor_desconto',
                                     'codigo_vendedor', 'cancelada', 'codigo_cadastro_geral', 'tipo_frete', 'observacao_corpo_nota',
                                     'informacoes_complementares', 'codigo_transportador', 'placa_veiculo', 'uf_veiculo',
                                     'quantidade', 'especie', 'marca', 'numero', 'peso_bruto', 'peso_liquido', 'incide_icms_frete',
                                     'incide_icms_seguro', 'incide_icms_outras_despesas', 'origem_nf_controle', 'perc_desconto_2',
                                     'valor_desconto_2', 'consumidor_final', 'indicador_presenca',
                                     'frete_terceirizado', 'nfe_finalidade',
                                     'chave_acesso_nf_e', 'base_ipi', 'base_cofins', 'base_pis',
                                     'valor_cofins', 'valor_pis', 'base_ii', 'valor_ii',
                                    'hora_emissao',  
                                     'inclusao_data', 'inclusao_por']
        valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                       '02','today',sTipoEntradaSaida,movimento,cfop,natureza,
                       valor,0,0,0,
                       0,0,0,0,0,0,
                       0,valor,0,0,
                       '','N',cliente_id,9,'',
                       informacoes_complementares,'','','',
                       0,'','','',0,0,'N',
                       'N','N',sOrigemControle,0,
                       0,'1','9',
                       'N','1',
                       '',0,0,0,
                       0,0,0,0,
                       'now',
                       'now','COCKPIT')]
        estoklus.insert('e_registro_nf_controle',campos_insert,valores_insert)

        referencia_produto = os["referencia_produto"]
        os_nro = int(os["id"].lstrip(os["id"][0:2]))
        campos_insert_mes =['codigo_movimento_es', 'e_s', 'codigo_tipo_movimento', 'data_Movimento_es', 'codigo_loja',
                              'codigo_produto', 'codigo_cor', 'codigo_tamanho', 'quantidade', 'observacao', 'preco', 'codigo_loja_1',
                              'codigo_serie', 'numero_nf_controle', 'codigo_registro_nf_controle', 'codigo_cfop',
                              'codigo_classificacao_fiscal', 'codigo_situacao_tributaria', 'codigo_cadastro_geral',
                              'codigo_vendedor', 'preco_custo', 'valor_unitario', 'valor_desconto', 'icms_percentual',
                              'ipi_percentual', 'valor_rateio_frete', 'valor_rateio_Seguro', 'valor_rateio_outros_custos_1',
                              'valor_rateio_outros_custos_2', 'codigo_pedido_venda', 'codigo_pedido_venda_item',
                              'codigo_romaneio', 'codigo_romaneio_item', 'movimento_cancelado', 'movimento_altera_estoque',
                              'cfop_altera_estoque', 'codigo_unidade', 'valor_desconto_nota', 'preco_desconto_especial',
                              'base_calculo_icms', 'aliquota_icms_st_mva', 'base_ipi', 'aliquota_cofins', 'valor_cofins',
                              'base_cofins', 'aliquota_pis', 'valor_pis', 'base_pis', 'aliquota_credito_icms',
                              'valor_credito_icms', 'valor_ipi', 'valor_icms', 'aliquota_ii', 'valor_ii', 'base_ii',
                              'codigo_cst_origem', 'codigo_cst_icms', 'codigo_cst_csosn', 'codigo_cst_ipi', 'codigo_cst_pis',
                              'codigo_cst_cofins', 'base_icms_st', 'aliq_icms_st', 'valor_icms_st', 'movimento_veio_sate',
                              'codigo_loja_fiscal','diferimento_icms', 'diferimento_icms_valor', 'vbcfcp', 'pfcp', 'vfcp', 'vbcfcpst', 'pfcpst',
                              'vfcpst', 'modbc', 'predbc', 'valor_icms_deson',

                              'inclusao_data', 'inclusao_por','descricao_tipo_item','codigo_os_assist_tecnica']
    
        codigo_mes = estoklus.fetchone("select GEN_ID(GEN_E_codigo_movimento_es,1) from RDB$DATABASE") 
        valores_insert_mes = [(codigo_mes,sTipoEntradaSaida,movimento,'today',loja,'95','','',1,referencia_produto,valor,loja,'02',proxima_nf,codigo_nf,cfop,'91119090','400',cliente_id,'',0,valor,0,0,0,0,0,0,0,0,0,0,0,'N','N','N','UN',0,0,
                           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'0',cst,'','99','99','99',0,0,0,'N',loja,0,0,0,0,0,0,0,0,0,0,0,'now','Cockpit',textonf,os_nro)]
    
        estoklus.insert('e_movimento_es',campos_insert_mes,valores_insert_mes)
        return str(codigo_nf)




def atualizar_cliente_estoklus(cliente):
    estoklus=Estoklus()

    existe = estoklus.fetchall("select 'ok' from g_cadastro_geral where codigo_cadastro_geral = '"+cliente["cliente_id"]+"'")

    if not existe: 
        return {"error":'Cliente não encontrado'}
    data_formatada = ''
    if (cliente.get("nascimento")!= ''):
        data_datetime = datetime.strptime(cliente["nascimento"], "%Y-%m-%d")
        data_formatada = data_datetime.strftime("%d/%m/%Y")
    colunas_update = ['nome', 'logradouro',
                                     'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
                                     'tel_trabalho', 'tel_celular', 'tel_residencial', 'email',
                                     'nascimento', 'cpf', 'cnpj', 'alteracao_data', 'alteracao_por',
                                     'codigo_tipo_pessoa','codigo_ibge_municipio']
    
    valores_update= [cliente["nome"],
                      cliente["logradouro"],
                      cliente["numero"],
                      cliente.get("complemento",''),
                      cliente["bairro"],
                      cliente["cidade"],
                      cliente["uf"],
                      cliente["cep"],
                      cliente.get("tel_trabalho",''),
                      cliente.get("tel_celular",''),
                      cliente.get("tel_residencial",''),
                      cliente["email"],
                      data_formatada,
                      cliente.get("cpf",''),
                      cliente.get("cnpj",''),
                      'now',
                      cliente["estoklus_id"],
                      cliente["tipo_pessoa"],
                      cliente["codigo_ibge"],
                      ]
    
    estoklus.update('g_cadastro_geral',colunas_update,valores_update,["codigo_cadastro_geral = '"+cliente["cliente_id"]+"'"],True)
    campo_auxiliar_cg(2,cliente,'tipo_contato',cliente["cliente_id"])


    return {'success':str(cliente["cliente_id"])}

def criar_cliente_estoklus(cliente):
    estoklus=Estoklus()

    if cliente["tipo_pessoa"] == 'F':
        existe = estoklus.fetchall("select 'ok' from g_cadastro_geral where cpf = '"+cliente["cpf"]+"'")
    else:
        existe = estoklus.fetchall("select 'ok' from g_cadastro_geral where cnpj = '"+cliente["cnpj"]+"'")

    if existe: 
        return None
    
    data_datetime = datetime.strptime(cliente["nascimento"], "%Y-%m-%d")
    data_formatada = data_datetime.strftime("%d/%m/%Y")

    id_cliente = estoklus.fetchone("select GEN_ID(gen_g_cadastro_geral,1) from RDB$DATABASE")
    campos_insert = ['codigo_cadastro_geral', 'codigo_tipo', 'nome', 'logradouro',
                                     'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
                                     'tel_trabalho', 'tel_celular', 'tel_residencial', 'email',
                                     'nascimento', 'cpf', 'cnpj', 'inclusao_data', 'inclusao_por', 'usuario_responsavel',
                                     'email_nfe', 'ativo', 'codigo_ibge_municipio', 'codigo_tipo_pessoa',
                                     'credito_liberado']
    
    valores_insert= [(id_cliente,
                      'I',
                      cliente["nome"],
                      cliente["logradouro"],
                      cliente["numero"],
                      cliente.get("complemento",''),
                      cliente["bairro"],
                      cliente["cidade"],
                      cliente["uf"],
                      cliente["cep"],
                      cliente.get("tel_trabalho",''),
                      cliente.get("tel_celular",''),
                      cliente.get("tel_residencial",''),
                      cliente["email"],
                      data_formatada,
                      cliente.get("cpf",''),
                      cliente.get("cnpj",''),
                      'now',
                      cliente["estoklus_id"],
                      cliente["estoklus_id"],
                      cliente["email"],
                      'S',
                      cliente["codigo_ibge"],
                      cliente["tipo_pessoa"],
                      'S'
                      )]
    
    estoklus.insert('g_cadastro_geral',campos_insert,valores_insert)
    campo_auxiliar_cg(2,cliente,'tipo_contato',id_cliente)

    return str(id_cliente)


def tracking_id(cliente):
    query ="select resposta from g_cadastro_geral_campo_auxiliar gr where codigo_cadastro_geral = '"+cliente+"' and  gr.codigo_campo_auxiliar='003'"

    estoklus = Estoklus()

    result = estoklus.fetchone(query)

    if not (result):
        return {"data": ''}
    else:
        return {"data": result}
    



           
def inserir_orcamento(orcamento):

    required_fields = ['itens',  'serie', 'estoklus_id', 'loja', 'referencia_produto', 'estoklus_id', 'id']
    required_fields_item = ['tipo', 'id', 'label', 'referencia', 'quantidade', 'preco_venda']
    validation = []
    for field in required_fields:
        if field not in orcamento:
            validation.append(field) 

    # Obtém a data e hora atual
    data_atual = datetime.now()

    # Soma 45 dias à data atual
    nova_data = data_atual + timedelta(days=int(orcamento["prazo"]))

    # Formata a nova data como desejar
    data_formatada = nova_data.strftime("%m/%d/%Y")


    if validation:
        return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}



    estoklus=Estoklus()
    
    campos_insert =['CODIGO_PECAS_SERVICOS','CODIGO_OS_ASSIST_TECNICA','PECA_OU_SERVICO','CODIGO_PRODUTO',
                     'DESCRICAO','REFERENCIA_FORNECEDOR','UNIDADE','QTDE','VALOR_UNITARIO','GARANTIA','INCLUSAO_DATA','INCLUSAO_POR','CODIGO_LOJA_BAIXA','EXTRA','APROVADO']
    ##VALIDAÇÃO
    os = orcamento["id"].lstrip(orcamento["id"][0:2])
    estoklus.delete_from_table('e_assist_tecnica_pecas_servicos',f'codigo_os_assist_tecnica = {os}')
    for item in orcamento["itens"]:
        for field in required_fields_item:
            if field not in item:
                validation.append(field)
        if validation:
            return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}

    ##INSERÇÃO DOS ITENS

    for item in orcamento["itens"]:

        if item["tipo"]== 'S':
            tipo_peca = 'S'
            extra = 'N'
            garantia = 'N'
        elif item["tipo"]== 'I':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'S'

        elif item["tipo"]== 'P':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'N'

        elif item["tipo"]== 'OP':
            tipo_peca = 'P'
            extra = 'O'
            garantia = 'N'   

        if item["tipo"]== 'SO':
            tipo_peca = 'S'
            extra = 'O'
            garantia = 'N'

        elif item["tipo"]== 'G':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'N'
        
        id_peca = estoklus.fetchone("select GEN_ID(gen_e_pecas_servicos,1) from RDB$DATABASE")
        valores_insert= [(id_peca,
                      os,
                      tipo_peca,
                      item["id"],
                      item["label"],
                      item["referencia"],
                      'UN',
                      item["quantidade"],
                      item["preco_venda"],
                      garantia,
                      'now',
                      orcamento["estoklus_id"],
                      orcamento["loja"],
                      extra,
                      'S'
                      )]
        
        ##ATUALIZAÇÃO PREÇOS

        #if orcamento["editado"] == 'S' and tipo_peca == 'P':
        #    atualizar_preco(item["id"],item["preco_venda"],'001')
        #    atualizar_preco(item["id"],item["preco_custo"],'D')
    
        estoklus.insert('E_ASSIST_TECNICA_PECAS_SERVICOS',campos_insert,valores_insert)

    ##ATUALIZAÇÃO DA CAPA
    data_analise = estoklus.fetchone(f"select data_analise from e_assist_tecnica where codigo_os_assist_tecnica = {os}")
    if data_analise == None:
        data_analise = 'today'    
    if orcamento["total_bruto"] > 0:
        colunas_update = ['modelo','referencia_produto', 'serie',
                                         'fase_atual', 'status_os', 'data_analise', 'tecnico_analise','observacao_analise',
                                         'data_prevista_entrega','diagnostico','valor_desconto','margem_wt','custo_total','margem_opcionais','lucro_opcional','lucro_obrigatorio','tipo_reparo','alteracao_data','alteracao_por','FASE1_ALTERACAO_DATA','FASE1_ALTERACAO_POR','aprovado','observacao_aprovacao']

        valores_update= [orcamento["modelo"],
            orcamento["referencia_produto"],
                          orcamento["serie"],
                          2,
                          '09',
                          data_analise,
                          orcamento["estoklus_id"],
                          '',
                          data_formatada,
                            orcamento.get("diagnostico_tecnico",''),
                            orcamento.get("valor_desconto_todos",0),
                            orcamento.get('valor_margem_obrigatorios',0),
                            orcamento.get('custo_total',0),
                            orcamento.get('valor_margem',0),
                            orcamento.get('valor_liquido',0),
                            orcamento.get('valor_liquido_obrigatorios',0),
                            orcamento["tipo_reparo"],
                            'now',
                            orcamento["estoklus_id"],
                            'now',
                            orcamento["estoklus_id"],
                            '',
                            ''
                          ]

        estoklus.update('e_assist_tecnica',colunas_update,valores_update,["codigo_os_assist_tecnica = "+os+""],True)
    else:       
        colunas_update = ['modelo','referencia_produto', 'serie',
                                         'fase_atual', 'status_os', 'data_analise', 'tecnico_analise','observacao_analise',
                                         'data_prevista_entrega','diagnostico','valor_desconto','margem_wt','custo_total','margem_opcionais','lucro_opcional','lucro_obrigatorio','tipo_reparo','alteracao_data','alteracao_por','FASE1_ALTERACAO_DATA','FASE1_ALTERACAO_POR',
                                         'aprovado','data_aprovado','FASE2_ALTERACAO_DATA','OBSERVACAO_APROVACAO','FASE2_ALTERACAO_POR']

        valores_update= [orcamento["modelo"],
            orcamento["referencia_produto"],
                          orcamento["serie"],
                          4,
                          '05',
                          'today',
                          orcamento["estoklus_id"],
                          '',
                          data_formatada,
                            orcamento.get("diagnostico_tecnico",''),
                            orcamento.get("valor_desconto_todos",0),
                            orcamento.get('valor_margem_obrigatorios',0),
                            orcamento.get('custo_total',0),
                            orcamento.get('valor_margem',0),
                            orcamento.get('valor_liquido',0),
                            orcamento.get('valor_liquido_obrigatorios',0),
                            orcamento["tipo_reparo"],
                            'now',
                            orcamento["estoklus_id"],
                            'now',
                            orcamento["estoklus_id"],
                            'S',
                            'today',
                            'today',
                            'Aprovado pela Garantia',
                            orcamento["estoklus_id"]
                          ]

        estoklus.update('e_assist_tecnica',colunas_update,valores_update,["codigo_os_assist_tecnica = "+os+""],True)

    campo_auxiliar_os(13,orcamento,'un_min',os)
    campo_auxiliar_os(14,orcamento,"variacao_sm",os)
    campo_auxiliar_os(15,orcamento,"consumo_ua",os)
    campo_auxiliar_os(84,orcamento,"amplitude",os)
    campo_auxiliar_os(85,orcamento,"variacao_sd",os)
    campo_auxiliar_os(83,orcamento,"orcamentista",os)
    campo_auxiliar_os(86,orcamento,"calibre_marca",os)
    campo_auxiliar_os(57,orcamento,"complicacao",os)
    campo_auxiliar_os(56,orcamento,"tipo_movimento",os)
    campo_auxiliar_os(10,orcamento,"prazo_cx",os)
    campo_auxiliar_os(11,orcamento,"garantia",os)
    campo_auxiliar_os(26,orcamento,"repair_tag",os)
    campo_auxiliar_os(28,orcamento,"repair_bre",os)
    campo_auxiliar_os(37,orcamento,"codigo_v01_bv",os)
    campo_auxiliar_os(34,orcamento,'codigo_sap_bv',os)
    campo_auxiliar_os(12,orcamento,"calibre",os)
    campo_auxiliar_os(89,orcamento,"intervencao",os)
    logging.info(f"{os} Orçada")
    return orcamento




def carrega_dados_devolucao(cliente):
    estoklus = Estoklus1()
    os_list = []
    sql = f"""select ast.status_os,

coalesce(aux87.resposta,0)codigo_produto_cliente
,coalesce(aux5.resposta,0)nf_cliente
, coalesce(es.numero_nf_controle,0) nf_estoklus
,loja_os
,codigo_cliente
,ast.valor_produto
, ast.referencia_os_cliente
, cg.codigo_tipo_pessoa
,referencia_produto,serie,modelo,ast.codigo_os_assist_tecnica,
(select count(resposta) from e_assist_tecnica_campo_auxiliar ca join e_assist_tecnica a
on a.codigo_os_assist_tecnica = ca.codigo_os_assist_tecnica where a.codigo_cliente = ast.codigo_cliente and codigo_campo_auxiliar = 5 and resposta = aux5.resposta) qtde_os_nota,
(select count(codigo_movimento_es) from e_movimento_es es
left join e_registro_nf_controle nf on nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle
where codigo_os_assist_tecnica in (select codigo_os_assist_tecnica from e_assist_tecnica_campo_auxiliar where codigo_campo_auxiliar = 5 and resposta = aux5.resposta)
and es.codigo_cfop in('5916','6916','5915','6915' ) and nf.cancelada <> 'S')qtde_emitido,gr.descricao_grupo_os


from e_assist_tecnica ast
left join e_grupo_os_assist_tecnica gr on ast.grupo_os_assist_tecnica = gr.codigo_grupo_os
left join g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral
left join e_movimento_es es on ast.codigo_os_assist_tecnica = es.codigo_os_assist_tecnica and es.codigo_cfop in ('1915','2915')
LEFT join e_assist_tecnica_campo_auxiliar aux5 on ast.codigo_os_assist_tecnica = aux5.codigo_os_assist_tecnica and aux5.codigo_campo_auxiliar = 5
LEFT join e_assist_tecnica_campo_auxiliar aux87 on ast.codigo_os_assist_tecnica = aux87.codigo_os_assist_tecnica and aux5.codigo_campo_auxiliar = 87

where

ast.fase_atual in (3,6) and ast.codigo_cliente = '{cliente}'   and
coalesce((select first 1 nf.numero_nf_controle from e_movimento_es  es
left join e_registro_nf_controle nf on nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle where es.codigo_cadastro_geral = ast.codigo_cliente and nf.codigo_cfop in('5916','6916','5915','6915') and codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica  and nf.cancelada <> 'S' ),0) = 0 """

    for row in estoklus.fetchall(sql):


        os_list.append({"status":row[0],
            "codigo_produto_cliente":row[1],
            "nf_cliente":row[2],
            "nf_estoklus":row[3],
            "loja_os":row[4].strip(),
            "codigo_cliente":row[5],
            "valor_produto":row[6],
            "referencia_os_cliente":row[7],
            "codigo_tipo_pessoa":row[8],
            "referencia_produto":row[9],
            "serie":row[10],
            "modelo":row[11],
            "codigo_os":row[12],
            "quantidade_recebida":row[13],
            "quantidade_devolvida":row[14],
            "marca":row[15]})
    
    return os_list




def gerar_nf_remessa(nf):

        loja=nf["loja"]
        cliente_id = nf["cliente_id"]
        estoklus = Estoklus()
        codigo_nf = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_REGISTRO_NF_C,1) from RDB$DATABASE") 
        sOrigemControle = 'NF08'
        cg_loja = "'*L-"+nf["loja"]+"'"
        if nf["tipo_entrada"] == 'E':
            movimento = '91'
            cfop = estoklus.fetchone("""select CASE WHEN CG.UF = CG1.UF THEN '1915'
ELSE '2915'  end

from g_cadastro_geral cg
left join g_cadastro_geral cg1 on cg.codigo_cadastro_geral = '"""+cliente_id+"""' and cg1.codigo_cadastro_geral = """+cg_loja+

""" where cg.codigo_cadastro_geral = '"""+ cliente_id +"""' AND CG1.codigo_cadastro_geral = """+cg_loja)
        else:
            movimento= '90'
            cfop = estoklus.fetchone("""select CASE WHEN CG.UF = CG1.UF THEN '5916'
ELSE '6916'  end

from g_cadastro_geral cg
left join g_cadastro_geral cg1 on cg.codigo_cadastro_geral = '"""+cliente_id+"""' and cg1.codigo_cadastro_geral = """+cg_loja+

""" where cg.codigo_cadastro_geral = '"""+ cliente_id +"""' AND CG1.codigo_cadastro_geral = """+cg_loja)

    

        querycfop = f"""Select First 1
    Trim(cfop.descricao_cfop) 
  From E_CFOP cfop
  Where cfop.codigo_cfop = {cfop} """
        natureza = estoklus.fetchone(querycfop)
        natureza = natureza.strip()
        if loja == 'PR':
            cst = '50'
            informacoes_complementares = """Suspensão nos termos do o artigo 334 do RICMS/PR"""
            informacoes_complementares += f'\n{nf["info_complementar"]}'
        if loja== 'SP':
            cst = '41'
            informacoes_complementares = """Sem incidência do ICMS, conforme artigo 7°, inciso X, do RICMS/SP."""
            informacoes_complementares += f'\n{nf["info_complementar"]}'
        if loja =='RJ':
            cst = '50'
            informacoes_complementares = """Suspensão nos termos do inciso I do artigo 52º do Livro I Decreto 27.427/00 - RICMS/RJ"""
            informacoes_complementares += f'\n{nf["info_complementar"]}'
        proxima_nf = estoklus.fetch_from_stored_proc('retornar_numero_nf',loja,'02')
        proxima_nf = proxima_nf[0][2]

        campos_insert = ['codigo_registro_nf_controle', 'codigo_loja', 'codigo_loja_fiscal', 'numero_nf_controle',
                                     'serie', 'data', 'e_s', 'codigo_tipo_movimento', 'codigo_cfop', 'natureza_operacao',
                                     'valor_total_produto', 'base_icms', 'valor_icms', 'base_icms_substituicao',
                                     'valor_icms_substituicao', 'valor_ipi', 'base_iss', 'valor_iss', 'valor_frete', 'valor_seguro',
                                     'valor_outras_despesas', 'valor_total_nf', 'percentual_desconto', 'valor_desconto',
                                     'codigo_vendedor', 'cancelada', 'codigo_cadastro_geral', 'tipo_frete', 'observacao_corpo_nota',
                                     'informacoes_complementares', 'codigo_transportador', 'placa_veiculo', 'uf_veiculo',
                                     'quantidade', 'especie', 'marca', 'numero', 'peso_bruto', 'peso_liquido', 'incide_icms_frete',
                                     'incide_icms_seguro', 'incide_icms_outras_despesas', 'origem_nf_controle', 'perc_desconto_2',
                                     'valor_desconto_2', 'consumidor_final', 'indicador_presenca',
                                     'frete_terceirizado', 'nfe_finalidade',
                                     'chave_acesso_nf_e', 'base_ipi', 'base_cofins', 'base_pis',
                                     'valor_cofins', 'valor_pis', 'base_ii', 'valor_ii',
                                    'hora_emissao',  
                                     'inclusao_data', 'inclusao_por']
        valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                       '02','today', nf["tipo_entrada"],movimento,cfop,natureza,
                       nf["total_nf"],0,0,0,
                       0,0,0,0,0,0,
                       0,nf["total_nf"],0,0,
                       '','N',cliente_id,9,'',
                       informacoes_complementares,'','','',
                       0,'','','',0,0,'N',
                       'N','N',sOrigemControle,0,
                       0,'1','9',
                       'N','1',
                       '',0,0,0,
                       0,0,0,0,
                       'now',
                       'now','COCKPIT')]
        estoklus.insert('e_registro_nf_controle',campos_insert,valores_insert)

        for item in nf["itens"]:

            referencia_produto = item["referencia_produto"]
            os_nro = item["codigo_os"]
            campos_insert_mes =['codigo_movimento_es', 'e_s', 'codigo_tipo_movimento', 'data_Movimento_es', 'codigo_loja',
                                  'codigo_produto', 'codigo_cor', 'codigo_tamanho', 'quantidade', 'observacao', 'preco', 'codigo_loja_1',
                                  'codigo_serie', 'numero_nf_controle', 'codigo_registro_nf_controle', 'codigo_cfop',
                                  'codigo_classificacao_fiscal', 'codigo_situacao_tributaria', 'codigo_cadastro_geral',
                                  'codigo_vendedor', 'preco_custo', 'valor_unitario', 'valor_desconto', 'icms_percentual',
                                  'ipi_percentual', 'valor_rateio_frete', 'valor_rateio_Seguro', 'valor_rateio_outros_custos_1',
                                  'valor_rateio_outros_custos_2', 'codigo_pedido_venda', 'codigo_pedido_venda_item',
                                  'codigo_romaneio', 'codigo_romaneio_item', 'movimento_cancelado', 'movimento_altera_estoque',
                                  'cfop_altera_estoque', 'codigo_unidade', 'valor_desconto_nota', 'preco_desconto_especial',
                                  'base_calculo_icms', 'aliquota_icms_st_mva', 'base_ipi', 'aliquota_cofins', 'valor_cofins',
                                  'base_cofins', 'aliquota_pis', 'valor_pis', 'base_pis', 'aliquota_credito_icms',
                                  'valor_credito_icms', 'valor_ipi', 'valor_icms', 'aliquota_ii', 'valor_ii', 'base_ii',
                                  'codigo_cst_origem', 'codigo_cst_icms', 'codigo_cst_csosn', 'codigo_cst_ipi', 'codigo_cst_pis',
                                  'codigo_cst_cofins', 'base_icms_st', 'aliq_icms_st', 'valor_icms_st', 'movimento_veio_sate',
                                  'codigo_loja_fiscal','diferimento_icms', 'diferimento_icms_valor', 'vbcfcp', 'pfcp', 'vfcp', 'vbcfcpst', 'pfcpst',
                                  'vfcpst', 'modbc', 'predbc', 'valor_icms_deson',

                                  'inclusao_data', 'inclusao_por','descricao_tipo_item','codigo_os_assist_tecnica']

            codigo_mes = estoklus.fetchone("select GEN_ID(GEN_E_codigo_movimento_es,1) from RDB$DATABASE") 
            valores_insert_mes = [(codigo_mes,nf["tipo_entrada"],movimento,'today',loja,'95','','',1,referencia_produto,item["valor_produto"],loja,'02',proxima_nf,codigo_nf,cfop,'91119090','400',cliente_id,'',0,item["valor_produto"],0,0,0,0,0,0,0,0,0,0,0,'N','N','N','UN',0,0,
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'0',cst,'','99','99','99',0,0,0,'N',loja,0,0,0,0,0,0,0,0,0,0,0,'now','Cockpit',item["descricao"],os_nro)]

            estoklus.insert('e_movimento_es',campos_insert_mes,valores_insert_mes)
        return str(codigo_nf)


def gerar_nf_icms(nf):

        loja=nf["loja"]
        cliente_id = nf["cliente_id"]
        estoklus = Estoklus()
        os_nro = nf["codigo_estoklus"]
        sOrigemControle = 'NF08'
        status_os = estoklus.fetchone(f"select status_os from e_assist_tecnica where codigo_os_assist_tecnica = {os_nro}")
        cg_loja = "'*L-"+nf["loja"]+"'"
        movimento= '90'
        itens_nf = ()
        nf["valor_liquido"] = float(estoklus.fetchone(f"""  select  COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) liquido
            from e_assist_tecnica ast
where ast.codigo_os_assist_tecnica = {os_nro}"""))
        nf["valor_cliente"] = nf["valor_liquido"]
        uf_destino = estoklus.fetchone("""select UF

from g_cadastro_geral cg


where cg.codigo_cadastro_geral = '"""+ cliente_id +"""'""")
        if uf_destino == nf["loja"]:
            cfop = '5102'
        else:
            cfop = '6102'
        


        if cfop == '6102' and status_os != '31':
            return {"error":"Permitido apenas clientes da mesma UF ou Acessórios"}
        querynota = f"""select codigo_nfse from  F_LANCAMENTO l
                        WHERE l.CODIGO_TIPO_LIGACAO = 'A'    and l.CODIGO_LIGACAO not starting with '*'

                        and codigo_ligacao = {os_nro}

                        group by 1
                        """
        for row in estoklus.fetchall(querynota):
            if row[0] >0:
                return {"error":"OS Possui NF de Serviço"}
        querycfop = f"""Select First 1
    Trim(cfop.descricao_cfop) 
  From E_CFOP cfop
  Where cfop.codigo_cfop = {cfop} """
        tem_nf = estoklus.fetchone(f"""select coalesce(max (es.codigo_movimento_es),0)
from e_movimento_es es
left join e_registro_nf_controle nf on nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle  where  codigo_os_assist_tecnica = {os_nro}  and es.codigo_cfop in ('6102','5102') and nf.cancelada != 'S'""")
        if(tem_nf > 0):
            return {"error":"OS já tem NF"}
        codigo_nf = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_REGISTRO_NF_C,1) from RDB$DATABASE") 
        natureza = estoklus.fetchone(querycfop)
        natureza = natureza.strip()
        cst = '00'
        proxima_nf = estoklus.fetch_from_stored_proc('retornar_numero_nf',loja,'02')
        proxima_nf = proxima_nf[0][2]
        icms = estoklus.fetch_from_stored_proc('E_SP_LER_ALIQUOTA_ICMS_PRODUTO','S','95',loja,uf_destino,loja,cfop,'','91149000','N')[0][0]
        icms = int(icms)
        if icms == 0:
            if nf["loja"] == 'SP':
                icms = 18
            elif nf["loja"] == 'PR':
                icms = 19
            elif nf["loja"] == 'RJ':
                icms = 16

        base_icms = nf["valor_cliente"]
        aliquota_icms = icms
        valor_icms = base_icms * (icms /100)
        
        
        informacoes_complementares = f"""OS {nf["id"]}"""
        campos_insert = ['codigo_registro_nf_controle', 'codigo_loja', 'codigo_loja_fiscal', 'numero_nf_controle',
                                         'serie', 'data', 'e_s', 'codigo_tipo_movimento', 'codigo_cfop', 'natureza_operacao',
                                         'valor_total_produto', 'base_icms', 'valor_icms', 'base_icms_substituicao',
                                         'valor_icms_substituicao', 'valor_ipi', 'base_iss', 'valor_iss', 'valor_frete', 'valor_seguro',
                                         'valor_outras_despesas', 'valor_total_nf', 'percentual_desconto', 'valor_desconto',
                                         'codigo_vendedor', 'cancelada', 'codigo_cadastro_geral', 'tipo_frete', 'observacao_corpo_nota',
                                         'informacoes_complementares', 'codigo_transportador', 'placa_veiculo', 'uf_veiculo',
                                         'quantidade', 'especie', 'marca', 'numero', 'peso_bruto', 'peso_liquido', 'incide_icms_frete',
                                         'incide_icms_seguro', 'incide_icms_outras_despesas', 'origem_nf_controle', 'perc_desconto_2',
                                         'valor_desconto_2', 'consumidor_final', 'indicador_presenca',
                                         'frete_terceirizado', 'nfe_finalidade',
                                         'chave_acesso_nf_e', 'base_ipi', 'base_cofins', 'base_pis',
                                         'valor_cofins', 'valor_pis', 'base_ii', 'valor_ii',
                                        'hora_emissao',  
                                         'inclusao_data', 'inclusao_por']
        campos_insert_mes =['codigo_movimento_es', 'e_s', 'codigo_tipo_movimento', 'data_Movimento_es', 'codigo_loja',
                                      'codigo_produto', 'codigo_cor', 'codigo_tamanho', 'quantidade', 'observacao', 'preco', 'codigo_loja_1',
                                      'codigo_serie', 'numero_nf_controle', 'codigo_registro_nf_controle', 'codigo_cfop',
                                      'codigo_classificacao_fiscal', 'codigo_situacao_tributaria', 'codigo_cadastro_geral',
                                      'codigo_vendedor', 'preco_custo', 'valor_unitario', 'valor_desconto', 'icms_percentual',
                                      'ipi_percentual', 'valor_rateio_frete', 'valor_rateio_Seguro', 'valor_rateio_outros_custos_1',
                                      'valor_rateio_outros_custos_2', 'codigo_pedido_venda', 'codigo_pedido_venda_item',
                                      'codigo_romaneio', 'codigo_romaneio_item', 'movimento_cancelado', 'movimento_altera_estoque',
                                      'cfop_altera_estoque', 'codigo_unidade', 'valor_desconto_nota', 'preco_desconto_especial',
                                      'base_calculo_icms', 'aliquota_icms_st_mva', 'base_ipi', 'aliquota_cofins', 'valor_cofins',
                                      'base_cofins', 'aliquota_pis', 'valor_pis', 'base_pis', 'aliquota_credito_icms',
                                      'valor_credito_icms', 'valor_ipi', 'valor_icms', 'aliquota_ii', 'valor_ii', 'base_ii',
                                      'codigo_cst_origem', 'codigo_cst_icms', 'codigo_cst_csosn', 'codigo_cst_ipi', 'codigo_cst_pis',
                                      'codigo_cst_cofins', 'base_icms_st', 'aliq_icms_st', 'valor_icms_st', 'movimento_veio_sate',
                                      'codigo_loja_fiscal','diferimento_icms', 'diferimento_icms_valor', 'vbcfcp', 'pfcp', 'vfcp', 'vbcfcpst', 'pfcpst',
                                      'vfcpst', 'modbc', 'predbc', 'valor_icms_deson',

                                      'inclusao_data', 'inclusao_por','descricao_tipo_item','codigo_os_assist_tecnica']        
        if status_os != '31':
            valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                           '02','today', 'S',movimento,cfop,natureza,
                           nf["valor_cliente"],base_icms,valor_icms,0,
                           0,0,0,0,0,0,
                           0,nf["valor_cliente"],nf["valor_cliente"] / 0.82,0,
                           '','N',cliente_id,9,'',
                           informacoes_complementares,'','','',
                           0,'','','',0,0,'N',
                           'N','N',sOrigemControle,0,
                           0,'1','9',
                           'N','1',
                           '',0,0,0,
                           0,0,0,0,
                           'now',
                           'now','COCKPIT')]
            referencia_produto = nf["marca"]       
            codigo_mes = estoklus.fetchone("select GEN_ID(GEN_E_codigo_movimento_es,1) from RDB$DATABASE")
            valores_insert_mes = [(codigo_mes,'S',movimento,'today',loja,'3268578','','',1,referencia_produto,nf["valor_cliente"],loja,'02',proxima_nf,codigo_nf,cfop,'91149000','400',cliente_id,'',0,nf["valor_cliente"],0,18,0,0,0,0,0,0,0,0,0,'N','N','N','UN',0,0,
                                   base_icms,0,
                                   0,0,0,0,0,0,0,0,0,0,valor_icms,0,0,0,
                                   '0',cst,'','99','99',
                                   '99',0,0,0,'N',
                                   loja,0,0,0,0,0,0,0,
                                   0,0,0,0,
                                   'now','Cockpit',f'KIT CONSERTO {nf["marca"]}',os_nro)]
            valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                           '02','today', 'S',movimento,cfop,natureza,
                           nf["valor_cliente"],base_icms,valor_icms,0,
                           0,0,0,0,0,0,
                           0,nf["valor_cliente"],nf["valor_cliente"] / 0.82,0,
                           '','N',cliente_id,9,'',
                           informacoes_complementares,'','','',
                           0,'','','',0,0,'N',
                           'N','N',sOrigemControle,0,
                           0,'1','9',
                           'N','1',
                           '',0,0,0,
                           0,0,0,0,
                           'now',
                           'now','COCKPIT')]
            estoklus.insert('e_movimento_es',campos_insert_mes,valores_insert_mes)      
        else:
            querypecas = f"""Select
    atps_.VALOR_UNITARIO,
    atps_.QTDE ,
     coalesce( ast.valor_desconto /(Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') *100 ,0) DESCONTO,
    p.codigo_produto,
    p.referencia_produto,
    coalesce(p.codigo_classificacao_fiscal,'')



    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    left join e_produto p on atps_.codigo_produto = p.codigo_produto
    left join e_assist_tecnica ast on atps_.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica where
    atps_.codigo_os_assist_tecnica = {os_nro} and atps_.garantia = 'N' and atps_.extra <> 'S' and atps_.peca_ou_servico = 'P' and p.codigo_produto <> '95' """
            base_icms_nf = 0
            valor_icms_nf = 0
            
            for row in estoklus.fetchall(querypecas):
                valor_unitario = float(row[0]) * (1 - float(row[2]) / 100)

                qtde = int(row[1])
                if nf["loja"] == 'SP':
                    base_icms = valor_unitario  * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms
                if nf["loja"] == 'PR':
                    base_icms = valor_unitario   * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms
                if nf["loja"] == 'RJ':
                    base_icms = valor_unitario  * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms 
                base_icms_nf += base_icms
                valor_icms_nf += valor_icms   
                codigo_mes = estoklus.fetchone("select GEN_ID(GEN_E_codigo_movimento_es,1) from RDB$DATABASE")
                valores_insert_mes = [(codigo_mes,'S',movimento,'today',loja,row[3],'','',row[1],row[4],valor_unitario*qtde,loja,'02',proxima_nf,codigo_nf,cfop,row[5],'400',cliente_id,'',0,valor_unitario,0,aliquota_icms,0,0,0,0,0,0,0,0,0,'N','N','N','UN',0,0,
                                   base_icms,0,
                                   0,0,0,0,0,0,0,0,0,0,valor_icms,0,0,0,
                                   '0',cst,'','99','99',
                                   '99',0,0,0,'N',
                                   loja,0,0,0,0,0,0,0,
                                   0,0,0,0,
                                   'now','Cockpit',f'KIT CONSERTO {nf["marca"]}',os_nro)]


                estoklus.insert('e_movimento_es',campos_insert_mes,valores_insert_mes)
                itens_nf = itens_nf + (codigo_mes,)
            rounded_base_icms = round(base_icms_nf, 2)
            valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                           '02','today', 'S',movimento,cfop,natureza,
                           nf["valor_cliente"],rounded_base_icms,valor_icms_nf,0,
                           0,0,0,0,0,0,
                           0,rounded_base_icms,rounded_base_icms,0,
                           '','N',cliente_id,9,'',
                           informacoes_complementares,'','','',
                           0,'','','',0,0,'N',
                           'N','N',sOrigemControle,0,
                           0,'1','9',
                           'N','1',
                           '',0,0,0,
                           0,0,0,0,
                           'now',
                           'now','COCKPIT')]
        estoklus.insert('e_registro_nf_controle',campos_insert,valores_insert)
        for item in itens_nf:    

                retorno = estoklus.fetch_from_stored_proc('e_sp_calcula_partilha_icms',item)
                if retorno[0][0]== 1:
                
                    VBCUFDEST = retorno[0][2]
                    PFCPUFDEST =retorno[0][3]
                    VBCFCPUFDEST = retorno[0][10]
                    PICMSUFDEST  = retorno[0][4]
                    PICMSINTER =  retorno[0][5]
                    PICMSINTERPART = retorno[0][6]
                    VFCPUFDEST = retorno[0][7]
                    VICMSUFDEST = retorno[0][8]
                    VICMSUFREMET = retorno[0][9]
                    estoklus.update('E_MOVIMENTO_ES',['VBCUFDEST','PFCPUFDEST','VBCFCPUFDEST','PICMSUFDEST','PICMSINTER','PICMSINTERPART','VFCPUFDEST','VICMSUFDEST','VICMSUFREMET'],
                        [VBCUFDEST,PFCPUFDEST,VBCFCPUFDEST,PICMSUFDEST,PICMSINTER,PICMSINTERPART,VFCPUFDEST,VICMSUFDEST,VICMSUFREMET],[f"codigo_movimento_es = {item}"],False)            


        
        estoklus.update(f'F_LANCAMENTO',['CODIGO_NFSE'],[-1],[f"CODIGO_TIPO_LIGACAO = 'A' and CODIGO_LIGACAO not starting with '*' and codigo_ligacao = {os_nro}"],False)
        estoklus.fetch_from_stored_proc('atualizar_valores_nota',codigo_nf)
        
        return {"success": proxima_nf}

def liberado_execucao(os):
    estoklus = Estoklus()
    if os.get('estoklus_id','') == '':
        return {"error": 'estoklus_id'}
    if os.get('texto_laboratorio','') == '':
         return {"error": 'texto_laboratorio'}   
    if os.get('codigo_estoklus') == '':
        return {"error": 'codigo_estoklus'}    
    if os.get('cliente_id') == '':
        return {"error": 'cliente_id'}    
    if os.get('sistema','') == '' or os.get('sistema','') == 'ANTIGO':
        return {"error":"sistema"}
    
    now = datetime.now()
    formatted_time = now.strftime('%H:%M')
    estoklus.update('E_ASSIST_TECNICA',['DATA_LIBERADO_EXECUCAO','STATUS_OS','alteracao_data','alteracao_por'],['today','10','today','CP'],["codigo_os_assist_tecnica =" + str(os["codigo_estoklus"])],False)
    estoklus.fetch_from_stored_proc('wt_gera_historico',os["codigo_estoklus"],'Fornitura',os["texto_laboratorio"],os['cliente_id'],formatted_time)
    logging.info("OS Liberada para Execução")
    return {"success":"ok"}


def gera_historico(texto,os,cliente,titulo):
# Formatar para obter a hora e o minuto no formato HH:MM
    now = datetime.now()
    formatted_time = now.strftime('%H:%M')
    estoklus = Estoklus()

    texto_modificado = texto.replace('\n', '\r\n')
    estoklus.fetch_from_stored_proc('wt_gera_historico',os,titulo,texto_modificado,cliente,formatted_time)


def get_forma_pagamentos():
    estoklus =Estoklus()
    query = """select codigo_forma_pagamento, descricao_forma_pagamento from e_forma_pagamento f
where f.ativo = 'S'"""

    return [{
        'codigo_forma_pagamento': row[0],
        'descricao_forma_pagamento': row[1]
     } for row in estoklus.fetchall(query)]



def gerar_nf_baixa_estoque(loja,infocomplementar,data_ini,data_fim):


        estoklus = Estoklus()
        sOrigemControle = 'NF08'
        cg_loja = "*L-"+loja+""
        movimento= '90'
        uf_destino = loja
        cfop = '5927'
        codigo_nf = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_REGISTRO_NF_C,1) from RDB$DATABASE") 
        natureza = "Lançamento efetuado a título de bx. estoque"
        natureza = natureza.strip()
        cst = '90'
        proxima_nf = estoklus.fetch_from_stored_proc('retornar_numero_nf',loja,'02')
        proxima_nf = proxima_nf[0][2]
        icms = 0
        icms = int(icms)
        if icms == 0:
            if loja == 'SP':
                icms = 18
            elif loja == 'PR':
                icms = 19
            elif loja == 'RJ':
                icms = 16

        base_icms = 0
        aliquota_icms = icms
        valor_icms = base_icms * (icms /100)
        
        
        informacoes_complementares = infocomplementar
        campos_insert = ['codigo_registro_nf_controle', 'codigo_loja', 'codigo_loja_fiscal', 'numero_nf_controle',
                                         'serie', 'data', 'e_s', 'codigo_tipo_movimento', 'codigo_cfop', 'natureza_operacao',
                                         'valor_total_produto', 'base_icms', 'valor_icms', 'base_icms_substituicao',
                                         'valor_icms_substituicao', 'valor_ipi', 'base_iss', 'valor_iss', 'valor_frete', 'valor_seguro',
                                         'valor_outras_despesas', 'valor_total_nf', 'percentual_desconto', 'valor_desconto',
                                         'codigo_vendedor', 'cancelada', 'codigo_cadastro_geral', 'tipo_frete', 'observacao_corpo_nota',
                                         'informacoes_complementares', 'codigo_transportador', 'placa_veiculo', 'uf_veiculo',
                                         'quantidade', 'especie', 'marca', 'numero', 'peso_bruto', 'peso_liquido', 'incide_icms_frete',
                                         'incide_icms_seguro', 'incide_icms_outras_despesas', 'origem_nf_controle', 'perc_desconto_2',
                                         'valor_desconto_2', 'consumidor_final', 'indicador_presenca',
                                         'frete_terceirizado', 'nfe_finalidade',
                                         'chave_acesso_nf_e', 'base_ipi', 'base_cofins', 'base_pis',
                                         'valor_cofins', 'valor_pis', 'base_ii', 'valor_ii',
                                        'hora_emissao',  
                                         'inclusao_data', 'inclusao_por']
        campos_insert_mes =['codigo_movimento_es', 'e_s', 'codigo_tipo_movimento', 'data_Movimento_es', 'codigo_loja',
                                      'codigo_produto', 'codigo_cor', 'codigo_tamanho', 'quantidade', 'observacao', 'preco', 'codigo_loja_1',
                                      'codigo_serie', 'numero_nf_controle', 'codigo_registro_nf_controle', 'codigo_cfop',
                                      'codigo_classificacao_fiscal', 'codigo_situacao_tributaria', 'codigo_cadastro_geral',
                                      'codigo_vendedor', 'preco_custo', 'valor_unitario', 'valor_desconto', 'icms_percentual',
                                      'ipi_percentual', 'valor_rateio_frete', 'valor_rateio_Seguro', 'valor_rateio_outros_custos_1',
                                      'valor_rateio_outros_custos_2', 'codigo_pedido_venda', 'codigo_pedido_venda_item',
                                      'codigo_romaneio', 'codigo_romaneio_item', 'movimento_cancelado', 'movimento_altera_estoque',
                                      'cfop_altera_estoque', 'codigo_unidade', 'valor_desconto_nota', 'preco_desconto_especial',
                                      'base_calculo_icms', 'aliquota_icms_st_mva', 'base_ipi', 'aliquota_cofins', 'valor_cofins',
                                      'base_cofins', 'aliquota_pis', 'valor_pis', 'base_pis', 'aliquota_credito_icms',
                                      'valor_credito_icms', 'valor_ipi', 'valor_icms', 'aliquota_ii', 'valor_ii', 'base_ii',
                                      'codigo_cst_origem', 'codigo_cst_icms', 'codigo_cst_csosn', 'codigo_cst_ipi', 'codigo_cst_pis',
                                      'codigo_cst_cofins', 'base_icms_st', 'aliq_icms_st', 'valor_icms_st', 'movimento_veio_sate',
                                      'codigo_loja_fiscal','diferimento_icms', 'diferimento_icms_valor', 'vbcfcp', 'pfcp', 'vfcp', 'vbcfcpst', 'pfcpst',
                                      'vfcpst', 'modbc', 'predbc', 'valor_icms_deson',

                                      'inclusao_data', 'inclusao_por','descricao_tipo_item','codigo_os_assist_tecnica']      
        querypecas = f"""select p.preco,pc.qtde,0,p.codigo_produto,pc.referencia_fornecedor, case when prod.codigo_classificacao_fiscal = '' then '91119090' else prod.codigo_classificacao_fiscal end


               from e_assist_tecnica ast
               join e_assist_tecnica_pecas_servicos pc on ast.codigo_os_assist_tecnica = pc.codigo_os_assist_tecnica and pc.peca_ou_servico = 'P'
               left join e_produto prod on prod.codigo_produto = pc.codigo_produto
               join e_produto_preco p on p.codigo_produto =  pc.codigo_produto



               where




             (select first 1 nf.inclusao_data from e_assist_tecnica_pagto pg
               join f_lancamento l on l.codigo_lancamento = pg.num_lancamento_guelt
               join f_nfse nf on nf.codigo_nfse = l.codigo_nfse
               where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) >='{data_ini}' and (select first 1 nf.inclusao_data from e_assist_tecnica_pagto pg
               join f_lancamento l on l.codigo_lancamento = pg.num_lancamento_guelt
               join f_nfse nf on nf.codigo_nfse = l.codigo_nfse
               where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) <= '{data_fim}' and p.codigo_tipo_preco = 'D'  and ast.loja_os = '{loja}'   and pc.codigo_produto not in  ('95','000801') and p.preco <> 0"""
        base_icms_nf = 0
        valor_icms_nf = 0
        for row in estoklus.fetchall(querypecas):
                valor_unitario = float(row[0]) * (1 - float(row[2]) / 100)

                qtde = int(row[1])
                if loja == 'SP':
                    base_icms = valor_unitario  * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms
                if loja == 'PR':
                    base_icms = valor_unitario   * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms
                if loja == 'RJ':
                    base_icms = valor_unitario  * qtde
                    valor_icms = base_icms * (icms /100)
                    aliquota_icms = icms 
                base_icms_nf += base_icms
                valor_icms_nf += valor_icms            
                codigo_mes = estoklus.fetchone("select GEN_ID(GEN_E_codigo_movimento_es,1) from RDB$DATABASE")
                valores_insert_mes = [(codigo_mes,'S',movimento,'today',loja,row[3],'','',row[1],row[4],valor_unitario,loja,'02',proxima_nf,codigo_nf,cfop,row[5],'400',cg_loja,'',0,valor_unitario,0,aliquota_icms,0,0,0,0,0,0,0,0,0,'N','N','N','UN',0,0,
                                   base_icms,0,
                                   0,0,0,0,0,0,0,0,0,0,valor_icms,0,0,0,
                                   '0',cst,'','99','99',
                                   '99',0,0,0,'N',
                                   loja,0,0,0,0,0,0,0,
                                   0,0,0,0,
                                   'now','Cockpit','',0)]


                estoklus.insert('e_movimento_es',campos_insert_mes,valores_insert_mes)


        rounded_base_icms = round(base_icms_nf, 2)
        valores_insert = [(codigo_nf,loja,loja,proxima_nf,
                           '02','12/31/2023', 'S',movimento,cfop,natureza,
                           rounded_base_icms,rounded_base_icms,valor_icms_nf,0,
                           0,0,0,0,0,0,
                           0,rounded_base_icms,rounded_base_icms,0,
                           '','N',cg_loja,9,'',
                           informacoes_complementares,'','','',
                           0,'','','',0,0,'N',
                           'N','N',sOrigemControle,0,
                           0,'1','9',
                           'N','1',
                           '',0,0,0,
                           0,0,0,0,
                           'now',
                           'now','COCKPIT')]
        estoklus.insert('e_registro_nf_controle',campos_insert,valores_insert)       
        estoklus.fetch_from_stored_proc('atualizar_valores_nota',codigo_nf)
        
        return {"success": proxima_nf}



def reprovar_os(os):
    
    gera_historico(os["texto_historico"],os["codigo_estoklus"],os["cliente_id"],os["titulo_historico"])
    campo_auxiliar_os(88,os,'motivo_reprovacao',os["codigo_estoklus"])
    estoklus = Estoklus()
    if os["brand_id"] == 'BE':
        campo_auxiliar_os(28,os,'repair_bre',os["codigo_estoklus"])
    estoklus.update('E_ASSIST_TECNICA',['FASE_ATUAL','STATUS_OS','ALTERACAO_DATA','ALTERACAO_POR','FASE2_alteracao_data','FASE2_ALTERACAO_POR','APROVADO','DATA_APROVADO'],
                    [3,
                     '04',
                     'now',
                     os["estoklus_id"],
                     'now',
                     os["estoklus_id"],
                     'N',
                     'today'],
                     [f"codigo_os_assist_tecnica = {os['codigo_estoklus']}"],False)
    logging.info(f"{os['codigo_estoklus']} Reprovada")
    




def aprovar_os(orcamento):

    required_fields = ['itens',  'serie', 'estoklus_id', 'loja', 'referencia_produto', 'estoklus_id', 'id','prazo']
    required_fields_item = ['tipo', 'id', 'label', 'referencia', 'quantidade', 'preco_venda']
    validation = []
    for field in required_fields:
        if field not in orcamento:
            validation.append(field) 

    # Obtém a data e hora atual
    data_atual = datetime.now()

    # Soma 45 dias à data atual
    nova_data = data_atual + timedelta(days=int(orcamento["prazo"]))

    # Formata a nova data como desejar
    data_formatada = nova_data.strftime("%m/%d/%Y")


    if validation:
        return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}



    estoklus=Estoklus()
    campos_insert =['CODIGO_PECAS_SERVICOS','CODIGO_OS_ASSIST_TECNICA','PECA_OU_SERVICO','CODIGO_PRODUTO',
                     'DESCRICAO','REFERENCIA_FORNECEDOR','UNIDADE','QTDE','VALOR_UNITARIO','GARANTIA','INCLUSAO_DATA','INCLUSAO_POR','CODIGO_LOJA_BAIXA','EXTRA','APROVADO']
    ##VALIDAÇÃO
    os = orcamento["codigo_estoklus"]
    estoklus.delete_from_table('e_assist_tecnica_pecas_servicos',f'codigo_os_assist_tecnica = {os}')
    for item in orcamento["itens"]:
        for field in required_fields_item:
            if field not in item:
                validation.append(field)
        if validation:
            return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}

    ##INSERÇÃO DOS ITENS
    tipo_peca = 'P'
    extra = 'N'
    garantia = 'N'
    for item in orcamento["itens"]:

        if item["tipo"]== 'S':
            tipo_peca = 'S'
            extra = 'N'
            garantia = 'N'
        elif item["tipo"]== 'I':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'S'

        elif item["tipo"]== 'P':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'N'

        elif item["tipo"]== 'OP':
            tipo_peca = 'P'
            extra = 'O'
            garantia = 'N'   

        if item["tipo"]== 'SO':
            tipo_peca = 'S'
            extra = 'O'
            garantia = 'N'

        elif item["tipo"]== 'G':
            tipo_peca = 'P'
            extra = 'N'
            garantia = 'N'
        
        id_peca = estoklus.fetchone("select GEN_ID(gen_e_pecas_servicos,1) from RDB$DATABASE")
        valores_insert= [(id_peca,
                      os,
                      tipo_peca,
                      item["id"],
                      item["label"],
                      item["referencia"],
                      'UN',
                      item["quantidade"],
                      item["preco_venda"],
                      garantia,
                      'now',
                      orcamento["estoklus_id"],
                      orcamento["loja"],
                      extra,
                      'S'
                      )]
        
        ##ATUALIZAÇÃO PREÇOS

        #if orcamento["editado"] == 'S' and tipo_peca == 'P':
        #    atualizar_preco(item["id"],item["preco_venda"],'001')
        #    atualizar_preco(item["id"],item["preco_custo"],'D')
    
        estoklus.insert('E_ASSIST_TECNICA_PECAS_SERVICOS',campos_insert,valores_insert)

    ##ATUALIZAÇÃO DA CAPA
    colunas_update = ['fase_atual', 'status_os','data_prevista_entrega','valor_desconto','margem_wt','custo_total','margem_opcionais','lucro_opcional','lucro_obrigatorio','alteracao_data','alteracao_por','FASE2_ALTERACAO_DATA','FASE2_ALTERACAO_POR',
                      'aprovado','observacao_aprovacao','data_aprovado','aprovado_por']
    
    valores_update= [4,
                      orcamento.get("status_aprovacao",'05'),
                      data_formatada,
                        orcamento.get("valor_desconto_todos",0),
                        orcamento.get('valor_margem_obrigatorios',0),
                        orcamento.get('custo_total',0),
                        orcamento.get('valor_margem',0),
                        orcamento.get('valor_liquido',0),
                        orcamento.get('valor_liquido_obrigatorios',0),
                        'now',
                        orcamento["estoklus_id"],
                        'now',
                        orcamento["estoklus_id"],
                        'S',
                        orcamento.get('observacao_aprovacao',''),
                        'today',
                        orcamento.get('contato_aprovacao','')
                      ]
    
    estoklus.update('e_assist_tecnica',colunas_update,valores_update,[f"codigo_os_assist_tecnica = {os}"],True)
    logging.info(f"{os} Aprovada")
    return {"data_previsao": data_formatada}
   


def get_customer_data(filter,data):
    estoklus = Estoklus1()
    query = f""" SELECT {data} from g_cadastro_geral
     where codigo_cadastro_geral = '{filter}' """
    
    return {"result": estoklus.fetchone(query)}


def consulta_financeiro_os(os):
    estoklus = Estoklus()
    sql = f"""select coalesce((select sum(valor) from e_assist_tecnica_pagto where codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),0) pago,
   COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) liquido,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) -
    coalesce((select sum(valor) from e_assist_tecnica_pagto where codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),0)  valor_restante
      from e_assist_tecnica ast
where ast.codigo_os_assist_tecnica = {os}"""
    
    return [{"valor_pago":round(float(row[0]),2),
             "valor_receber":round(float(row[1]),2),
             "valor_restante": round(float(row[2]),2)} for row in estoklus.fetchall(sql)]
    
    

def lanca_financeiro(os,valor,forma_pagamento,tipo,usuario,observacao,loja):
    estoklus = Estoklus()
    estoklus.fetch_from_stored_proc('wt_criar_lancamento',tipo,usuario,os,forma_pagamento,valor,observacao,loja)
    logging.info(f"lançado financeiro da OS {os}")

    return {"sucess": consulta_financeiro_os(os)}



def insere_peca_extra(item,os,user,loja):
    campos_insert =['CODIGO_PECAS_SERVICOS','CODIGO_OS_ASSIST_TECNICA','PECA_OU_SERVICO','CODIGO_PRODUTO',
                     'DESCRICAO','REFERENCIA_FORNECEDOR','UNIDADE','QTDE','VALOR_UNITARIO','GARANTIA','INCLUSAO_DATA','INCLUSAO_POR','CODIGO_LOJA_BAIXA','EXTRA','APROVADO']
    estoklus = Estoklus()
    id_peca = estoklus.fetchone("select GEN_ID(gen_e_pecas_servicos,1) from RDB$DATABASE")
    valores_insert= [(id_peca,
                      os,
                      'P',
                      item["id"],
                      item["label"],
                      item["referencia"],
                      'UN',
                      item["quantidade"],
                      item["preco_venda"],
                      'N',
                      'now',
                      user,
                      loja,
                      'S',
                      'S'
                      )]
    
    estoklus.insert('E_ASSIST_TECNICA_PECAS_SERVICOS',campos_insert,valores_insert)

    return('OK')

def desativa_peca(codigo_pecas_servicos):
    estoklus = Estoklus()
    estoklus.update('e_assist_tecnica_pecas_servicos',[('qtde')],[(0)],[f"codigo_pecas_servicos = {codigo_pecas_servicos}"],False)
    return 'OK'


def remove_peca(codigo_pecas_servicos):
    estoklus = Estoklus()
    estoklus.delete_from_table('e_assist_tecnica_pecas_servicos',f"codigo_pecas_servicos = {codigo_pecas_servicos}")
    return 'OK'

def libera_os_acessorios(codigo_os,user):
    estoklus = Estoklus()
    estoklus.update('e_assist_tecnica',['data_inicio_conserto','data_termino_conserto','fase_atual','status_os','fase3_alteracao_data','fase3_alteracao_por','fase4_alteracao_data','fase4_alteracao_por','tecnico_responsavel_conserto','tecnico_responsavel_liberacao','alteracao_data','alteracao_por'],
                                       ['today','today',6,'31','now',user,'now',user,'99',user,'now',user],[f"codigo_os_assist_tecnica = {codigo_os}"],False)
    
    logging.info(f"{codigo_os} acessório Liberada")
    return 'OK'

def fluxo_conserto(os,fluxo,user):
     estoklus = Estoklus()
     if fluxo == 'prep':
        estoklus.update('E_ASSIST_TECNICA',['fase_atual','status_os','data_inicio_preparacao','tecnico_preparacao','data_inicio_conserto','tecnico_responsavel_conserto','fase3_alteracao_data','fase3_alteracao_por'],
                        ['5','40',os["data_inicio_preparacao"],os['tecnico_preparacao'],os["data_inicio_preparacao"],os['tecnico_preparacao'],'now',user],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)
     elif fluxo=='pol':
        estoklus.update('E_ASSIST_TECNICA',['fase_atual','status_os','data_termino_preparacao','data_inicio_polimento','tecnico_polimento','fase3_alteracao_data','fase3_alteracao_por'],
                        ['5','41',os["data_inicio_polimento"],os["data_termino_preparacao"],os['tecnico_polimento'],'now',user],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)
     elif fluxo=='conserto':
                query=f"select coalesce(data_inicio_conserto,'0') from e_assist_tecnica where codigo_os_assist_tecnica = {os['codigo_estoklus']}"

                if estoklus.fetchone(query) == '0':
                    estoklus.update('E_ASSIST_TECNICA',['fase_atual','status_os','data_inicio_servico','tecnico_responsavel_conserto','data_inicio_conserto','fase3_alteracao_data','fase3_alteracao_por'],
                        ['5','06',os["data_inicio_conserto"],os['tecnico_servico'],os["data_inicio_conserto"],'now',user],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)
                else:
                    estoklus.update('E_ASSIST_TECNICA',['fase_atual','status_os','data_inicio_servico','tecnico_responsavel_conserto','fase3_alteracao_data','fase3_alteracao_por'],
                        ['5','06',os["data_inicio_conserto"],os['tecnico_servico'],'now',user],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)

     elif fluxo=='qa':
        estoklus.update('E_ASSIST_TECNICA',['fase_atual','status_os','data_termino_conserto','tecnico_responsavel_conserto','fase3_alteracao_data','fase3_alteracao_por'],
                        ['5','07',os["data_termino_conserto"],os["tecnico_servico"],'now',os["tecnico_servico"]],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)
     elif fluxo=='le':
            campo_auxiliar_os(43,os,'contrato_richemont',os["codigo_estoklus"])
            campo_auxiliar_os(26,os,'repair_tag',os["codigo_estoklus"])
            campo_auxiliar_os(20,os,'defect_tag',os["codigo_estoklus"])
            campo_auxiliar_os(24,os,'warranty_tag',os["codigo_estoklus"])
            campo_auxiliar_os(25,os,'country_tag',os["codigo_estoklus"])
            campo_auxiliar_os(28,os,'repair_bre',os["codigo_estoklus"])
            campo_auxiliar_os(32,os,'tracking_id_breitling',os["codigo_estoklus"])
            campo_auxiliar_os(29,os,'defect_bre',os["codigo_estoklus"])
            campo_auxiliar_os(31,os,'ultimo_conserto_bre',os["codigo_estoklus"])
            campo_auxiliar_os(30,os,'pais_bre',os["codigo_estoklus"])
            campo_auxiliar_os(35,os,'codigo_v02_bv',os["codigo_estoklus"])
            campo_auxiliar_os(37,os,'codigo_v01_bv',os["codigo_estoklus"])
            campo_auxiliar_os(34,os,'codigo_sap_bv',os["codigo_estoklus"])
            campo_auxiliar_os(90,os,"amplitude"  ,os["codigo_estoklus"])  
            campo_auxiliar_os(91,os,"variacao_sd",os["codigo_estoklus"])  
            campo_auxiliar_os(16,os,"un_min"     ,os["codigo_estoklus"])  
            campo_auxiliar_os(17,os,"variacao_sm",os["codigo_estoklus"])  
            campo_auxiliar_os(18,os,"consumo_ua" ,os["codigo_estoklus"])  
            estoklus.update('E_ASSIST_TECNICA',['tipo_reparo','fase_atual','status_os','data_termino_controle','tecnico_responsavel_liberacao','data_termino_conserto','fase4_alteracao_data','fase4_alteracao_por'],
                        [os["tipo_reparo"],'6',os["status_finalizado"],os["data_liberado_entrega"],user,os["data_liberado_entrega"],'now',user],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)

     elif fluxo=='entregue':
            estoklus.update('E_ASSIST_TECNICA',['fase_atual','data_entrega_produto','observacao_entrega','tecnico_responsavel_entrega','fase5_alteracao_data','fase5_alteracao_por','status_os'],
                        ['7',os["data_entrega_produto"],os.get("observacao_entrega",""),user,'now',user,os['status_finalizado']],[f'codigo_os_assist_tecnica = {os["codigo_estoklus"]}'],False)
            campo_auxiliar_os(7,os,'codigo_rastreio_saida',os["codigo_estoklus"])






