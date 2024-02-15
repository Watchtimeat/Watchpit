import json
from click import pause
from markupsafe import _MarkupEscapeHelper
import numpy as np
import pandas as pd
from io import BytesIO
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
from models.estoklus import Estoklus1
from models.purchase_orders import create_purchase_order
from models.resources import create_resource
import tempfile,pytz
from datetime import datetime
from models import forecast_functions

def fixed_mean(series, i_std):
        mean = series.mean()
        std = series.std()
        return series[(series >= mean - i_std * std) & (series <= mean + i_std * std)].mean()

def p_value(series):
        return adfuller(series)[1]

def send_excel_to_resource(file_dir):
    # Gerar o arquivo Excel

    # Ler o arquivo Excel gerado
    filename = file_dir
    with open(filename, "rb") as f:
        wb_bytes = BytesIO(f.read())

    # Criar o objeto resource com o arquivo Excel como stream
    resource = {
        "content_type": "application/vnd.ms-excel",
        "type": "excel"
    }
    
    return create_resource(resource, stream=wb_bytes)   
# Configurações da conexão com o banco de dados


def gera_algoritimo(marca,first_period,last_period,month_forecast,owner):
    estoklus = Estoklus1()
    primeiro_periodo = first_period
    ultimo_periodo =last_period 

    # SQL Query
    sql_query = f"""select ast.codigo_os_assist_tecnica,
    p.codigo_marca,
    p.referencia_fornecedor,
    p.descricao_produto,
    orc.qtde,
    ast.data_aprovado,
    p.codigo_classe categoria, 
    coalesce((select first 1 (preco) from e_produto_preco pp where pp.codigo_produto = p.codigo_produto and codigo_tipo_preco = '002' order by inclusao_data desc),0) preco,
    0 st_min,
    coalesce((select sum(quantidade_atual) from e_produto_quantidade_atual est where est.codigo_produto = p.codigo_produto and quantidade_atual >=0),0)ST
    ,0 OS_PENDENTES


    from e_assist_tecnica ast
    left join e_assist_tecnica_pecas_servicos orc on ast.codigo_os_assist_tecnica= orc.codigo_os_assist_tecnica
    left join e_produto p on orc.codigo_produto = p.codigo_produto
    left join e_grupo_os_assist_tecnica gr on ast.grupo_os_assist_tecnica = gr.codigo_grupo_os

    where ast.data_aprovado >= '01/01/2022'
    and p.codigo_produto <> '95' and p.codigo_produto <> '0000801' and orc.peca_ou_servico <> 'S'

    and p.codigo_marca = '{marca}'

    union all

    select

     vi.codigo_movimento_item,
     p.codigo_marca,
     p.referencia_fornecedor,
     p.descricao_produto,
     vi.quantidade,
     vi.inclusao_data,
     p.codigo_classe categoria,
      coalesce((select first 1 (preco) from e_produto_preco pp where pp.codigo_produto = p.codigo_produto and codigo_tipo_preco = '002' order by inclusao_data desc),0) preco,
    0 st_min,
    coalesce((select sum(quantidade_atual) from e_produto_quantidade_atual est where est.codigo_produto = p.codigo_produto and quantidade_atual >=0),0)ST
    ,0 OS_PENDENTES

    from e_movimento_vendas_item vi
    join e_produto p on p.codigo_produto = vi.codigo_produto  where vi.inclusao_data >='01/01/2022' and p.codigo_tipo_produto = 1
    and p.codigo_marca = '{marca}'""".replace('\n\t', ' ')

    lista = estoklus.fetchall(sql_query)
    # Estabelece a conexão com o banco de dados Firebird

    data = pd.DataFrame(lista, columns = [
        'service_id',
        'product_brand',
        'product_id',
        'product_description',
        'quantity',
        'service_date',
        'product_category',
        'product_cost',
        'min_stock',
        'stock',
        'dependent_service'
    ])

    # Renomeia as colunas conforme necessário

    np.seterr('ignore')

    products_pending = forecast_functions.pedido_por_os(marca,'S','')
    products_requested = forecast_functions.pedidos_em_transito(marca)
    products_stmin = forecast_functions.get_st_min(marca)

    period = 'm'
    data['service_id'] = data['service_id'].apply(str)
    data['service_date'] = pd.to_datetime(data['service_date'], format='%d/%m/%Y')
    data['period'] = data['service_date'].dt.to_period(period)
    data['product_cost'] = pd.to_numeric(data['product_cost'])
    data = data[(data['period'] >= first_period) & (data['period'] <= last_period)]
    data


    stock = data[['product_id','product_brand','stock']]
    stock = stock.groupby('product_id').agg({'stock':'last', 'stock':'last', 'stock':'last'}).fillna(0)
    stock.reset_index(inplace=True)
    stock['stock'] = stock['stock'].astype(int)
    stock


    first_period = data['period'].min()
    last_period = data['period'].max()
    periods = pd.DataFrame(pd.period_range(first_period, last_period), columns=['period'])
    group = data.groupby('product_id')
    products = pd.DataFrame()
    products['brand'] = group['product_brand'].last().str.lower()
    products['category'] = group['product_category'].last().str.lower()
    products['description'] = group['product_description'].last()
    products['last_cost'] = group['product_cost'].last()
    products['first_demand'] = group['period'].min()
    products['last_demand'] = group['period'].max()
    products['periods'] = (products['last_demand'] - products['first_demand']).apply(lambda x: x.n) + 1
    products['quantity_sum'] = group['quantity'].sum().astype(int)
    products['quantity_monthly_mean'] = products['quantity_sum'] / ((last_period - first_period).n + 1)
    products.reset_index(inplace=True)
    products.sort_values(by='quantity_sum', ascending=False, inplace=True)
    products = products.merge(stock, how='left')
    products.fillna(0, inplace=True)
    products.set_index('product_id', inplace=True)
    products


    orders = data[['service_id','product_id','quantity','service_date','product_cost']].copy()
    orders.columns=['id','productId','quantity','date','product_cost']
    orders['date'] = orders['date'].astype(str)
    orders


    cartesian = pd.merge(data['product_id'].drop_duplicates(), periods, how='cross')
    demands = data.groupby(['product_id','period'])['quantity'].sum().reset_index()
    demands = cartesian.merge(demands, how='left').fillna(0)
    demands['quantity'] = demands['quantity'].astype(float)

    items_order = list()
    count = 0
    forecasts = pd.DataFrame()
    for product_id in products.index:
        product = demands[demands['product_id'] == product_id][['period','quantity']].set_index('period')
        product[product.cummax().eq(0)] = np.nan
        product.dropna(inplace=True)
      ##  product.loc[product['quantity'] == 0, 'quantity'] = 1  para deixar o algoritimo otimista (estoque alto) - mul
        if len(product) > 1:
            fit = ExponentialSmoothing(
                product,
                trend = 'add'
            ).fit()
            forecast = pd.DataFrame(fit.forecast(month_forecast)+1).astype(int).T
            forecast.index = [product_id]
            forecast.index.name = 'product_id'
            # Somar as quantidades de todos os meses anteriores ao último
       #     if month_forecast > 1:  # Checar se há mais de um mês na previsão
       #         sum_of_previous_months = forecast.iloc[0, :-1].sum()  # Somar todas as colunas exceto a última
       #     else:
       #         sum_of_previous_months = 0  # Se só tem um mês, não tem meses anteriores
        #
        #    forecast['sum_of_previous_months'] = sum_of_previous_months
            if product_id in products_pending:
                pending_service_value = products_pending[product_id]['requested_quantity']
            else:
                pending_service_value = 0  
            forecast['pending_service'] = pending_service_value
            if product_id in products_requested:
                requested_value = products_requested[product_id]['requested_quantity']
            else:
                requested_value = 0  
            if product_id in products_stmin:
                 stmin_value = products_stmin[product_id]['requested_quantity']
            else:
                stmin_value = 0  
            forecast["stmin"] = stmin_value
            forecast['pending_service'] = pending_service_value
            forecast['requested_quantity'] = requested_value
            last_month_quantity = forecast.iloc[0, -5]  # Pegar a quantidade do último mês (5 casas à esquerda)
            forecast['last_month_quantity'] = last_month_quantity
            current_stock = products.loc[product_id, 'stock']
            month_mean = products.loc[product_id, 'quantity_monthly_mean'] 
            ##---CÁLCULO ALGORITIMO V2--- 
        #SALDO À COMPRAR = [(MES PROJETADO FINAL + ST SEG)] - [(ST - OS PENDENTES) - (SOMA MESES PROJETADOS - SOMA PEDIDOS EM ABERTO)]
            if month_mean >= 0.6:
                forecast['final_value'] = (last_month_quantity + stmin_value) - ((current_stock + requested_value )-pending_service_value)
            else:
                 forecast['final_value'] = stmin_value - ((current_stock + requested_value )-pending_service_value)
            forecasts = pd.concat([forecasts, forecast])

        if count % 100 == 0:
            print(count)
        count = count + 1


    recommendation = pd.merge(products.reset_index(), forecasts.reset_index(), how='left')

    # Criar um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Salvando o DataFrame no arquivo temporário
        recommendation.to_excel(tmp.name, index=False)

        # Enviar o arquivo Excel para o recurso e obter o ID do recurso
        resource_id = send_excel_to_resource(tmp.name)

    for index, row in recommendation.iterrows():
         if row['final_value'] > 0:
            items_order.append({"product_code":row["product_id"],
                                "product_cost":row["last_cost"],
                                "product_id":row["product_id"],
                                "product_name":row["description"],
                                "requested_quantity":row["final_value"],
                                "status":"active",
                                "total_cost":row["last_cost"] * row["final_value"]})
              

    # Criar a ordem de compra
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    created = datetime.now(fuso_horario).isoformat()
    order_info = {
        "brand": marca.upper(),
        "status": "draft",
        "mode": "Algoritimo",
        "created": created,
        "owner": owner,
        "forecast_file": resource_id["id"],
        "items": items_order,
        "first_period": primeiro_periodo,
        "last_period": ultimo_periodo
    }
    print(order_info)
    # Criar a ordem de compra
    result = create_purchase_order(order_info)
            

    return {"message": "Pedido " +marca+ " criado com sucesso"}














