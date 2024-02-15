from models.estoklus import Estoklus
from datetime import datetime,timedelta
import copy


def gerar_romaneio(items,unidadeOrigem,unidadeDestino):
    estoklus = Estoklus()
    current_date = datetime.now()

# Format as string in the format expected by your database
# For example, YYYY-MM-DD HH:MI:SS
    current_date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')

    # Supondo que current_date seja a data atual
    current_date = datetime.now()

    # Formata a data atual como string
    current_date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')

    # Calcula o primeiro dia do próximo mês
    next_month = current_date.replace(day=28) + timedelta(days=4)  # Isso leva ao próximo mês, não importa o dia
    first_day_next_month = next_month.replace(day=1)

    # Calcula o dia 10 do próximo mês
    data_prevista = first_day_next_month.replace(day=10).strftime('%m/%d/%Y')  # Formato MM/DD/AAAA

    # Extrai mês e ano da data atual para mes_competencia
    mes_competencia = current_date.strftime('%m/%Y')  # Formato MM/AAAA
    nome_loja = ''
    if unidadeOrigem == 'SP':
        nome_loja = 'JM ASSISTENCIA'
    elif unidadeOrigem == 'RJ':
        nome_loja = 'JM RACOSKI'
    elif unidadeOrigem == 'PR':
        nome_loja = 'WATCH TIME CURITIBA'
    insert_colums = list()
    insert_values = list()
    insert_values_item = list()
    values_to_insert = []
    #gerar a capa do romaneio
    codigo_romaneio = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_ROMANEIO_CAPA,1) from RDB$DATABASE") 
    insert_colums = 'codigo_romaneio_capa', 'data_romaneio','codigo_loja_saida','codigo_loja_entrada','codigo_cadastro_geral','codigo_tipo_movimento','tem_retorno_pendente','observacao', 'status_romaneio', 'msg_geracao_automatica','codigo_cfop', 'codigo_sate', 'inclusao_data', 'inclusao_por'
    insert_values = codigo_romaneio,'today',unidadeOrigem,unidadeDestino,'','20','n','Gerado pelo Cockpit','0','01-Romaneio gerado pelo Cockpit','','',current_date_str,'Cockpit'
    estoklus.insertone('E_ROMANEIO_CAPA',insert_colums,insert_values)
    total_romaneio = 0
    for item in items:
        print(f'item -{item}')
        codigo_romaneio_item = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_ROMANEIO_ITEM,1) from RDB$DATABASE")  
        total_romaneio += item["preco"] * item["quantidade"]
        insert_colums_item = ('codigo_romaneio_item',
                      'codigo_romaneio_capa', 
                      'codigo_produto', 
                      'codigo_cor', 
                      'codigo_tamanho',
                      'quantidade_prevista', 
                      'codigo_tipo_movimento_s', 
                      'preco_unitario', 
                      'inclusao_data', 
                      'inclusao_por',
                      'codigo_pedido_venda', 
                      'codigo_pedido_venda_item',
                      'codigo_os_assist_tecnica')
        insert_values_item =(codigo_romaneio_item,
                      codigo_romaneio,
                      item['codigo_produto'],
                      '',
                      ' ',
                      item['quantidade'],
                      '20',
                      item['preco'],
                      'now',
                      'Cockpit',
                      None,
                      None,
                      item["codigo_os"])                      
        values_to_insert.append(insert_values_item)

    
    estoklus.insert('E_ROMANEIO_ITEM',insert_colums_item,values_to_insert)
    #Geração do financeiro de pagamento e recebimento
    #pagamento
    
    campos_pagamento = ('parcela','sequencial_parcela','total_de_parcelas','descricao_lancamento','codigo_tipo_operacao','codigo_cadastro_geral',
'duplicata_fatura','data_emissao','mes_ano_competencia','data_documento','codigo_local_documento','codigo_loja','codigo_conta','valor_previsao','valor_previsao_liquido',
'inclusao_por','inclusao_data','data_previsao','CODIGO_CLASSIFICACAO', 'CODIGO_SUB_CLASSIFICACAO')
    valores_pagamento = (
    '000','00','000',f'PAGTO.NF XXX {nome_loja}, REF.ROMANEIO {codigo_romaneio}'  ,'P',f'*L-{unidadeOrigem}','001/001','today',mes_competencia,'today',
'B',unidadeDestino,'20',total_romaneio,total_romaneio,'RNN',current_date_str,data_prevista,'200','202')
    print(valores_pagamento)
    estoklus.insertone('F_LANCAMENTO',campos_pagamento,valores_pagamento)
   
    #recebimento
    estoklus.insertone('F_LANCAMENTO',
    ('parcela','sequencial_parcela','total_de_parcelas','descricao_lancamento','codigo_tipo_operacao','codigo_cadastro_geral',
'duplicata_fatura','data_emissao','mes_ano_competencia','data_documento','codigo_local_documento','codigo_loja','codigo_conta','valor_previsao','valor_previsao_liquido',
'inclusao_por','inclusao_data','data_previsao','CODIGO_CLASSIFICACAO', 'CODIGO_SUB_CLASSIFICACAO'),(
    '000','00','000',f'RCBTO.NF XXX {nome_loja}, REF.ROMANEIO {codigo_romaneio}'  ,'R',f'*L-{unidadeDestino}','001/001','today',mes_competencia,'today',
'B',unidadeOrigem,'20',total_romaneio,total_romaneio,'RNN','now',data_prevista,'200','202'))
    return codigo_romaneio


def get_os_list():
    estoklus = Estoklus()
    querypecas =""" SELECT
   ast.loja_os,
   trim(ast.loja_os)||AST.CODIGO_OS_ASSIST_TECNICA CODIGO_OS_ASSIST_TECNICA,
   AST.FASE_ATUAL,
   p.referencia_produto,
   ASTPS.DESCRICAO,
   ast.data_prevista_entrega,
   descricao_grupo_os,
   astps.codigo_produto,
   astps.descricao,
   qtde -  Coalesce((Select Sum(Case When mes.e_s = 'S' then mes.quantidade else mes.quantidade * -1 end) From E_MOVIMENTO_ES mes
              Where mes.codigo_pecas_servicos = astps.codigo_pecas_servicos and mes.codigo_produto = p.codigo_produto),0)
          - coalesce((select sum(ei.quantidade_prevista) from e_romaneio_capa r
                           join e_romaneio_item   ei  on r.codigo_romaneio_capa = ei.codigo_romaneio_capa
                           where r.status_romaneio not in ('5','3') and 
                                 ei.codigo_os_assist_tecnica <> '' and 
                                 trim(ast.loja_os)||astps.codigo_os_assist_tecnica = ei.codigo_os_assist_tecnica and ei.codigo_produto = p.codigo_produto),0) AS QTDE,
   coalesce((select preco from e_produto_preco pp where pp.codigo_produto = astps.codigo_produto and codigo_tipo_preco = 'D'),0),
   codigo_pecas_servicos

   FROM e_assist_tecnica ast

   left join e_assist_tecnica_pecas_servicos astps on ast.codigo_os_assist_tecnica = astps.codigo_os_assist_tecnica
   left join e_grupo_os_assist_tecnica gr on ast.grupo_os_assist_tecnica = gr.codigo_grupo_os
   left join e_produto p on astps.codigo_produto = p.codigo_produto

   WHERE
   AST.status_os = '05' and fase_atual not in (3,7,8)
   and
   ASTPS.PECA_OU_SERVICO = 'P' AND
   astps.codigo_produto not in ('95','0000801') and
   ASTPS.REFERENCIA_FORNECEDOR <> ''
   and
   qtde -  Coalesce((Select Sum(Case When mes.e_s = 'S' then mes.quantidade else mes.quantidade * -1 end) From E_MOVIMENTO_ES mes
              Where mes.codigo_pecas_servicos = astps.codigo_pecas_servicos and mes.codigo_produto = p.codigo_produto),0)
          - coalesce((select sum(ei.quantidade_prevista) from e_romaneio_capa r
                           join e_romaneio_item   ei  on r.codigo_romaneio_capa = ei.codigo_romaneio_capa
                           where r.status_romaneio not in ('5','3') and 
                                 ei.codigo_os_assist_tecnica <> '' and 
                                 trim(ast.loja_os)||astps.codigo_os_assist_tecnica = ei.codigo_os_assist_tecnica and ei.codigo_produto = p.codigo_produto),0)> 0
               union
            select
       pp.codigo_loja,
           cast( trim(pp.codigo_loja)||'STmin'  as varchar(266)),
            '4',
           referencia_produto,
            cast(p.descricao_produto as varchar(200)),
          cast( '01/01/2030' as timestamp),
           (select descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_marca = p.codigo_marca),
            p.codigo_produto,
           cast(p.descricao_produto as varchar(200)),
           cast((coalesce(est.quantidade_atual,0) - pp.quantidade_minima) * -1 as numeric(18,5) ),
            coalesce((select preco from e_produto_preco pp where pp.codigo_produto = p.codigo_produto and codigo_tipo_preco = 'D'),0),0
            from e_produto_quantidade_auxiliar pp
left join e_produto_quantidade_atual est on est.codigo_produto =  pp.codigo_produto  and pp.codigo_loja = est.codigo_loja
left join e_produto p on pp.codigo_produto = p.codigo_produto

where   ((coalesce(est.quantidade_atual,0) - pp.quantidade_minima) * -1) > 0

order by   6 asc

            """
    

    os_dict = {}
    counter = 1
    for row in estoklus.fetchall(querypecas):
    # Verifica se o código da OS já está no dicionário
        if row[1] in os_dict:
        # Se já está no dicionário, adiciona a peça à lista de peças para essa OS
            os_dict[row[1]]['items'].append({
                       "referencia": row[3],
                        "quantidade": int(row[9]),
                        "codigo_produto": row[7],
                        "descricao": row[4],
                        "preco": float(row[10]),
                        "codigo_os": row[1],
                        "row_key": counter,
                        'data_previsao': row[5].strftime('%d/%m/%Y'),
                        'codigo_pecas_servicos': row[11]
            })
            counter += 1
        else:
            # Se não está no dicionário, cria uma nova entrada para a OS com a unidade e a peça
            os_dict[row[1]] = {
                'unidade_conserto': row[0],
                'data_previsao': row[5].strftime('%d/%m/%Y'),
                'marca': row[6],
                'items': [
                    {
                        "referencia": row[3],
                        "quantidade": int(row[9]),
                        "codigo_produto": row[7],
                        "descricao": row[4],
                        "preco": float(row[10]),
                        "codigo_os": row[1],
                        "row_key": counter,
                        'data_previsao': row[5].strftime('%d/%m/%Y'),
                        'codigo_pecas_servicos': row[11]
                    }
                ]
            }
            counter += 1

    
    return os_dict

def get_estoques():
    estoklus = Estoklus()
    queryestoque = """select referencia_produto,
    quantidade_atual,codigo_loja from e_produto_quantidade_atual est
    left join e_produto p on p.codigo_produto = est.codigo_produto
    where est.quantidade_atual > 0  and p.ativo = 'S'"""

    estoques = {}

    for row in estoklus.fetchall(queryestoque):
        # Verifica se o código da loja já está no dicionário
        if row[2] not in estoques:
            # Se não está no dicionário, cria uma nova entrada para a loja com a lista de itens
            estoques[row[2]] = {"items": []}
        
        # Adiciona a peça à lista de peças para essa loja
        estoques[row[2]]["items"].append({
            "referencia": row[0],
            "quantidade_disponivel": int(row[1])
        })

    return estoques


def gerar_excel(separacao, unidade_estoque):
    print(separacao)
    if unidade_estoque not in separacao:
        print(f"Nenhuma peça para separar para a unidade de estoque {unidade_estoque}.")
        return

    linhas = []
    for unidade_destino, marcas in separacao[unidade_estoque].items():
        for marca, ordens_servico in marcas.items():
            for codigo_os, os in ordens_servico.items():
                for item in os['items']:
                    linha = {
                        'UNIDADE DE DESTINO': unidade_destino,
                        'MARCA': marca,
                        'OS': codigo_os,
                        'CODIGO DA PEÇA': item['referencia'],
                        'DESCRIÇÃO': item["descricao"],
                        'QUANTIDADE': item['quantidade'],
                        'TIPO DE SEPARACAO': os['tipo'],  # 'tipo' é uma chave no nível da ordem de serviço, não do item
                        'PREÇO': item["preco"],
                        "CODIGO_ESTOKLUS": item["codigo_produto"],
                        "row_key": item["row_key"],
                    }
                    linhas.append(linha)
                    
    df = pd.DataFrame(linhas)
    df.to_excel(f'{unidade_estoque}_separacao.xlsx', index=False)

def separar_itens(unidades_estoque, unidades_conserto):
    separacao = {}
    itens_pendentes = []

    for os_id, ordem in unidades_conserto.items():
        unidade_conserto = ordem['unidade_conserto']
        marca = ordem['marca']
        for item in ordem['items']:
            quantidade_necessaria = item['quantidade']
            quantidade_separada = 0

            # Verifica primeiro a unidade de conserto
            if unidade_conserto in unidades_estoque:
                for estoque_item in unidades_estoque[unidade_conserto]['items']:
                    if estoque_item['referencia'] == item['referencia']:
                        qtd_disponivel = min(estoque_item['quantidade_disponivel'], quantidade_necessaria)
                        quantidade_separada += qtd_disponivel
                        estoque_item['quantidade_disponivel'] -= qtd_disponivel
                        add_item_separacao(separacao, unidade_conserto, unidade_conserto, marca, os_id, item, qtd_disponivel)

            # Se ainda precisamos de mais, verifica as outras unidades
            if quantidade_separada < quantidade_necessaria:
                for unidade_estoque, estoque in unidades_estoque.items():
                    if unidade_estoque == unidade_conserto:  # já verificamos essa
                        continue
                    for estoque_item in estoque['items']:
                        if estoque_item['referencia'] == item['referencia']:
                            qtd_disponivel = min(estoque_item['quantidade_disponivel'], quantidade_necessaria - quantidade_separada)
                            quantidade_separada += qtd_disponivel
                            estoque_item['quantidade_disponivel'] -= qtd_disponivel
                            add_item_separacao(separacao, unidade_estoque, unidade_conserto, marca, os_id, item, qtd_disponivel)
                            if quantidade_separada == quantidade_necessaria:
                                break

            # Se ainda faltam itens, adicione à lista de pendentes
            if quantidade_separada < quantidade_necessaria:
                item_copy = item.copy()
                item_copy['quantidade'] = quantidade_necessaria - quantidade_separada
                itens_pendentes.append(item_copy)
    for unidade_estoque, consertos in separacao.items():
        for unidade_conserto, marcas in consertos.items():
            for marca, ordens in marcas.items():
                for os_id, os in ordens.items():
                    total = all(item['quantidade'] == 0 for item in itens_pendentes if item['codigo_os'] == os_id)
                    sortida = len([item for item in os['items'] if item['unidade_estoque'] != unidade_conserto]) > 0
                    for item in os['items']:
                        if total and sortida:
                            item['tipo'] = 'Sortida e suprida'
                        elif total and not sortida:
                            item['tipo'] = 'Todas peças e suprida'
                        elif not total and sortida:
                            item['tipo'] = 'Sortida e parcial'
                        else:  # not total and not sortida
                            item['tipo'] = 'Todas as peças e parcial'
    chaves_para_remover = []

    for unidade_estoque, consertos in separacao.items():
        for unidade_conserto, marcas in consertos.items():
            for marca, ordens in marcas.items():
                for os_id in list(ordens.keys()):  # Criar uma cópia da lista de chaves para iterar
                    if unidade_estoque == unidade_conserto:
                        if os_id == unidade_estoque + 'STmin':
                            # Adiciona a chave à lista de remoção
                            chaves_para_remover.append((unidade_estoque, unidade_conserto, marca, os_id))

    for unidade_estoque, unidade_conserto, marca, os_id in chaves_para_remover:
        del separacao[unidade_estoque][unidade_conserto][marca][os_id]

    return separacao, itens_pendentes

def add_item_separacao(separacao, unidade_estoque, unidade_conserto, marca, os_id, item, quantidade_separada):
    item_copy = item.copy()
    item_copy['quantidade'] = quantidade_separada
    item_copy['unidade_estoque'] = unidade_estoque
    if item_copy['quantidade'] != 0:
        if unidade_estoque not in separacao:
            separacao[unidade_estoque] = {}
        if unidade_conserto not in separacao[unidade_estoque]:
            separacao[unidade_estoque][unidade_conserto] = {}
        if marca not in separacao[unidade_estoque][unidade_conserto]:
            separacao[unidade_estoque][unidade_conserto][marca] = {}
        if os_id not in separacao[unidade_estoque][unidade_conserto][marca]:
            separacao[unidade_estoque][unidade_conserto][marca][os_id] = {'items': [], 'tipo': 'Total e parcial'}  # tipo é fixo, ajuste se necessário

        separacao[unidade_estoque][unidade_conserto][marca][os_id]['items'].append(item_copy)


def gerar_separacao():

    return separar_itens(get_estoques(),get_os_list())[0]



def consulta_romaneios(referencia_produto):
    estoklus = Estoklus()
    query = f"""SELECT p.referencia_produto,erc.codigo_romaneio_capa,ei.quantidade_prevista,sr.descricao,erc.data_romaneio,coalesce(ei.codigo_os_assist_tecnica,''),erc.codigo_loja_entrada,erc.codigo_loja_saida


from e_produto p
left join e_romaneio_item ei on p.codigo_produto = ei.codigo_produto
left join e_romaneio_capa erc on erc.codigo_romaneio_capa = ei.codigo_romaneio_capa
left join e_i_status_romaneio sr on sr.codigo = erc.status_romaneio

where p.referencia_fornecedor = '{referencia_produto}'  and erc.data_romaneio >= cast('today' as date) -180
order by 5 desc"""
    return [{
        'referencia_produto': row[0],
        'romanio': row[1],
        'quantidade': row[2],
        'status_romaneio': row[3],
        'data_romaneio': row[4],
        'OS': row[5],
        'loja_destino': row[6],
        'loja_origem': row[7],
    } for row in estoklus.fetchall(query)]


def baixa_pecas(items,user):
    estoklus = Estoklus()
    for item in items:
        estoklus.fetch_from_stored_proc('AT_RETIRAR_PECA',item["codigo_pecas_servicos"],item["quantidade"],user)
    
    return {"success":"OK"}

def baixa_pecas_os(items,user):
    estoklus = Estoklus()
    for item in items:
        estoklus.fetch_from_stored_proc('AT_RETIRAR_PECA',item["codigo_pecas_servicos"],item["quantidade_a_retirar"],user)
    
    return {"success":"OK"}

def devolve_peca(item,user):
    estoklus = Estoklus()
    estoklus.fetch_from_stored_proc('AT_DEVOLVER_PECA',item["codigo_pecas_servicos"],item["quantidade"],user)
    
    return {"success":"OK"}















# CÓDIGO ANTIGO DE OS PERFEITAS#
#def tem_romaneio(codigo_os,codigo_produto):
#    os = codigo_os.lstrip(codigo_os[0:2])
#    estoklus = Estoklus()
#    query = f"select 'S' from e_romaneio_item   ei where ei.codigo_os_assist_tecnica = '{codigo_os}' and codigo_produto = '{codigo_produto}' and (select r.status_romaneio from e_romaneio_capa r where r.codigo_romaneio_capa = ei.codigo_romaneio_capa) <> 5"
#    resultado = estoklus.fetchone(query)
#    if resultado == 'S':
#        return True
#    return False
#
#
#def analisar_ordens_servico(unidades_estoque, ordens_servico):
#    separacao = {}
#
#    ordens_servico = dict(sorted(ordens_servico.items(), key=lambda x: '/'.join(x[1]['data_previsao'].split('/')[::-1])))
#
#    for codigo_os, os in ordens_servico.items():
#        unidade_completa = encontrar_unidade_completa(unidades_estoque, os)
#        if unidade_completa:
#            if unidade_completa not in separacao:
#                separacao[unidade_completa] = {}
#            if os['unidade_conserto'] not in separacao[unidade_completa]:
#                separacao[unidade_completa][os['unidade_conserto']] = {}
#            if os['marca'] not in separacao[unidade_completa][os['unidade_conserto']]:
#                separacao[unidade_completa][os['unidade_conserto']][os['marca']] = {}
#            if codigo_os not in separacao[unidade_completa][os['unidade_conserto']][os['marca']]:
#                separacao[unidade_completa][os['unidade_conserto']][os['marca']][codigo_os] = {'items': []}
#            romaneio = False
#            for item in os['items']:
#                if unidade_completa != os['unidade_conserto'] and tem_romaneio(codigo_os, item['codigo_produto']):
#                    romaneio = True
#                    break  # Desconsidera o item se tem romaneio
#            if not romaneio:
#                pode = adicionar_a_separacao(separacao, unidade_completa, os, unidades_estoque)
#                if pode:
#                    for item in os['items']:
#                        item['separacao'] = 'completa'
#                        separacao[unidade_completa][os['unidade_conserto']][os['marca']][codigo_os]['items'].append(item)
#
#        else:
#            unidades_sortidas = encontrar_unidades_sortidas(unidades_estoque, os)
#            if unidades_sortidas:
#                for ref_unidade, itens_unidade in unidades_sortidas:
#                    if ref_unidade not in separacao:
#                        separacao[ref_unidade] = {}
#                    if os['unidade_conserto'] not in separacao[ref_unidade]:
#                        separacao[ref_unidade][os['unidade_conserto']] = {}
#                    if os['marca'] not in separacao[ref_unidade][os['unidade_conserto']]:
#                        separacao[ref_unidade][os['unidade_conserto']][os['marca']] = {}
#                    if codigo_os not in separacao[ref_unidade][os['unidade_conserto']][os['marca']]:
#                        separacao[ref_unidade][os['unidade_conserto']][os['marca']][codigo_os] = {'items': []}
#
#                    for ref_item, qtd in itens_unidade.items():
#                        item = next(item for item in os['items'] if item['referencia'] == ref_item)
#                        item_copia = item.copy()
#                        item_copia['quantidade'] = qtd
#                        item_copia['separacao'] = 'sortida'  
#                        if item_copia['quantidade'] > 0 and (ref_unidade == os['unidade_conserto'] or not tem_romaneio(codigo_os, item['codigo_produto'])):
#                            pode = adicionar_a_separacao(separacao, ref_unidade, {'unidade_conserto': os['unidade_conserto'], 'marca': os['marca'], 'items': [item_copia]}, unidades_estoque)
#                            if pode:
#                                separacao[ref_unidade][os['unidade_conserto']][os['marca']][codigo_os]['items'].append(item_copia)
#    
#    return separacao
#
#def adicionar_a_separacao(separacao, unidade_estoque, ordem_servico, unidades_estoque):
#    if unidade_estoque not in separacao:
#        separacao[unidade_estoque] = {}
#    if ordem_servico['unidade_conserto'] not in separacao[unidade_estoque]:
#        separacao[unidade_estoque][ordem_servico['unidade_conserto']] = {}
#    if ordem_servico['marca'] not in separacao[unidade_estoque][ordem_servico['unidade_conserto']]:
#        separacao[unidade_estoque][ordem_servico['unidade_conserto']][ordem_servico['marca']] = {}
#
#    # Fazendo uma cópia dos itens do estoque
#    estoque_copia = copy.deepcopy(unidades_estoque[unidade_estoque]['items'])
#
#    # Reduzindo a quantidade em estoque na cópia
#    for item in ordem_servico['items']:
#        for estoque_item in estoque_copia:
#            if estoque_item['referencia'] == item['referencia']:
#                if estoque_item['quantidade_disponivel'] >= item['quantidade']:
#                    estoque_item['quantidade_disponivel'] -= item['quantidade']
#                else:
#                    # Não subtrair se a quantidade disponível for menor do que a quantidade necessária
#                    return False
#
#    # Atualizando a quantidade em estoque após verificar todos os itens
#    unidades_estoque[unidade_estoque]['items'] = estoque_copia
#    return True
#
#                    
#
#
#
#def remover_estoque(unidade_estoque, item, quantidade):
#    for produto in unidade_estoque['items']:
#        if produto['referencia'] == item['referencia']:
#            produto['quantidade_disponivel'] -= quantidade
#            break
#def get_os_list():
#    estoklus = Estoklus()
#    querypecas =""" SELECT
#            ast.loja_os,
#            trim(ast.loja_os)||AST.CODIGO_OS_ASSIST_TECNICA CODIGO_OS_ASSIST_TECNICA,
#            AST.FASE_ATUAL,
#            ASTPS.REFERENCIA_FORNECEDOR,
#            ASTPS.DESCRICAO,
#            CASE WHEN (select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos) IS NULL THEN ASTPS.QTDE ELSE QTDE - (select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos) END QTDE,
#            ast.data_prevista_entrega,
#            (select descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica),
#            astps.codigo_produto,
#            astps.descricao,
#            coalesce((select preco from e_produto_preco pp where pp.codigo_produto = astps.codigo_produto and codigo_tipo_preco = 'D'),0)
#            from e_assist_tecnica_pecas_servicos astps
#            left join e_assist_tecnica ast on ast.codigo_os_assist_tecnica = astps.codigo_os_assist_tecnica
#
#            WHERE 
#             
#            AST.status_os in ('05','03') and fase_atual not in (3,7,8) and
#            ASTPS.PECA_OU_SERVICO = 'P' AND astps.codigo_produto not in ('95','0000801') and
#            ASTPS.REFERENCIA_FORNECEDOR <> '' 
#            and qtde -  coalesce((select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos),0) >0
#            """
#    
#
#    os_dict = {}
#    counter = 1
#    for row in estoklus.fetchall(querypecas):
#    # Verifica se o código da OS já está no dicionário
#        if row[1] in os_dict:
#        # Se já está no dicionário, adiciona a peça à lista de peças para essa OS
#            os_dict[row[1]]['items'].append({
#                "referencia": row[3],
#                "quantidade": int(row[5]),
#                "codigo_produto": row[8],
#                "descricao": row[9],
#                "preco": float(row[10]),
#                "codigo_os": row[1],
#                "row_key": counter,
#                'data_previsao': row[6].strftime('%d/%m/%Y')
#            })
#            counter += 1
#        else:
#            # Se não está no dicionário, cria uma nova entrada para a OS com a unidade e a peça
#            os_dict[row[1]] = {
#                'unidade_conserto': row[0],
#                'data_previsao': row[6].strftime('%d/%m/%Y'),
#                'marca': row[7],
#                'items': [
#                    {
#                        "referencia": row[3],
#                        "quantidade": int(row[5]),
#                        "codigo_produto": row[8],
#                        "descricao": row[9],
#                        "preco": float(row[10]),
#                        "codigo_os": row[1],
#                        "row_key": counter,
#                        'data_previsao': row[6].strftime('%d/%m/%Y')
#                    }
#                ]
#            }
#            counter += 1
#
#
#    
#    return os_dict
#
#def tem_estoque(unidade_estoque, referencia, quantidade_necessaria):
#    for item in unidade_estoque['items']:
#        if item['referencia'] == referencia and item['quantidade_disponivel'] >= quantidade_necessaria:
#            return True
#    return False
#
#def tem_todos_itens(unidade_estoque, ordem_servico):
#    for item_os in ordem_servico['items']:
#        tem_item = tem_estoque(unidade_estoque, item_os['referencia'], item_os['quantidade'])
#        if not tem_item:
#            return False
#    return True
#
#def encontrar_unidade_completa(unidades_estoque, ordem_servico):
#    # Primeiro verifica a unidade da ordem de serviço
#    unidade_ordem_servico = ordem_servico.get('unidade_conserto')
#    if unidade_ordem_servico:
#        unidade_estoque = unidades_estoque.get(unidade_ordem_servico)
#        if unidade_estoque and tem_todos_itens(unidade_estoque, ordem_servico):
#            return unidade_ordem_servico
#
#    
#
#    # Se a unidade da ordem de serviço não tem todos os itens, verifica as outras unidades
#    for nome_unidade, unidade in unidades_estoque.items():
#        if nome_unidade != unidade_ordem_servico and tem_todos_itens(unidade, ordem_servico):
#            return nome_unidade
#
#    return None
#
#def encontrar_unidades_sortidas(unidades_estoque, ordem_servico):
#    unidades_possiveis = []
#    itens_necessarios = {item['referencia']: item['quantidade'] for item in ordem_servico['items']}
#    
#    # Primeiro, verifique se a unidade de conserto tem algumas das peças
#    unidade_conserto = ordem_servico['unidade_conserto']
#    if unidade_conserto in unidades_estoque:
#        unidade = unidades_estoque[unidade_conserto]
#        itens_disponiveis = {item['referencia']: item['quantidade_disponivel'] for item in unidade['items']}
#        itens_unidade = {ref: min(qtd, itens_disponiveis.get(ref, 0)) for ref, qtd in itens_necessarios.items()}
#        unidades_possiveis.append((unidade_conserto, itens_unidade))
#        for ref, qtd in itens_unidade.items():
#            itens_necessarios[ref] -= qtd
#
#    # Em seguida, adicione as outras unidades que possuem as peças restantes para suprir a OS
#    for unidade, estoque in unidades_estoque.items():
#        if unidade == unidade_conserto:  # Já verificamos a unidade de conserto
#            continue
#        itens_disponiveis = {item['referencia']: item['quantidade_disponivel'] for item in estoque['items']}
#        itens_unidade = {ref: min(qtd, itens_disponiveis.get(ref, 0)) for ref, qtd in itens_necessarios.items()}
#        unidades_possiveis.append((unidade, itens_unidade))
#        for ref, qtd in itens_unidade.items():
#            itens_necessarios[ref] -= qtd
#
#    # Verifique se todas as unidades juntas suprem a necessidade da OS
#    if all(qtd <= 0 for qtd in itens_necessarios.values()):
#        return unidades_possiveis
#    else:
#        return None
#
#def get_estoques():
#    estoklus = Estoklus()
#    queryestoque = """select referencia_produto,
#    quantidade_atual,codigo_loja from e_produto_quantidade_atual est
#    left join e_produto p on p.codigo_produto = est.codigo_produto
#    where est.quantidade_atual > 0"""
#
#    estoques = {}
#
#    for row in estoklus.fetchall(queryestoque):
#        # Verifica se o código da loja já está no dicionário
#        if row[2] not in estoques:
#            # Se não está no dicionário, cria uma nova entrada para a loja com a lista de itens
#            estoques[row[2]] = {"items": []}
#        
#        # Adiciona a peça à lista de peças para essa loja
#        estoques[row[2]]["items"].append({
#            "referencia": row[0],
#            "quantidade_disponivel": int(row[1])
#        })
#
#    return estoques
#
#
#
#
#def pecas_para_separar(separacao, unidade_estoque):
#    if unidade_estoque not in separacao:
#        print(f"Nenhuma peça para separar para a unidade de estoque {unidade_estoque}.")
#        return
#
#    marcas_impressas = set()
#    for unidade_conserto, marcas in separacao[unidade_estoque].items():
#        print(f"\nPeças para separar para a unidade {unidade_conserto}:")
#        for marca, ordens_servico in marcas.items():
#            if marca not in marcas_impressas:
#                print(f"\nMarca: {marca}")
#                marcas_impressas.add(marca)
#            for codigo_os, os in ordens_servico.items():
#                print("\nOS: ", codigo_os)
#                for item in os['items']:
#                    print(f"   Código da peça: {item['referencia']}, quantidade: {item['quantidade']}")
#
#
#def gerar_excel(separacao, unidade_estoque):
#    if unidade_estoque not in separacao:
#        print(f"Nenhuma peça para separar para a unidade de estoque {unidade_estoque}.")
#        return
#
#    linhas = []
#    for unidade_conserto, marcas in separacao[unidade_estoque].items():
#        for marca, ordens_servico in marcas.items():
#            for codigo_os, os in ordens_servico.items():
#                for item in os['items']:
#                    linha = {
#                        'UNIDADE DE DESTINO': unidade_conserto,
#                        'MARCA': marca,
#                        'OS': codigo_os,
#                        'CODIGO DA PEÇA': item['referencia'],
#                        'DESCRIÇÃO': item["descricao"],
#                        'QUANTIDADE': item['quantidade'],
#                        'TIPO DE SEPARACAO': item["separacao"],
#                        'PREÇO': item["preco"],
#                        "CODIGO_ESTOKLUS":item["codigo_produto"],
#                        "row_key":item["row_key"],
#                    }
#                    linhas.append(linha)
#                    
#    df = pd.DataFrame(linhas)
#    df.to_excel(f'{unidade_estoque}_separacao.xlsx', index=False)
#
#def gerar_separacao():
#
#    unidades_estoque = get_estoques()
#    ordens_servico =get_os_list()
#
#
#    lista = analisar_ordens_servico(unidades_estoque,ordens_servico)
#    return lista 