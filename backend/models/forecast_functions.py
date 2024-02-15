from models.estoklus import Estoklus1
from models import execute, fetchall, fetchone, databasePool




def get_st_min(marca):
    estoklus = Estoklus1()
    query = f""" select p.referencia_fornecedor,sum(coalesce(st.quantidade_minima,0))

 from e_produto_quantidade_auxiliar st
 join e_produto p on st.codigo_produto = p.codigo_produto

 where p.codigo_marca = '{marca}'
 group by 1
"""
    return {row[0]:{"requested_quantity":int(row[1])} for row in 
    estoklus.fetchall(query)}


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
    return result



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
              and P.codigo_marca = '{marca}'


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
    return retorno


print(pedido_por_os("RADO",'S','RNN'))


def pedidos_em_transito(marca):
    query ="""SELECT 
    p.data->>'brand' as brand,
    pi.data->>'product_code' as product_code, 
    coalesce(SUM((pi.data->>'requested_quantity')::int),0) - coalesce(SUM((invoices->>'received_quantity')::int),0) as invoiced_quantity_total
FROM 
    watchtime.purchase_order_items pi 
LEFT JOIN 
    watchtime.purchase_orders p on pi.purchase_order_id = p.id
LEFT JOIN LATERAL (
    SELECT jsonb_array_elements(pi.data->'invoices') as invoices
    UNION ALL
    SELECT '{}'::jsonb WHERE NOT EXISTS (SELECT 1 FROM jsonb_array_elements(pi.data->'invoices'))
) AS invoices ON TRUE
LEFT JOIN 
    watchtime.purchase_invoices inv ON inv.id = (invoices->>'id')
WHERE 
	p.data->>'brand'='"""+marca+"""' and
    pi.data->>'status' != 'cancelled'
    AND p.data->>'status' in ('approved', 'requested', 'receiving', 'confirmed')
    AND (inv.data->>'status' IS NULL OR inv.data->>'status' != 'cancelled')
GROUP BY 
    p.data->>'brand', pi.data->>'product_code' """
    return {row[1]:{"requested_quantity":row[2]} for row in 
    fetchall(query)}