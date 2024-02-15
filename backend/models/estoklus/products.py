import logging
from models.estoklus import Estoklus,Estoklus1
from models import fetchone
from models.products import create_products,update_product,get_product,get_products_by_ids

def prod_diff():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
    estoklus = Estoklus1()
    
    
    prod_final = list()
    query = """SELECT p.referencia_fornecedor,p.descricao_produto
    ,coalesce((SELECT first 1 preco FROM E_PRODUTO_PRECO epp WHERE epp.codigo_produto = p.codigo_produto AND codigo_tipo_preco = '002'),0),
    coalesce((SELECT ec.descricao_classe FROM E_CLASSE ec WHERE ec.codigo_classe= p.codigo_classe),'NA'),
    p.codigo_marca
    FROM e_produto p 
    WHERE ( inclusao_data >= CAST(CURRENT_DATE AS DATE) or alteracao_data >= CAST(CURRENT_DATE AS DATE))  AND codigo_tipo_produto = 1
    AND referencia_fornecedor <> ''""".replace('\n\t', ' ')

    for row in estoklus.fetchall(query):
        
        query2 = "select id from watchtime.products where id = %s"
        rowc = fetchone(query2, (row[0],))
        if not rowc:
            prod_final.append({"id": row[0], "code": row[0], "name": row[1], "cost":float(row[2]),"category": row[3],"brand": row[4].strip()}) 

    if not prod_final:
        return "sem itens para criar"

    create_products(prod_final)
    return "Produtos importados com sucesso"


def description_update():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
    estoklus = Estoklus1()
    query = """SELECT p.referencia_fornecedor, p.descricao_produto,
                      coalesce((SELECT ec.descricao_classe FROM E_CLASSE ec WHERE ec.codigo_classe= p.codigo_classe),'NA'),
                      p.codigo_marca
               FROM e_produto p 
               WHERE alteracao_data >= CAST(CURRENT_DATE AS DATE) AND codigo_tipo_produto = 1
               AND referencia_fornecedor <> ''"""
    produtos_referencias = []
    for row in estoklus.fetchall(query):
        produtos_referencias.append((str(row[0]),row[1],row[2],row[3].strip()))  # append whole row

    # Get all products by ids
    product_refs = {ref for ref,_,_,_ in produtos_referencias}
    produtos = get_products_by_ids(product_refs)

    # Check if name, class or brand has changed and update
    atualiza = []
    for ref, descricao, classe, marca in produtos_referencias:
        if ref in produtos:
            produto = produtos[ref]
            if produto["name"] != descricao or produto["brand"] != marca or produto["category"] != classe:
                produto["name"] = descricao
                produto["brand"] = marca
                produto["category"] = classe
                atualiza.append(produto)

    # Update products
    for produto in atualiza:
        update_product(produto)
            
    if len(atualiza) == 0:
        return 0

    return atualiza#len(atualiza)


def price_update():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
    estoklus = Estoklus1()
    query = """ SELECT(SELECT referencia_fornecedor FROM e_produto p WHERE p.codigo_produto = pp.codigo_produto),pp.preco 
               FROM e_produto_preco pp
               WHERE codigo_tipo_preco = '002' AND preco > 0 and
               (pp.alteracao_data >= CAST(CURRENT_DATE - 4 AS DATE) OR 
                pp.inclusao_data >= CAST(CURRENT_DATE - 4 AS DATE))"""
    precos = []
    for row in estoklus.fetchall(query):
        precos.append((row[0], float(row[1])))

    # Get all products by ids
    product_ids = {id for id, _ in precos}
    produtos = get_products_by_ids(product_ids)

    # Check if cost has changed and update
    atualiza = []
    for id, preco in precos:
        if id in produtos and produtos[id]["cost"] != preco:
            produtos[id]["cost"] = preco
            atualiza.append(produtos[id])

    # Update products
    for produto in atualiza:
        update_product(produto)
            
    return len(atualiza)