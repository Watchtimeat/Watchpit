import pandas as pd
from models.estoklus import Estoklus
import json
import logging,ast


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])



def inserir_itens_pedido(items,pedido,loja,valordeclarado,frete,valorchf,aliquota):

    pedido = str(pedido[0])
    estoklus = Estoklus()
    cambio = (valordeclarado + frete) / valorchf
    icms_calc = 0.83
    if loja == 'PR':
        icms_calc = 0.81
    if loja == 'RJ':
        icms_calc = 0.82
    values_list_1 = []
    values_list_2 = []
    for item in items:
        sCodigoTamanho =''
        sCodigoCor =''
        sCodigoUnidade = 'UN'
        nBaseII =  item["fob"] * cambio
        npercentii = 0.6
        nValorII =  npercentii * nBaseII
        nAliquotaICMS =  aliquota
        nPrecoCompraBruto = nBaseII
        nBaseICMS = ((nPrecoCompraBruto + nValorII) * item["qtd"] ) / icms_calc
        nValorICMS =   nBaseICMS * ( nAliquotaICMS /100)
        dDataEmissao   = 'now'
        nValorFrete   = 0
        nValorDesconto   = 0
        nValorSeguro  = 0
        nValorOutrasDespesas    = 0
        sCodigoCFOP  = '3102'
        sSeqItem   = 1
        nValorAFRMM   = 0
        sCodigoCST       = '0'
        nValorAduaneira   = 0
        nValorIPI  = 0
        nAliquotaIPI    = 0
        nBaseIPI = 0
        nBaseICMSst  = 0
        nValorICMSst   = 0
        nBasePIS   = 0
        nAliquotaPIS   = 0
        nValorPIS   = 0
        nBaseCOFINS   = 0
        nAliquotaCOFINS    = 0
        nValorCOFINS   = 0
        nValorAcrescimoTributo = 0
        nBaseSISCOMEX = 0
        nValorSISCOMEX = 0
        nAliquotaSISCOMEX = 0
        nPrecoTotalFinal = 0
        sNumAdicao = '001'


        codigo_pedido_item = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_PED_CP_ITEM,1) from RDB$DATABASE")       
        codigo_pedido_item_imp = estoklus.fetchone("select GEN_ID(GEN_E_CODIGO_PED_CP_ITEM_IMP,1) from RDB$DATABASE")
        nAliquotaII = 60
      
        nPrecoTotalFinal = nPrecoCompraBruto * item["qtd"]
        insert_values_1 = (
        codigo_pedido_item,
        pedido,
        item["codigo_produto"],
        sCodigoTamanho,
        sCodigoCor,
        item["obs"],
        nPrecoCompraBruto,
        nPrecoCompraBruto,
        nPrecoCompraBruto,
        nPrecoCompraBruto,
        dDataEmissao,
        item["qtd"],
        sCodigoUnidade,
        'now',
        'Cockpit'
        )

        insert_values_2 = (
        codigo_pedido_item_imp,
        codigo_pedido_item,
        nPrecoCompraBruto,
        nValorAcrescimoTributo,
        nValorFrete,
        nValorDesconto,
        item["qtd"],
        sCodigoCFOP,
        item["ncm"],
        sCodigoCST,
        sNumAdicao,
        sSeqItem,
        nBaseII,
        nAliquotaII,
        nValorII,
        nBaseIPI,
        nAliquotaIPI,
        nValorIPI,
        nBaseICMS,
        nAliquotaICMS,
        nValorICMS,
        nBaseICMSst,
        nValorICMSst,
        nBasePIS,
        nAliquotaPIS,
        nValorPIS,
        nBaseCOFINS,
        nAliquotaCOFINS,
        nValorCOFINS,
        nBaseSISCOMEX,
        nAliquotaSISCOMEX,
        nValorSISCOMEX,
        nValorSeguro,
        nValorOutrasDespesas,
        nValorFrete,
        nValorAcrescimoTributo,
        nPrecoCompraBruto,
        nPrecoCompraBruto,
        nPrecoTotalFinal,
        nValorAFRMM,
        nValorAduaneira,
        'N',
        'now',
        'Cockpit'
        )

        
        values_list_1.append(insert_values_1)
        values_list_2.append(insert_values_2)
    table_name_1 = "E_PEDIDO_COMPRA_ITEM"
    columns_1 = [
    "codigo_pedido_compra_item",
    "codigo_pedido_compra",
    "codigo_produto",
    "codigo_tamanho",
    "codigo_cor",
    "observacoes",
    "preco_compra_bruto",
    "preco_compra",
    "preco_unitario",
    "preco_compra_i",
    "data_previsao",
    "quantidade_prevista",
    "codigo_unidade",
    "inclusao_data",
    "inclusao_por"
    ]

    table_name_2 = "E_PEDIDO_COMPRA_ITEM_IMP"
    columns_2 = [
    "codigo_pedido_compra_item_imp",
    "codigo_pedido_compra_item",
    "preco_unitario",
    "valor_acrescimo_tributo",
    "valor_frete",
    "valor_desconto",
    "quantidade",
    "codigo_cfop",
    "ncm",
    "cst",
    "num_adicao",
    "seq_item",
    "base_ii",
    "aliquota_ii",
    "valor_ii",
    "base_ipi",
    "aliquota_ipi",
    "valor_ipi",
    "base_icms",
    "aliquota_icms",
    "valor_icms",
    "base_icms_st",
    "valor_icms_st",
    "base_pis",
    "aliquota_pis",
    "valor_pis",
    "base_cofins",
    "aliquota_cofins",
    "valor_cofins",
    "base_siscomex",
    "aliquota_siscomex",
    "valor_siscomex",
    "valor_seguro",
    "valor_outras_despesas",
    "valor_frete_fob",
    "valor_acrescimo_tributo_fob",
    "preco_unitario_fob",
    "preco_unitario_final",
    "preco_total_final",
    "valor_taxa_afrmm",
    "valor_desp_aduaneira",
    "Importado_Do_XML",
    "inclusao_data",
    "inclusao_por"
    ]

   
# Chamando a função 'insert' para inserir os valores na tabela E_PEDIDO_COMPRA_ITEM
    estoklus.insert(table_name_1, columns_1, values_list_1)

# Chamando a função 'insert' para inserir os valores na tabela E_PEDIDO_COMPRA_ITEM_IMP
    estoklus.insert(table_name_2, columns_2, values_list_2)

    return True




def create_order_estoklus(data, file):
    if isinstance(data, str):
        data = json.loads(data)

    df = pd.read_excel(file, dtype={'Reference': str})
    df = df.fillna("")
    erros = []
    items = []
    estoklus = Estoklus()
    required_fields = ['fornecedor', 'ref', 'comprador', 'loja', 'dir', 'desembaracoUF', 'cfop', 'desembaracoLocal', 'datadesembaraco', 'dataDir','aliquota','valorDeclarado','valorFrete','valorItens']
    validation = []

    for field in required_fields:
        if field not in data:
            validation.append(field)

    if validation:
        return {"error":'Não foram preenchidos todos os campos - ' + ', '.join(validation)}
    
    if "Reference" in df.columns.values and "Invoice Qty" in df.columns.values and "Unit Price" in df.columns.values and "Obs" in df.columns.values:            

        for idx, row in df.iterrows():
            ref = row['Reference']
            # Busca as informações dos produtos
            query = "select codigo_produto, codigo_classificacao_fiscal, referencia_fornecedor from e_produto where referencia_fornecedor = ? and ativo = 'S'"
            rows = estoklus.fetchall_with_params(query, [ref])
            logging.info(rows)
            # Cria um dicionário com os resultados
            results_dict = {row[2]: (row[0], row[1]) for row in rows}
            
            
            if ref not in results_dict:
                # Produto inexistente
                erros.append({"id": ref, "problem": "Inexistente"})
            else:
                codigo_produto, codigo_classificacao_fiscal = results_dict[ref]

                # Verifica se o NCM existe
                if not codigo_classificacao_fiscal:
                    erros.append({"id": ref, "problem": "NCM Inexistente"})
                else:
                    # Adiciona o item à lista
                    items.append({"codigo_produto":str(codigo_produto),"ncm":str(codigo_classificacao_fiscal),"ref": str(row["Reference"]), "qtd": int(row["Invoice Qty"]), "obs": row["Obs"], "fob": float(row["Unit Price"])})
    else:
        return {"error": "Arquivo fora do layout (Reference,Invoice Qty, Unit Price, Obs)"}
    
    if erros:
        return {"error": erros}  

    if not items:
        return {"error": "Arquivo vazio"}
    
 

    pedido = estoklus.exec_stored_proc('wt_criar_pc', data['fornecedor'], data['ref'], data['comprador'], data['loja'], data['dir'], data['desembaracoUF'].upper(), data['cfop'], data['desembaracoLocal'].upper(), data['datadesembaraco'], data['dataDir'])
    
    if not pedido:
        return {"error":"Falha ao criar o pedido"}
    
     
    insercao_items = inserir_itens_pedido(items,pedido,data['loja'],data['valorDeclarado'],data['valorFrete'],data['valorItens'],data['aliquota'])
    atualiza_preco(items)
    if insercao_items:
        return {"success": "Pedido " + str(pedido[0]) + " criado no Estoklus."}
    else:
        return {"error": "Falha ao inserir o pedido"}
    

def atualiza_preco(items):

    
    for item in items:
        cod = item["codigo_produto"]
        val = item["fob"]
        estoklus = Estoklus()
        query = f"select codigo_produto from e_produto_preco where codigo_produto ='{cod}' and codigo_tipo_preco = '002'"
        existepreco = estoklus.fetchone(query)
        columns = []
        values = []
        if not existepreco:
            columns = ["CODIGO_PRODUTO","CODIGO_TIPO_PRECO","PRECO","MODULO_DE_REAJUSTE","INCLUSAO_DATA"]
            values = [(item["codigo_produto"], '002', val, 'Inserção -  Cockpit', 'now')]
            
            estoklus.insert("e_produto_preco", columns, values)

       
        else:
            table_name = 'e_produto_preco'
            column_names = ['preco', 'MODULO_DE_REAJUSTE','inclusao_data']
            values = (val, 'Update preco - Cockpit','now')
            conditions = [
                "codigo_tipo_preco = '002'",
                f"codigo_produto = '{cod}'"
            ]
    # Chame a função update com os parâmetros
            estoklus.update(table_name, column_names, values, conditions, sql_echo=True)
    