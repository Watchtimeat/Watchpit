import pytz
from datetime import datetime
from models.estoklus import Estoklus
from models.purchase_orders import get_product_resquested_quantity,create_purchase_order
from models.service_orders import create_service_orders,create_customers,get_customers
from models.service_orders import get_service_orders as get_services,create_service_order_items,get_service_order_items,delete_service_order,delete_customer
from models.estoklus import Estoklus1
import logging
import locale

# Configurar a localidade para 'pt_BR.UTF-8'
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')




logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

def agrupa_pedidos(pedido):
    result = {}
    for item in pedido:
        product_id = item["product_id"]
        product_code = item['product_code']
        requested_quantity = item['requested_quantity']
        codigos_os = item["OS"][0]
        status = item['status']
        product_cost = item['product_cost']
        total_cost = item['total_cost']
        product_name= item['product_name']
        product_category = item['product_category']
        estoque = item['ESTOQUE']
        if product_code in result:
            result[product_code]["product_code"] = product_code
            result[product_code]["product_id"] = product_id
            result[product_code]['requested_quantity'] += requested_quantity
            result[product_code]['OS'].append(codigos_os)
            result[product_code]['status'] == status
            result[product_code]['product_cost'] = product_cost
            result[product_code]['total_cost'] += total_cost
            result[product_code]['product_category'] == product_category
            result[product_code]['product_name'] == product_name
            result[product_code]['ESTOQUE'] == estoque
        else:
            result[product_code] = {'product_id': product_id,'product_code': product_code, 'requested_quantity': requested_quantity, 'OS': [codigos_os] , 'status': status, 'product_cost': product_cost, 'total_cost': total_cost, 'product_category': product_category, 'product_name': product_name, 'ESTOQUE': estoque}

    #checa quantidades solicitadas
    final =[]
    for item in result.values():
        response = get_product_resquested_quantity(item["product_code"])

        qtd = response["requested_quantity"]
        resultado = item["requested_quantity"] - int(qtd) - item["ESTOQUE"]
        if resultado > 0:
            item["requested_quantity"] = resultado
            final.append(item)
    return final



def pedido_por_os(marca,agrupa,owner):

    estoklus = Estoklus1()

    retorno = list()

   ##get_pending_service_orders():
    query =  f"""SELECT
            trim(ast.loja_os)||AST.CODIGO_OS_ASSIST_TECNICA CODIGO_OS_ASSIST_TECNICA,
            AST.FASE_ATUAL,
            P.REFERENCIA_FORNECEDOR,
            ASTPS.DESCRICAO,
            CASE WHEN (select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos) IS NULL THEN ASTPS.QTDE ELSE QTDE - (select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos) END QTDE,
            P.CODIGO_MARCA,
            CASE
                when astps.extra = 'S' then 'QUEBRA/PERDA'
                when astps.GARANTIA = 'S' and ast.tipo_reparo = 2 then 'GARANTIA'
                WHEN astps.GARANTIA = 'S' and ast.tipo_reparo = 3 then 'GARANTIA'
                WHEN astps.GARANTIA = 'S' and ast.tipo_reparo = 8 then 'GARANTIA'
                WHEN astps.GARANTIA = 'S' and ast.tipo_reparo NOT IN (3,2) then 'INCLUIDO NO SERVIÇO'
                WHEN astps.valor_unitario = 0 then 'INCLUIDO NO SERVIÇO'
            else 'A COBRAR' end TIPO,
            CASE
                WHEN c.CODIGO_TIPO_PESSOA = 'J' and c.CODIGO_cadastro_geral IN('210120','209184','208212','209310','208901','S059873','208383') then 'BTQ'
                WHEN C.CODIGO_tipo_pessoa = 'J' then 'CONC'
                else 'CF'
            end ORIGEM,
            coalesce((SELECT sum(quantidade_atual) FROM e_produto_quantidade_atual ea WHERE codigo_produto = astps.codigo_produto),0) ESTOQUE,
            ast.ALTERACAO_DATA,
            coalesce((select preco from e_produto_preco where codigo_produto = astps.codigo_produto and codigo_tipo_preco = '002'),0),
            (select descricao_classe from e_classe  cl left join e_produto pp on cl.codigo_classe = pp.codigo_classe where pp.codigo_produto = astps.codigo_produto )classe
        FROM
            E_ASSIST_TECNICA AST
                LEFT JOIN E_ASSIST_TECNICA_PECAS_SERVICOS ASTPS ON AST.CODIGO_OS_ASSIST_TECNICA = ASTPS.CODIGO_OS_ASSIST_TECNICA
                LEFT JOIN E_PRODUTO P ON ASTPS.codigo_produto = P.codigo_produto
                LEFT JOIN g_cadastro_geral c ON c.codigo_cadastro_geral = ast.codigo_cliente
        WHERE 

            AST.status_os in('03','05')
            AND astps.codigo_produto not in ('95','0000801') AND fase_atual not in (3,7,8)
               and
            ASTPS.PECA_OU_SERVICO = 'P' AND
            ASTPS.REFERENCIA_FORNECEDOR <> '' and qtde -  coalesce((select sum( CASE WHEN E_S = 'S' then quantidade else quantidade * -1 end) from e_movimento_es es where es.codigo_pecas_servicos = astps.codigo_pecas_servicos),0) >0
              and (select FIRST 1 'S' from e_romaneio_item   ei where ei.codigo_os_assist_tecnica <> '' and trim(ast.loja_os)||astps.codigo_os_assist_tecnica = ei.codigo_os_assist_tecnica and ei.codigo_produto = astps.codigo_produto and (select r.status_romaneio from e_romaneio_capa r where r.codigo_romaneio_capa = ei.codigo_romaneio_capa) not in (5,3)) is null
              and P.codigo_marca = (select codigo_marca from e_grupo_os_assist_tecnica m where m.CODIGO_GRUPO_OS = '{marca}')


order by   1 asc"""




    for row in estoklus.fetchall(query) :
    
        custot = float(row[4]) * float(row[10])
        
        retorno.append ({
            "status": "active",
            'OS': [{'code': row[0]}],
            'FASE_ATUAL': row[1],
            'product_id': row[2],
            'product_code': row[2],
            'product_name': row[3],
            'requested_quantity': int(row[4]),
            'DESCRICAO_GRUPO_OS': row[5],
            'TIPO': row[6],
            'ORIGEM': row[7],
            'ESTOQUE': int(row[8]),
            'ALTERACAO_DATA': row[9].strftime('%d/%m/%Y'),
            'product_cost': float(row[10]),
            'total_cost': custot,
            'product_category': row[11] })

    

    if agrupa == 'S':
        retorno = agrupa_pedidos(retorno)
    order = list()
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data = datetime.now(fuso_horario).isoformat()

      
    if not retorno:
        return {"message":"Não foram identificadas pendências de peças"}
    
    query2 ="select descricao_grupo_os from e_grupo_os_assist_tecnica WHERE CODIGO_GRUPO_OS = '" + marca + "'"
    
    
    for row in estoklus.fetchall(query2) :
        brand = row[0]
    
    order = {
                    "brand": brand.upper(),
                    "status": "draft",
                    "mode": "OS",
                    "created": data,
                    "items": retorno,
                    "owner": owner
                }

    result = create_purchase_order(order)

    return {"message": "Pedido " +brand+ " criado com sucesso"}


def get_service_orders():

    estoklus = Estoklus()

    query = "select loja_os,codigo_os_assist_tecnica,data_aprovado,(select descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica), (select count (codigo_pecas_servicos) from e_assist_tecnica_pecas_servicos pc where pc.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and pc.codigo_produto <> '95' and pc.referencia_fornecedor <> '' ) from e_assist_tecnica ast where ast.fase_atual = 4 and   (select count (codigo_pecas_servicos) from e_assist_tecnica_pecas_servicos pc where pc.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and pc.codigo_produto <> '95' and pc.referencia_fornecedor <> '' ) <> 0"

    orders = []
        
    for row in estoklus.fetchall(query):
        orders.append({"loja": row[0],
                 "os": row[1],
                 "approved_date": row[2].strftime('%d/%m/%Y'),
                 "brand": row[3],
                 "pecas": row[4]})
    
    return orders

def gerar_demanda(periodo_inicial,periodo_final,marca):
    estoklus = Estoklus()
    sql = """select
ast.codigo_os_assist_tecnica,
(select gr.descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica),
P.referencia_fornecedor,
p.descricao_produto,
orc.qtde,
ast.data_aprovado,
(select cc.descricao_classe from e_classe cc where cc.codigo_classe = p.codigo_classe)categoria,
coalesce((select preco from e_produto_preco pp where pp.codigo_produto = p.codigo_produto and pp.codigo_tipo_preco = '002'),0)custo,
0 "estoque segurança",
coalesce((select sum(quantidade_atual) from e_produto_quantidade_atual est where est.codigo_produto = p.codigo_produto and est.quantidade_atual >0),0)estoque ,
coalesce((select sum(qtde) from e_assist_tecnica_pecas_servicos os left join e_assist_tecnica astt on astt.codigo_os_assist_tecnica = os.codigo_os_assist_tecnica where os.codigo_produto = p.codigo_produto and astt.fase_atual in (4,5) and (select count(codigo_pecas_servicos) from e_movimento_es es where es.codigo_pecas_servicos = os.codigo_pecas_servicos and e_s = 'S') in(0,2) ),0)ospendentes


from

  e_assist_tecnica_pecas_servicos orc
left join e_assist_tecnica ast on orc.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
left join e_produto p on p.codigo_produto = orc.codigo_produto

where

ast.data_aprovado >= '03/01/2023' and ast.data_aprovado <= '03/31/2023' and ast.aprovado = 'S'
and  orc.referencia_fornecedor not in ('95', '') and orc.peca_ou_servico = 'P' and ast.status_os <> '31'  AND P.CODIGO_PRODUTO <> '95'  and orc.referencia_fornecedor <> ''  and orc.referencia_fornecedor <> 'Juntas de Vedação'
    """
   
    estoklus.fetchall(sql)

    return None


def importar_os(sistema):
    existing_orders = get_services({"_select": "id", "_distinct": True, "_order_a": "id"})
    existing_ids = {customer['id'] for customer in existing_orders['data']}
    estoklus = Estoklus1()
    if sistema == 'novo':

        sql = """select trim(loja_os),trim(loja_os)||codigo_os_assist_tecnica ,(select gr.descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica)marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral



 """
    elif sistema == 'sp':
            estoklus.database = 'D:/CDSIS/Dat/Wservice.CDB'

            sql = """select 'SP','SPA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),(select descricao_tipo_os from e_tipo_os_assist_tecnica where codigo_tipo_os = ast.tipo_reparo),
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),diagnostico,ast.codigo_os_assist_tecnica

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral


 """

    elif sistema == 'rj':
            estoklus.database = 'D:/CDSIS/Dat/wtime.CDB'
            sql = """select 'RJ','RJA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),(select descricao_tipo_os from e_tipo_os_assist_tecnica where codigo_tipo_os = ast.tipo_reparo),
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),diagnostico,ast.codigo_os_assist_tecnica

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral


 """
    elif sistema == 'pr':
            estoklus.database = 'D:/CDSIS/Dat/wservice_cwb.CDB'
            sql = """select 'PR','PRA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),(select descricao_tipo_os from e_tipo_os_assist_tecnica where codigo_tipo_os = ast.tipo_reparo),
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),diagnostico,ast.codigo_os_assist_tecnica

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral


 """
    
    
    os_list = []

    for row in estoklus.fetchall(sql):
             service_id = row[1]
             if service_id not in existing_ids:
                    
                    os_list.append({
    "id": row[1],
    "loja": row[0].upper().strip() if isinstance(row[0], str) else row[0],
    "marca": row[2].upper() if isinstance(row[2], str) else row[2],
    "modelo": row[3].upper() if isinstance(row[3], str) else row[3],
    "referencia_produto": row[4].upper() if isinstance(row[4], str) else row[4],
    "serie": row[5].upper() if isinstance(row[5], str) else row[5],
    "nome": row[6].upper() if isinstance(row[6], str) else row[6],
    "documento": row[7].upper() if isinstance(row[7], str) else row[7],
    "codigo_tipo_pessoa": row[8].upper() if isinstance(row[8], str) else row[8],
    "valor_desconto": float(row[9]),
    "status_os": row[10].upper() if isinstance(row[10], str) else row[10],
    "tipo_reparo": row[11].upper() if isinstance(row[11], str) else row[11],
    "valor_cliente": float(row[12]),
    "valor_bruto": float(row[13]),
    "serviço": float(row[14]),
    "polimento": float(row[15]),
    "valor_pecas": float(row[16]),
    "data_entrega_produto": row[19].strftime('%d/%m/%Y').lower() if row[19] is not None else '',
    "data_os": row[22].strftime('%d/%m/%Y').lower(),
    "data_analise": row[23].strftime('%d/%m/%Y').lower() if row[23] is not None else '',
    "data_aprovado": row[24].strftime('%d/%m/%Y').lower() if row[24] is not None else '',
    "aprovado": row[25].upper() if isinstance(row[25], str) else row[25],
    "data_inicio_conserto": row[26].strftime('%d/%m/%Y').lower() if row[26] is not None else '',
    "data_termino_conserto": row[27].strftime('%d/%m/%Y').lower() if row[27] is not None else '',
    "status": row[28],
    "calibre": row[29].upper() if isinstance(row[29], str) else row[29],
    "cliente_id": row[30].upper() if isinstance(row[30], str) else row[30],
    "os_loja":row[31].upper() if isinstance(row[31], str) else row[31],
    "tipo_movimento":row[32],
    "tipo_complicacao":row[33],
    "defeito":row[34],
    "brand_id":row[35],
    "diagnostico_tecnico":row[36],
    "codigo_estoklus":int(row[37])
})
                    

        
    
    create_service_orders(os_list)
    
    if not os_list:
        return None

    return 'OK'



def importar_clientes():
    existing_customers = get_customers({"_select": "id", "_distinct": True, "_order_a": "id"})
    existing_ids = {customer['id'] for customer in existing_customers['data']}
    estoklus = Estoklus1()
    customer_list = []
    sql = """ select codigo_cadastro_geral, nome,cg.tel_trabalho,cg.tel_celular,cg.tel_outros,cg.cpf,cg.cnpj,cg.codigo_tipo_pessoa, logradouro,cg.numero,complemento,bairro,cidade,cg.cep,cg.uf,cg.email,cg.codigo_ibge_municipio,nascimento,(select resposta from g_cadastro_geral_campo_auxiliar where codigo_cadastro_geral = cg.codigo_cadastro_geral and codigo_campo_auxiliar = 2)
    

from g_cadastro_geral cg  where codigo_tipo_pessoa <> 'E' and (alteracao_data>= 'today' or inclusao_data >= 'today') """
    for row in estoklus.fetchall(sql):
            customer_id = row[0].upper() if isinstance(row[0], str) else row[0]
        
        # Verificar se o ID do cliente já existe antes de inserir



            if customer_id in existing_ids:
                delete_customer(customer_id)

            customer_list.append({
    "id": row[0].upper() if isinstance(row[0], str) else row[0],
    "nome": row[1].upper() if isinstance(row[0], str) else row[1],
    "tel_trabalho": row[2].upper() if isinstance(row[2], str) else row[2],
    "tel_celular": row[3].upper() if isinstance(row[3], str) else row[3],
    "tel_outros": row[4].upper() if isinstance(row[4], str) else row[4],
    "cpf": row[5].upper() if isinstance(row[5], str) else row[5],
    "cnpj": row[6].upper() if isinstance(row[6], str) else row[6],
    "codigo_tipo_pessoa": row[7].upper() if isinstance(row[7], str) else row[7],
    "logradouro": row[8].upper() if isinstance(row[8], str) else row[8],
    "numero": row[9].upper() if isinstance(row[9], str) else row[9],
    "complemento": row[10].upper() if isinstance(row[10], str) else row[10],
    "bairro": row[11].upper() if isinstance(row[11], str) else row[11],
    "cidade": row[12].upper() if isinstance(row[12], str) else row[12],
    "cep": row[13].upper() if isinstance(row[13], str) else row[13],
    "uf": row[14].upper() if isinstance(row[14], str) else row[14],
    "email": row[15].upper() if isinstance(row[15], str) else row[15],
    "codigo_ibge": row[16].upper() if isinstance(row[16], str) else row[16],
    "nascimento": row[17]
})
    create_customers(customer_list)

    return customer_list        


def grupo_estoklus(grupo):
    estoklus = Estoklus1()
    query="""select  gr.descricao_subgrupo,gr.codigo_subgrupo from   g_subgrupo gr where codigo_grupo ='"""+grupo+"'"

    return [{
        'label': row[0],
        'id': row[1],
    } for row in estoklus.fetchall(query)]

def usuarios_estoklus():
    estoklus = Estoklus1()
    query="select codigo_usuario,nome from b_usuario where ativo = 'S ' order by nome asc"

    return [{
        'label': row[1],
        'id': row[0],
    } for row in estoklus.fetchall(query)]



def importar_pecas(sistema):
    estoklus = Estoklus1()
    existing_orders = get_service_order_items({"_select": "id", "_distinct": True, "_order_a": "id"})
    existing_ids = {customer['id'] for customer in existing_orders['data']}

    if sistema == 'novo':
        query = """
    SELECT    ast.referencia_produto,
        ast.grupo_os_assist_tecnica,
        modelo,
        LOJA_OS||ast.codigo_os_assist_tecnica,
        aps.referencia_fornecedor,
        aps.descricao, 
        aps.peca_ou_servico,
        aps.extra,
        aps.valor_unitario,
        aps.qtde,
        aps.codigo_produto


    FROM
        e_assist_tecnica ast
    JOIN 
        e_assist_tecnica_pecas_servicos aps ON ast.codigo_os_assist_tecnica = aps.codigo_os_assist_tecnica
    WHERE
        aps.referencia_fornecedor <> '' and referencia_produto <> ''
    """
    elif sistema == 'sp':
            estoklus.database = 'D:/CDSIS/Dat/wservice.CDB'
            query = """
    SELECT    ast.referencia_produto,
        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),
        modelo,
        'SPA'||ast.codigo_os_assist_tecnica,
        aps.referencia_fornecedor,
        aps.descricao, 
        aps.peca_ou_servico,
        aps.extra,
        aps.valor_unitario,
        aps.qtde,
        aps.codigo_produto


    FROM
        e_assist_tecnica ast
    JOIN 
        e_assist_tecnica_pecas_servicos aps ON ast.codigo_os_assist_tecnica = aps.codigo_os_assist_tecnica
    WHERE
        aps.referencia_fornecedor <> '' and referencia_produto <> ''
    """
    elif sistema == 'pr':
            estoklus.database = 'D:/CDSIS/Dat/wservice_cwb.CDB'
            query = """
    SELECT    ast.referencia_produto,
        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),
        modelo,
        'PRA'||ast.codigo_os_assist_tecnica,
        aps.referencia_fornecedor,
        aps.descricao, 
        aps.peca_ou_servico,
        aps.extra,
        aps.valor_unitario,
        aps.qtde,
        aps.codigo_produto


    FROM
        e_assist_tecnica ast
    JOIN 
        e_assist_tecnica_pecas_servicos aps ON ast.codigo_os_assist_tecnica = aps.codigo_os_assist_tecnica
    WHERE
        aps.referencia_fornecedor <> '' and referencia_produto <> ''
    """
    elif sistema == 'rj':
        estoklus.database = 'D:/CDSIS/Dat/wtime.CDB'
        query = """
    SELECT    ast.referencia_produto,
                (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ),
        modelo,
        'RJA'||ast.CODIGO_OS_ASSIST_TECNICA,
        aps.referencia_fornecedor,
        aps.descricao, 
        aps.peca_ou_servico,
        aps.extra,
        aps.valor_unitario,
        aps.qtde,
        aps.codigo_produto


    FROM
        e_assist_tecnica ast
    JOIN 
        e_assist_tecnica_pecas_servicos aps ON ast.codigo_os_assist_tecnica = aps.codigo_os_assist_tecnica
    WHERE
        aps.referencia_fornecedor <> '' and referencia_produto <> ''
    """

    rows = estoklus.fetchall(query)
    
    os_dict = []
    for row in rows:
        os_id = row[3]
        os_dict.append({
            "id": os_id,
            "referencia_produto": row[0],
            "referencia_fornecedor": row[4],
            "quantidade": int(row[9]), 
            "descricao": row[5],
            "extra": row[7],
            "valor_unitario": float(row[8]),
            "codigo_produto": row[10], 
            "tipo_peca": row[6]
            })

    create_service_order_items(os_dict)


def orcamento_estoklus(referencia):
    estoklus = Estoklus1()
    query = f"""select distinct orc.codigo_produto,(select first 1 referencia_produto from e_produto where codigo_produto = orc.codigo_produto),(select first 1 descricao_produto from e_produto where codigo_produto = orc.codigo_produto)

from e_assist_tecnica_pecas_servicos orc
left join e_assist_tecnica ast on orc.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica


where ast.referencia_produto = '{referencia}' and (select first 1 codigo_tipo_produto from e_produto p where p.codigo_produto = orc.codigo_produto) = '1' order by 2 asc"""
    
    return [{
        'label': row[2],
        'id': row[0],
        'referencia': row[1]


    } for row in estoklus.fetchall(query)]

def consulta_peca_estoklus(referencia):
    estoklus = Estoklus1()
    query = f"""select distinct p.codigo_produto,referencia_produto,descricao_produto,coalesce((SELECT FIRST 1 PRECO FROM E_PRODUTO_PRECO WHERE CODIGO_PRODUTO = p.CODIGO_PRODUTO AND CODIGO_TIPO_PRECO = '001'),0),coalesce((SELECT FIRST 1 PRECO FROM E_PRODUTO_PRECO WHERE CODIGO_PRODUTO = p.CODIGO_PRODUTO AND CODIGO_TIPO_PRECO = 'D'),0),coalesce((SELECT coalesce(sum(quantidade_atual),0) FROM E_PRODUTO_quantidade_atual WHERE CODIGO_PRODUTO = p.CODIGO_PRODUTO and quantidade_atual >0),0)

 from e_produto p


where p.referencia_produto = '{referencia}' and codigo_tipo_produto = 1 and ativo = 'S'"""
    
    return [{
        'label': row[2],
        'id': row[0],
        'referencia': row[1],
        'preco_venda': row[3],
        'preco_custo': row[4],
        'estoque': row[5]


    } for row in estoklus.fetchall(query)]



def consulta_servico_estoklus(marca):
    estoklus = Estoklus1()
    query = f"""select distinct p.codigo_produto,referencia_produto,descricao_produto,COALESCE((SELECT FIRST 1 PRECO FROM E_PRODUTO_PRECO WHERE CODIGO_PRODUTO = p.CODIGO_PRODUTO AND CODIGO_TIPO_PRECO = '001'),0),(SELECT FIRST 1 PRECO FROM E_PRODUTO_PRECO WHERE CODIGO_PRODUTO = p.CODIGO_PRODUTO AND CODIGO_TIPO_PRECO = 'D')

 from e_produto p


where (p.codigo_marca = '{marca}' and codigo_tipo_produto = 2 and ativo = 'S'  ) or CODIGO_PRODUTO = '0101679'"""
    
    return [{
        'label': row[2],
        'id': row[0],
        'referencia': row[1],
        'preco_venda': row[3],
        'preco_custo': row[4]

    } for row in estoklus.fetchall(query)]



def consulta_dados_marca(marca):
    estoklus = Estoklus1()
    query = f"""select URL,USUARIO,SENHA,DESCONTO_PF,DESCONTO_PJ,PRAZO,GARANTIA

 from e_grupo_os_assist_tecnica 


where codigo_grupo_os = '{marca}'"""
    
    return [{
        'URL': row[0],
        'USUARIO': row[1],
        'SENHA': row[2],
        'DESCONTO_PF': row[3],
        'DESCONTO_PJ': row[4],
        'PRAZO': row[5],
        'GARANTIA': row[6]

    } for row in estoklus.fetchall(query)]


def atualizar_os(sistema):
    existing_orders = get_services({"_select": "id", "_distinct": True, "_order_a": "id"})
    existing_ids = {os['id'] for os in existing_orders['data']}
    estoklus = Estoklus1()
    if sistema == 'novo':

        sql = """select trim(loja_os),trim(loja_os)||codigo_os_assist_tecnica ,(select gr.descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica)marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica,
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '83'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '86'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '13'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '14'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '15'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '84'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '85'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                                        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),data_prevista_entrega



 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral

  where (ast.alteracao_data >='today' or ast.inclusao_data >= 'today')


 """
    elif sistema == 'sp':
            estoklus.database = 'D:/CDSIS/Dat/Wservice.CDB'

            sql = """select 'SP','SPA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica,
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '83'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '86'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '13'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '14'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '15'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '84'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '85'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                                        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),data_prevista_entrega
 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral
 where data_os >= '01/01/2018'

 """

    elif sistema == 'rj':
            estoklus.database = 'D:/CDSIS/Dat/wtime.CDB'
            sql = """select 'RJ','RJA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
   Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica,
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '83'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '86'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '13'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '14'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '15'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '84'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '85'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                                        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),data_prevista_entrega

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral

 """
    elif sistema == 'pr':
            estoklus.database = 'D:/CDSIS/Dat/wservice_cwb.CDB'
            sql = """select 'PR','PRA'||codigo_os_assist_tecnica ,(
        SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'G' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '1'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            ))marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
   Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica,
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '83'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '86'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '13'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '14'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '15'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '84'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '85'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                                        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),data_prevista_entrega

 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral
 

 """
    
    
    os_list = []

    for row in estoklus.fetchall(sql):
             delete_service_order(row[1])
             os_list.append({
    "id": row[1],
    "loja": row[0].upper().strip() if isinstance(row[0], str) else row[0],
    "marca": row[2].upper() if isinstance(row[2], str) else row[2],
    "modelo": row[3].upper() if isinstance(row[3], str) else row[3],
    "referencia_produto": row[4].upper() if isinstance(row[4], str) else row[4],
    "serie": row[5].upper() if isinstance(row[5], str) else row[5],
    "nome": row[6].upper() if isinstance(row[6], str) else row[6],
    "documento": row[7].upper() if isinstance(row[7], str) else row[7],
    "codigo_tipo_pessoa": row[8].upper() if isinstance(row[8], str) else row[8],
    "valor_desconto": float(row[9]),
    "status_os": row[10].upper() if isinstance(row[10], str) else row[10],
    "tipo_reparo": int(row[11]),
    "valor_cliente": float(row[12]),
    "valor_bruto": float(row[13]),
    "serviço": float(row[14]),
    "polimento": float(row[15]),
    "valor_pecas": float(row[16]),
    "data_entrega_produto": row[19].strftime('%Y-%m-%d').lower() if row[19] is not None else '',
    "data_os": row[22].strftime('%Y-%m-%d').lower(),
    "data_analise": row[23].strftime('%Y-%m-%d').lower() if row[23] is not None else '',
    "data_aprovado": row[24].strftime('%Y-%m-%d').lower() if row[24] is not None else '',
    "aprovado": row[25].upper() if isinstance(row[25], str) else row[25],
    "data_inicio_conserto": row[26].strftime('%Y-%m-%d').lower() if row[26] is not None else '',
    "data_termino_conserto": row[27].strftime('%Y-%m-%d').lower() if row[27] is not None else '',
    "status": row[28],
    "calibre": row[29].upper() if isinstance(row[29], str) else row[29],
    "cliente_id": row[30].upper() if isinstance(row[30], str) else row[30],
    "os_loja":row[31].upper() if isinstance(row[31], str) else row[31],
    "tipo_movimento":int(row[32]) if isinstance(row[32], str) else '',
    "complicacao":int(row[33]) if isinstance(row[33], str) else '',
    "defeito":row[34],
    "brand_id":row[35],
    "diagnostico_tecnico":row[36],
    "codigo_estoklus":row[37],
    "repair_bre":row[38],
    "repair_tag":row[39],
    "orcamentista":row[40],
    "calibre_marca":row[41],
    "un_min":row[42],
    "variacao_sm":row[43],
    "consumo_ua":row[44],
    "amplitude":row[45],
    "variacao_sd":row[46],
    "intervencao":row[47],
    "data_prevista_entrega": row[48].strftime('%Y-%m-%d').lower() if row[48] is not None else ''
})
           

                       

        
    
    create_service_orders(os_list)
    
    if not os_list:
        return None

    return 'OK'



def get_pecas(os):
    estoklus = Estoklus1()

    sqlpeca = f"""select p.referencia_produto,orc.descricao, p.codigo_produto, CASE
when orc.valor_unitario = 0 and orc.peca_ou_servico = 'P' then 'I'
when ORC.peca_ou_servico = 'S' and extra = 'N'   then 'S'
when  ORC.peca_ou_servico = 'S' and extra = 'O'   then 'SO'
WHEN ORC.peca_ou_servico = 'P' and extra = 'N'   then 'P'
when ORC.peca_ou_servico = 'P' and extra = 'O'   then 'OP' end tipo,
orc.qtde,
orc.valor_unitario  ,
coalesce((select sum(est.quantidade_atual) from e_produto_quantidade_atual est where codigo_produto = p.codigo_produto),0),
case when ORC.peca_ou_servico = 'P' then coalesce((select max(preco) from e_produto_preco est where codigo_produto = p.codigo_produto and codigo_tipo_preco = 'D'),0)
else 150 * ORC.qtde end




from
e_assist_tecnica ast
left join e_assist_tecnica_pecas_servicos orc on ast.codigo_os_assist_tecnica = orc.codigo_os_assist_tecnica
left join e_produto p on orc.codigo_produto = p.codigo_produto
where ast.codigo_os_assist_tecnica = {os}"""
    items = []
    for row in estoklus.fetchall(sqlpeca):
        
        if row[1]:
            items.append({
                     "id":row[2],
                     "label":row[1],
                     "preco_custo":row[7],
                     "preco_venda":row[5],
                     "referencia":row[0],
                     "quantidade":row[4],
                     "tipo":row[3].strip() if row[3] else '',
                     "estoque":row[6]
                 })
        
    return items


def get_capa_os(os):
            capa = []

            estoklus = Estoklus() 
            sql = f"""select
               Coalesce(( SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '10'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '')   ,


                  Coalesce(  (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '11'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),'')    GARANTIA,
                CASE WHEN coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) = 0 then 0 else  Round(  ((ast.valor_desconto) /    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) )* 100 ,2) end,

    (select coalesce(sum(pg.valor),0) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica)pgto,
    DESCONTO_PF,CASE WHEN AST.codigo_cliente = 'PADA BR100206' THEN 25 ELSE DESCONTO_PJ END,cast(CASE WHEN DATA_PREVISTA_ENTREGA IS NULL THEN PRAZO ELSE
     DATA_PREVISTA_ENTREGA - DATA_ANALISE END as integer),GARANTIA,DIAGNOSTICO


                    from e_assist_tecnica ast
                    left join e_grupo_os_assist_tecnica gr on ast.grupo_os_assist_tecnica = gr.codigo_grupo_os
                    where codigo_os_assist_tecnica = {os} """

            for row in estoklus.fetchall(sql):
                capa =    {
                'prazo_cx': row[0],
                'garantia':  row[1],
                'desconto':  row[2],
                'valor_pago': row[3],
                'desconto_pf':row[4],
                'desconto_pj':row[5],
                'prazo':row[6],
                'diagnostico_tecnico':row[8]
                }

            return capa


def get_os_completa(os):
     
    data_atual = datetime.now()

    # Mapeando o número do mês para o nome em português
    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }
    data = data_atual.day
    mes = meses[data_atual.month]
    ano = data_atual.year
    data_documento = f"{data}, {mes}, {ano}"
    estoklus=Estoklus1()
    query = f"""select   
cg.nome,
ast.referencia_os_cliente,
ast.codigo_os_assist_tecnica,
ast.grupo_os_assist_tecnica,
CASE WHEN CG.codigo_tipo_pessoa = 'F' then CPF else CNPJ end  ,
cg.email,
cg.tel_celular,
CASE WHEN CG.codigo_tipo_pessoa = 'F' then cg.identidade else cg.inscricao_estadual end  ,
cg.contato   ,
cg.cep,
cg.logradouro,
cg.bairro,
cg.cidade,
cg.uf,
ast.tipo_reparo,
gr.descricao_grupo_os,
ast.modelo,
ast.referencia_produto,
ast.serie,
ast.valor_produto,
ast.data_os,
'' as portador,
ast.inclusao_por,
ast.tipo_reparo,
Coalesce(( SELECT atca.resposta
            FROM e_assist_tecnica_campo_auxiliar atca
            WHERE atca.codigo_campo_auxiliar = '10'
                AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '') prazo,
ast.data_analise,
ast.tecnico_analise,
ast.diagnostico,
ast.acessorios,
ast.defeito,
ast.detalhes,
'Conserto Total' tipo_servico,
cg.complemento,
(select b.nome from b_usuario b where b.codigo_usuario = ast.inclusao_por),
tp.descricao_tipo_os,
cg.tel_residencial,
cg.numero,
CASE WHEN CG.codigo_tipo_pessoa = 'J' THEN Coalesce(( SELECT atca.resposta
            FROM e_assist_tecnica_campo_auxiliar atca
            WHERE atca.codigo_campo_auxiliar = '5'
                AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '') ELSE coalesce((select first 1 numero_nf_controle from e_movimento_es es where es.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and e_s = 'E' and
codigo_cfop in ('1915','2915')),0) end  NF_ENTRADA,
ast.observacao_produto,
ast.observacao_analise,
  Coalesce(( SELECT atca.resposta
            FROM e_assist_tecnica_campo_auxiliar atca
            WHERE atca.codigo_campo_auxiliar = '89'
                AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '') TIPO_intervencao
,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra = 'N'),0) bruto_obrigatorios,
                    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ),0) bruto_opcional,


case when valor_desconto=0 then  0 else coalesce( cast((valor_desconto / (Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )) as float) * 100 ,0) end desconto,
     COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) liquido,
    Coalesce(( SELECT atca.resposta
            FROM e_assist_tecnica_campo_auxiliar atca
            WHERE atca.codigo_campo_auxiliar = '11'
                AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '')
                ,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra = 'O' ),0),
    Coalesce(( SELECT atca.resposta
            FROM e_assist_tecnica_campo_auxiliar atca
            WHERE atca.codigo_campo_auxiliar = '56'
                AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica) , '') TIPO_MECANISMO,
                coalesce((SELECT sg.descricao_subgrupo
        FROM g_subgrupo sg
        WHERE sg.codigo_grupo = 'TR' 
            AND sg.codigo_subgrupo = (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica
            )),''),
            f.email,
             (select coalesce(sum(pg.valor),0) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica)pgto,
             case when ast.data_inicio_preparacao is null and ast.data_inicio_conserto is not null then
             data_inicio_conserto else ast.data_inicio_preparacao end data_inicio_preparacao,
              case when ast.data_inicio_preparacao is null and ast.data_inicio_conserto is not null then
             data_inicio_conserto else ast.data_termino_preparacao end data_termino_preparacao,
             
               case when ast.data_inicio_preparacao is null and ast.data_inicio_conserto is not null then
             data_inicio_conserto else data_inicio_polimento end  data_inicio_polimento ,
               case when ast.data_inicio_preparacao is null and ast.data_inicio_conserto is not null then
             data_inicio_conserto else data_termino_polimento end  data_termino_polimento ,
               case when ast.data_inicio_preparacao  IS NULL and ast.data_inicio_conserto IS NOT NULL then
             data_inicio_conserto else data_inicio_servico end  data_inicio_servico ,
               case when ast.data_inicio_preparacao  IS NULL and ast.DATA_TERMINO_CONSERTO IS NOT NULL then
             data_inicio_conserto else DATA_TERMINO_SERVICO end  DATA_TERMINO_SERVICO ,
             ast.data_inicio_conserto,
             ast.data_termino_conserto,
case when ast.data_inicio_preparacao  IS NULL and ast.data_inicio_conserto IS NOT NULL then
ast.tecnico_responsavel_conserto else ast.tecnico_preparacao end  tecnico_preparaca,
  case when ast.data_inicio_preparacao  IS NULL and ast.data_inicio_conserto IS NOT NULL then
ast.tecnico_responsavel_conserto else ast.tecnico_polimento end  tecnico_polimento ,
  case when ast.data_inicio_preparacao  IS NULL and ast.data_inicio_conserto IS NOT NULL then
ast.tecnico_responsavel_conserto else ast.tecnico_servico end  tecnico_servico,
fase_atual,
status_os,
fs.descricao,
st.descricao_status_os,
data_aprovado,
data_liberado_execucao,
loja_os,
cg.codigo_cadastro_geral,
data_prevista_entrega,
cg.codigo_tipo_pessoa,
data_entrega_produto,
(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '43'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '26'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '24'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '25'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '32'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '29'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '31'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '30'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '35'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '37'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '34'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                            (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '36'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                            (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '38'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    coalesce(data_termino_controle,data_termino_conserto),ast.status_os




from e_assist_tecnica ast
join g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral
join e_grupo_os_assist_tecnica gr on gr.codigo_grupo_os = ast.grupo_os_assist_tecnica
join e_tipo_os_assist_tecnica tp on tp.codigo_tipo_os = ast.tipo_reparo
left join b_usuario f on f.codigo_usuario = ast.inclusao_por
join e_status_os_assist_tecnica st   on st.codigo_status_os = ast.status_os
join e_i_fase_os_assist_tecnica fs on fs.codigo = ast.fase_atual


where ast.codigo_os_assist_tecnica = {os}"""
     
    service = []
    for row in estoklus.fetchall(query):
        service.append({
        'nome': formatar_nome(row[0]),
        'os_loja': row[1] if row[1] else '-',
        'codigo_estoklus': row[2],
        'id': f"{row[68].strip()}{row[2]}",
        'brand_id': row[3],
        'documento': formatar_documento(row[4]),
        'email': row[5].lower(),
        'tel_celular':formatar_telefone(row[6]),
        'rg': row[7] if row[7] else '',
        'contato': formatar_nome(row[8]),
        'cep': formatar_cep(row[9]),
        'logradouro': formatar_nome(row[10]),
        'complemento': formatar_nome(row[32]),
        'bairro': formatar_nome(row[11]),
        'cidade': formatar_nome(row[12]),
        'uf': row[13],
        'tipo_reparo': int(row[14]),
        'marca': formatar_nome(row[15]),
        'modelo': formatar_nome(row[16]),
        'referencia_produto': row[17],
        'serie': row[18],
        'valor_produto':  locale.currency(float(row[19]), grouping=True, symbol=None),
        'data_os': formatar_data(row[20]),
        'portador': formatar_nome(row[21]),
        'tecnico_abertura': row[22],
        'nome_tecnico': formatar_nome(row[33]),
        'codigo_reparo': int(row[23]),
        'nome_reparo': formatar_nome(row[34]),
        'prazo_entrega': row[24] if row[24] else '-',
        'data_analise': formatar_data(row[25]),
        'tecnico_analise': row[26] if row[26] else '-',
        'diagnostico_tecnico': row[27] if row[27] else '-',
        'acessorios': row[28],
        'defeito': row[29] if row [29] else '-',
        'detalhes': row[30] if row [30] else '-',
        'tipo_servico': row[31],
        'telefone':formatar_telefone(row[35]) if row [35] else '-',
        'numero': row[36] if row [36] else '-',
        'data_documento':data_documento,
        'nf_entrada':row[37],
        'data_compra': '-',
        'observacao': row[38],
        'observacao_orcamento': row[39],
        'intervencao': row[40],
        'bruto_obrigatorios':float(row[41]),
        'bruto_opcional': float(row[42]),
        'desconto': float(row[43]),
        'desconto_obrigatorios': locale.currency(round(float(row[41])  * (float(row[43]) / 100),2), grouping=True, symbol=None),
        'desconto_opcionais': locale.currency((float(row[46]) + float(row[41])) * (float(row[43]) / 100), grouping=True, symbol=None),
        'liquido_obrigatorios':locale.currency(float(row[41]) - (float(row[41])  * (float(row[43]) / 100)), grouping=True, symbol=None) ,
        'liquido_opcionais': locale.currency(float(row[44]), grouping=True, symbol=None) ,
        'garantia': row[45],
        'valor_opcionais': locale.currency(float(row[46]), grouping=True, symbol=None),
        'tipo_mecanismo':row[47],
        'descricao_intervencao': row[48],
        'email_funcionario':row[49],
        'valor_pago': locale.currency(float(row[50]), grouping=True, symbol=None),
        "data_inicio_preparacao":row[51].strftime('%Y-%m-%d') if row[51] else '',
        "data_termino_preparacao":row[52].strftime('%Y-%m-%d') if row[52] else '',
        "data_inicio_polimento":row[53].strftime('%Y-%m-%d') if row[53] else '',
        "data_termino_polimento":row[54].strftime('%Y-%m-%d') if row[54] else '',
        "data_inicio_servico":row[55].strftime('%Y-%m-%d') if row[55] else '',
        "data_termino_servico":row[56].strftime('%Y-%m-%d') if row[56] else '',
        "data_inicio_conserto":row[57].strftime('%Y-%m-%d') if row[57] else '',
        "data_termino_conserto":row[58].strftime('%Y-%m-%d') if row[58] else '',
        "tecnico_preparacao": row[59],
        "tecnico_polimento": row[60],
        "tecnico_servico": row[61],
        "status_os": row[62],
        "fase": row[63],
        "nome_status": row[64],
        "nome_fase": row[65],
        'data_aprovado':row[66].strftime('%Y-%m-%d') if row[66] else '',
        'data_liberado_execucao': row[67].strftime('%Y-%m-%d') if row[67] else '',
        'loja':row[68].strip(),
        'cliente_id':row[69],
        'data_prevista': row[70].strftime('%Y-%m-%d') if row[70] else '',
        'tipo_pessoa':row[71],
        'data_entrega_produto': row[72].strftime('%Y-%m-%d') if row[72] else '',
        "contrato_richemont":row[73],
        "repair_tag":   row[74],
        "defect_tag": row[75],
        "warranty_tag": row[76],
        "country_tag": row[77],
        "repair_bre": row[78],
        "tracking_id_breitling": row[79],
        "defect_bre": row[80], 
        "ultimo_conserto_bre": row[81],
        "pais_bre": row[82],
        "codigo_v02_bv_1":row[83] ,
        "codigo_v01_bv_1": row[84],
        "codigo_sap_bv": row[85],
        "codigo_v01_bv_2": row[86],
        "codigo_v02_bv_2": row[87],
        "data_liberado_entrega": row[88].strftime('%Y-%m-%d') if row[88] else '',
        "status_finalizado": row[89]        
        })

        queryorc = f"""select  orc.descricao,orc.qtde,round(orc.valor_unitario * qtde,2),extra,peca_ou_servico,orc.referencia_fornecedor,
        Coalesce((Select Sum(Case When mes.e_s = 'S' then mes.quantidade else mes.quantidade * -1 end) From E_MOVIMENTO_ES mes 
              Where mes.codigo_pecas_servicos = orc.codigo_pecas_servicos),0) as qtde_retirada,coalesce((select quantidade_atual from e_produto_quantidade_atual 
              where codigo_produto = orc.codigo_produto and codigo_loja = ast.loja_os ),0),codigo_pecas_servicos,orc.codigo_produto

from e_assist_tecnica ast
join e_assist_tecnica_pecas_servicos   orc on ast.codigo_os_assist_tecnica = orc.codigo_os_assist_tecnica

where orc.codigo_os_assist_tecnica = {os}

order by peca_ou_servico desc ,valor_unitario desc"""
        itens = []
        for row in estoklus.fetchall(queryorc):
             itens.append({
                  'descricao': row[0],
                  'tipo': row[3],
                  'quantidade': int(row[1]),
                  'valor_cliente':  locale.currency(float(row[2]), grouping=True, symbol=None),
                  "servico":  row[4],
                  "referencia_produto": row[5],
                  "quantidade_retirada": int(row[6]),
                  "estoque": int(row[7]),
                  "codigo_pecas_servicos": int(row[8]),
                  "codigo_produto": row[9]
             })
        service[0]["itens"] = itens

    return service








def formatar_nome(nome):
    if not nome:
        return "-"

    # Lista de palavras que não devem ser capitalizadas
    excecoes = ["da", "de", "do", "e","DA", "DE", "DO", "E"]
    
    # Divide o nome em palavras
    palavras = nome.split()
    
    # Capitaliza a primeira letra de cada palavra, exceto as que estão na lista de exceções
    nome_formatado = " ".join([palavra.title() if palavra.lower() not in excecoes else palavra.lower() for palavra in palavras])
    
    return nome_formatado


def formatar_documento(doc):
    # Removendo caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, doc))
    
    # Formatando CPF
    if len(numeros) == 11:
        return "{}.{}.{}-{}".format(numeros[:3], numeros[3:6], numeros[6:9], numeros[9:])
    
    # Formatando CNPJ
    elif len(numeros) == 14:
        return "{}.{}.{}/{}-{}".format(numeros[:2], numeros[2:5], numeros[5:8], numeros[8:12], numeros[12:])
    
    # Retornando o documento original caso não seja CPF nem CNPJ
    else:
        return doc
    

def formatar_cep(cep):
    # Removendo caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, cep))
    
    # Formatando CEP
    if len(numeros) == 8:
        return "{}-{}".format(numeros[:5], numeros[5:])
    
    # Retornando o CEP original caso não tenha 8 dígitos
    else:
        return cep
    

def formatar_data(data):
    if data is None:
        return "-"
    return data.strftime('%d/%m/%Y')


def formatar_telefone(telefone):
    if telefone is None or telefone == '':
        return "-"
    # Removendo caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, telefone))
    
    # Formatando telefone com nono dígito
    if len(numeros) == 11:
        return "({}) {}-{}".format(numeros[:2], numeros[2:7], numeros[7:])
    
    # Formatando telefone sem nono dígito
    elif len(numeros) == 10:
        return "({}) {}-{}".format(numeros[:2], numeros[2:6], numeros[6:])
    
    # Retornando o telefone original caso não tenha 10 ou 11 dígitos
    else:
        return telefone 


def gera_nf_entrada_final (os):
    from models.estoklus.services import gerar_nf_entrada
    service = get_os_completa(os)[0]
    if service["nf_entrada"] == "0":
        service["nf_entrada"] = ""
    service["id"]= f"{service['loja']}{str(service['codigo_estoklus'])}"
    service["valor_produto"] = service["valor_produto"].replace('.', '').replace(',', '.')
    service["valor_produto"] = float(service["valor_produto"])
    return gerar_nf_entrada(service,'E')

gera_nf_entrada_final(24981)

def atualizar_os_single(os):
    estoklus = Estoklus1()

    sql = f"""select trim(loja_os),trim(loja_os)||codigo_os_assist_tecnica ,(select gr.descricao_grupo_os from e_grupo_os_assist_tecnica gr where gr.codigo_grupo_os = ast.grupo_os_assist_tecnica)marca,modelo,referencia_produto,serie,nome,case when cg.cpf = '' then cg.cnpj else cg.cpf end,cg.codigo_tipo_pessoa,ast.valor_desconto,(select descricao_status_os from e_status_os_assist_tecnica where codigo_status_os = ast.status_os),ast.tipo_reparo,
    COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0) valor_liquido,
    coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.extra <> 'S'),0) valor_bruto,
    Coalesce(coalesce((Select
     coalesce(Sum(atps_.VALOR_UNITARIO*atps_.QTDE),0)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao not like '%Poli%'),0),0) servico,
coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'S' and atps_.descricao like '%Pol%'),0) polimento
, coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P'  and atps_.extra <> 'S'),0) valor_pecas ,
    COALESCE((select Sum(coalesce((select max(preco) from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0) and pp.codigo_produto <> '95'),valor_unitario /2)*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N'  and atps_.peca_ou_servico = 'P' and atps_.valor_unitario > 0  and atps_.extra <> 'S'),0) custo_pecas_cobradas,
    COALESCE((SELECT Sum((select preco from e_produto_preco pp where codigo_produto = atps_.codigo_produto and codigo_tipo_preco = 'D' and ((pp.inclusao_data <= ast.inclusao_data and preco >0) or preco >0)and pp.codigo_produto <> '95' )*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and ( ast.grupo_os_assist_tecnica) not in ('BA','CA','JC','IW','MB','VC','PI','OP')  and atps_.peca_ou_servico = 'P' and (atps_.valor_unitario = 0 or atps_.garantia = 'S' or  atps_.extra = 'S')),0) custo_pecas_inclusas
,DATA_ENTREGA_PRODUTO
,''
,  COALESCE(((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S' ) - ast.VALOR_DESCONTO ) * 0.18,0) imposto
,data_os,data_analise,data_aprovado,aprovado,data_inicio_conserto,data_termino_conserto,fase_atual,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '12'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),codigo_cadastro_geral,REFERENCIA_OS_CLIENTE,(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '56'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),(
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '57'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),defeito, grupo_os_assist_tecnica,diagnostico,ast.codigo_os_assist_tecnica,
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '83'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '86'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '13'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '14'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '15'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '84'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '85'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                                        (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '89'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                    ast.data_prevista_entrega,
                       (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '34'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                       (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '35'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                       (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '36'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                       (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '37'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                       (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '38'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica)



 from e_assist_tecnica ast
 left join  g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral

 where codigo_os_assist_tecnica = {os}

 """
    os_list = []

    for row in estoklus.fetchall(sql):
             service_id = row[1]
             delete_service_order(service_id)
             os_list.append({
    "id": row[1],
    "loja": row[0].upper().strip() if isinstance(row[0], str) else row[0],
    "marca": row[2].upper() if isinstance(row[2], str) else row[2],
    "modelo": row[3].upper() if isinstance(row[3], str) else row[3],
    "referencia_produto": row[4].upper() if isinstance(row[4], str) else row[4],
    "serie": row[5].upper() if isinstance(row[5], str) else row[5],
    "nome": row[6].upper() if isinstance(row[6], str) else row[6],
    "documento": row[7].upper() if isinstance(row[7], str) else row[7],
    "codigo_tipo_pessoa": row[8].upper() if isinstance(row[8], str) else row[8],
    "valor_desconto": float(row[9]),
    "status_os": row[10].upper() if isinstance(row[10], str) else row[10],
    "tipo_reparo": int(row[11]),
    "valor_cliente": float(row[12]),
    "valor_bruto": float(row[13]),
    "serviço": float(row[14]),
    "polimento": float(row[15]),
    "valor_pecas": float(row[16]),
    "data_entrega_produto": row[19].strftime('%Y-%m-%d').lower() if row[19] is not None else '',
    "data_os": row[22].strftime('%Y-%m-%d').lower(),
    "data_analise": row[23].strftime('%Y-%m-%d').lower() if row[23] is not None else '',
    "data_aprovado": row[24].strftime('%Y-%m-%d').lower() if row[24] is not None else '',
    "aprovado": row[25].upper() if isinstance(row[25], str) else row[25],
    "data_inicio_conserto": row[26].strftime('%Y-%m-%d').lower() if row[26] is not None else '',
    "data_termino_conserto": row[27].strftime('%Y-%m-%d').lower() if row[27] is not None else '',
    "status": row[28],
    "calibre": row[29].upper() if isinstance(row[29], str) else row[29],
    "cliente_id": row[30].upper() if isinstance(row[30], str) else row[30],
    "os_loja":row[31].upper() if isinstance(row[31], str) else row[31],
    "tipo_movimento":int(row[32]) if isinstance(row[32], str) else '',
    "complicacao":int(row[33]) if isinstance(row[33], str) else '',
    "defeito":row[34],
    "brand_id":row[35],
    "diagnostico_tecnico":row[36],
    "codigo_estoklus":row[37],
    "repair_bre":row[38],
    "repair_tag":row[39],
    "orcamentista":row[40],
    "calibre_marca":row[41],
    "un_min":row[42],
    "variacao_sm":row[43],
    "consumo_ua":row[44],
    "amplitude":row[45],
    "variacao_sd":row[46],
    "intervencao":row[47],
    "data_prevista_entrega": row[48].strftime('%Y-%m-%d').lower() if row[48] is not None else '',
    "codigo_sap_bv":row[49],
    "codigo_v02_bv_1":row[50],
    "codigo_v02_bv_2":row[51],
    "codigo_v01_bv_1":row[52],
    "codigo_v01_bv_2":row[53] 
})                     
    
    create_service_orders(os_list)
    
    if not os_list:
        return None

    return 'OK'


def load_cx_marcas(os):
     estoklus=Estoklus()
     sql = f"""
select (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '43'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '26'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '20'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '24'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '25'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '28'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '32'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '29'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '31'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '30'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '35'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '37'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                     (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '34'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                            (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '36'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica),
                            (
                SELECT atca.resposta
                FROM e_assist_tecnica_campo_auxiliar atca
                WHERE atca.codigo_campo_auxiliar = '38'
                    AND atca.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica)
                    
                    from e_assist_tecnica ast
                    where codigo_os_assist_tecnica = {os}"""
     return [{
"contrato_richemont":row[0],
"repair_tag": row[1],
"defect_tag": row[2],
"warranty_tag": row[3],
"country_tag": row[4],
"repair_bre": row[5],
"tracking_id_breitling": row[6],
"defect_bre": row[7], 
"ultimo_conserto_bre": row[8],
"pais_bre": row[9],
"codigo_v02_bv":row[10] ,
"codigo_v01_bv_1": row[11],
"codigo_sap_bv_1": row[12],
"codigo_v01_bv_1": row[13],
"codigo_sap_bv_1": row[14]
          
     } for row in estoklus.fetchall(sql)]

def load_dados_entrega(os):
     estoklus = Estoklus()
     sql=f"""select coalesce((select first 1 case when  coalesce(codigo_nfse,0) > 0 then 'true' else  'false' end  from f_lancamento  f
where codigo_ligacao = '{os}'    and (f.descricao_lancamento like 'Có%' or f.descricao_lancamento like 'Assist%')),'false')nf_servico ,
coalesce((select case when codigo_movimento_es is not null then 'true' else 'false' end from e_movimento_es es where es.codigo_os_assist_tecnica =  ast.codigo_os_assist_tecnica
and es.codigo_cfop in ('5916','6916') and (select nf.cancelada from e_registro_nf_controle nf where nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle) = 'N'),'false') nf_devolucao ,
coalesce((select first 1 case when codigo_movimento_es is not null then 'true' else 'false' end from e_movimento_es es where es.codigo_os_assist_tecnica =  ast.codigo_os_assist_tecnica
and es.codigo_cfop in ('6102','5102') and (select nf.cancelada from e_registro_nf_controle nf where nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle) = 'N'),'false') nf_produto,
coalesce((select case when codigo_movimento_es is not null then 'true' else 'false' end from e_movimento_es es where es.codigo_os_assist_tecnica =  ast.codigo_os_assist_tecnica
and es.codigo_cfop in ('1915','2915') and (select nf.cancelada from e_registro_nf_controle nf where nf.codigo_registro_nf_controle = es.codigo_registro_nf_controle) = 'N'),'false') nf_entrada 

from e_assist_tecnica ast

where codigo_os_assist_tecnica = {os}"""
     
     row = estoklus.fetchall(sql)[0]
     return{
          'nf_servico':row[0],
          'nf_devolucao':row[1],
          'nf_produto':row[2],
          'nf_entrada':row[3]
     }















     