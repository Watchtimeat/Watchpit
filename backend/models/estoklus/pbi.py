import firebirdsql as fb
from datetime import datetime
from decimal import Decimal
from models.estoklus import Estoklus


def get_repaired_orders():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_termino_conserto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    from e_assist_tecnica ast
    where 
extract (year from ast.data_termino_conserto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    querysp = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'SP',ast.data_termino_conserto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    from e_assist_tecnica ast
    where 
extract (year from ast.data_termino_conserto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    queryrj = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'RJ',ast.data_termino_conserto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    from e_assist_tecnica ast
    where 
extract (year from ast.data_termino_conserto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    querycwb = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'PR',ast.data_termino_conserto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    from e_assist_tecnica ast
    where 
extract (year from ast.data_termino_conserto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})

    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()


    return(consulta)


def get_openned_orders():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_os
from e_assist_tecnica  ast
where 
extract (year from ast.data_os) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_os) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    query2 = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_os
from e_assist_tecnica  ast
where 
extract (year from ast.data_os) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_os) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    cur.execute(query2)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_OS": row[3].strftime('%m/%d/%Y')})

    con.close()
    return(consulta)

def get_estimated_orders():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_analise
from e_assist_tecnica  ast
where 
extract (year from ast.data_analise) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_analise) =    extract (month from (select cast('Now' as date) from rdb$database))""".replace('\n\t', ' ')

    query2 = "select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_termino_conserto,coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_     WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0.0) from e_assist_tecnica ast where extract (year from ast.data_termino_conserto) =  extract (year from (select cast('Now' as date) from rdb$database)) and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))'"

    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_ANALISE": row[3].strftime('%m/%d/%Y')})

    con.close()
    return(consulta)

def get_approved_orders():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select 
data_aprovado
,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0)


, cast ( a.loja_os as varchar(20) ) codigo_loja
, cast(a.grupo_os_assist_tecnica as varchar(200)),
a.codigo_os_assist_tecnica

from e_assist_tecnica a

left join g_cadastro_geral c on c.codigo_cadastro_geral = a.codigo_cliente
left join e_funcionario f on f.codigo_usuario = a.fase2_alteracao_por

where a.aprovado = 'S' and
    extract (year from a.data_aprovado) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from a.data_aprovado) =    extract (month from (select cast('Now' as date) from rdb$database)) 



 

    
    
    union


select m.data_venda,

cast (coalesce((select sum(mi.preco_digitado) from e_movimento_vendas_item mi 

 where mi.codigo_movimento_capa = m.codigo_movimento_capa and
mi.codigo_produto not in('95','70','0101679','0184225','5135014')),0.00)as double precision) 
, cast ( m.codigo_loja as varchar(20) ) codigo_loja
,cast('SATE' as varchar(200)),codigo_movimento_capa
from e_movimento_vendas_capa m

left join g_cadastro_geral c on c.codigo_cadastro_geral = m.codigo_cadastro_geral
left join e_funcionario f on f.codigo_funcionario =  m.codigo_vendedor

where (select sum(mi.preco_digitado) from e_movimento_vendas_item mi 
             where mi.codigo_movimento_capa = m.codigo_movimento_capa and 
                   mi.codigo_produto not in('95','70','0101679','0184225','5135014')) is not null



  AND extract (year from m.data_venda) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from m.data_venda) =    extract (month from (select cast('Now' as date) from rdb$database))  
    
""".replace('\n\t', ' ')

    querysp = """select 
data_aprovado
,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0)


, cast ( 'SP' as varchar(20) ) codigo_loja
, cast(( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as varchar(200))

from e_assist_tecnica a

left join g_cadastro_geral c on c.codigo_cadastro_geral = a.codigo_cliente
left join e_funcionario f on f.codigo_usuario = a.fase2_alteracao_por

where a.aprovado = 'S' and
    extract (year from a.data_aprovado) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from a.data_aprovado) =    extract (month from (select cast('Now' as date) from rdb$database)) 



 
""".replace('\n\t', ' ')
    queryrj ="""select 
data_aprovado
,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0)


, cast ( 'RJ' as varchar(20) ) codigo_loja
, cast(( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as varchar(200))

from e_assist_tecnica a

left join g_cadastro_geral c on c.codigo_cadastro_geral = a.codigo_cliente
left join e_funcionario f on f.codigo_usuario = a.fase2_alteracao_por

where a.aprovado = 'S' and
    extract (year from a.data_aprovado) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from a.data_aprovado) =    extract (month from (select cast('Now' as date) from rdb$database)) 



 
""".replace('\n\t', ' ')
    querycwb = """select 
data_aprovado
,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0)


, cast ( 'PR' as varchar(20) ) codigo_loja
, cast(( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as varchar(200))

from e_assist_tecnica a

left join g_cadastro_geral c on c.codigo_cadastro_geral = a.codigo_cliente
left join e_funcionario f on f.codigo_usuario = a.fase2_alteracao_por

where a.aprovado = 'S' and
    extract (year from a.data_aprovado) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from a.data_aprovado) =    extract (month from (select cast('Now' as date) from rdb$database)) 



 
""".replace('\n\t', ' ')
    
    seq = 0
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"MARCA":row[3],"LOJA":row[2],"DATA_APROVADO": row[0].strftime('%m/%d/%Y'),"VALOR": float(row[1]),"row":seq})
        seq +=1
    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
        consulta.append({"MARCA":row[3],"LOJA":row[2],"DATA_APROVADO": row[0].strftime('%m/%d/%Y'),"VALOR": float(row[1]),"row":seq})
        seq +=1
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
        consulta.append({"MARCA":row[3],"LOJA":row[2],"DATA_APROVADO": row[0].strftime('%m/%d/%Y'),"VALOR": float(row[1]),"row":seq})
        seq +=1
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
        consulta.append({"MARCA":row[3],"LOJA":row[2],"DATA_APROVADO": row[0].strftime('%m/%d/%Y'),"VALOR": float(row[1]),"row":seq})
        seq +=1
    con.close()
    return(consulta)

def get_delivered_orders():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_entrega_produto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    ,coalesce((select sum(valor) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and  extract (month from pg.inclusao_data) = extract (month from (select cast('Now' as date) from rdb$database)) ),0)
from e_assist_tecnica  ast
where 
extract (year from ast.data_entrega_produto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_entrega_produto) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'""".replace('\n\t', ' ')

    querycwb = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'PR',ast.data_entrega_produto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    ,coalesce((select sum(valor) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and  extract (month from pg.inclusao_data) = extract (month from (select cast('Now' as date) from rdb$database)) ),0)
from e_assist_tecnica  ast
where 
extract (year from ast.data_entrega_produto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_entrega_produto) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'""".replace('\n\t', ' ')
    
    querysp = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'SP',ast.data_entrega_produto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    ,coalesce((select sum(valor) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and  extract (month from pg.inclusao_data) = extract (month from (select cast('Now' as date) from rdb$database)) ),0)
from e_assist_tecnica  ast
where 
extract (year from ast.data_entrega_produto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_entrega_produto) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'""".replace('\n\t', ' ')
    
    queryrj = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'RJ',ast.data_entrega_produto,coalesce((Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0)
    ,coalesce((select sum(valor) from e_assist_tecnica_pagto pg where pg.codigo_os_assist_tecnica = ast.codigo_os_assist_tecnica and  extract (month from pg.inclusao_data) = extract (month from (select cast('Now' as date) from rdb$database)) ),0)
from e_assist_tecnica  ast
where 
extract (year from ast.data_entrega_produto) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_entrega_produto) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'""".replace('\n\t', ' ')

    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_ENTREGA_PRODUTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4]),"VALOR_FINAN": float(row[5])})

    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_ENTREGA_PRODUTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4]),"VALOR_FINAN": float(row[5])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_ENTREGA_PRODUTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4]),"VALOR_FINAN": float(row[5])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_ENTREGA_PRODUTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4]),"VALOR_FINAN": float(row[5])})
    con.close()

    return(consulta)

def get_awaiting_estimate():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os, cast('now' as date) - cast(data_os as date)
from e_assist_tecnica  ast
where 
ast.data_analise is null and fase_atual not in (7,8,3)""".replace('\n\t', ' ')

    query2 = "select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_termino_conserto,coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_     WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0.0) from e_assist_tecnica ast where extract (year from ast.data_termino_conserto) =  extract (year from (select cast('Now' as date) from rdb$database)) and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))'"

    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO": row[3]})

    con.close()
    return(consulta)


def get_awaiting_approval():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,a.loja_os, cast('now' as date) - cast(data_analise as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is null  and a.data_analise is not null and  fase_atual not in (7,8,3)""".replace('\n\t', ' ')

    query2 = "select codigo_os_assist_tecnica,grupo_os_assist_tecnica,ast.loja_os,ast.data_termino_conserto,coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_     WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - ast.VALOR_DESCONTO,0.0) from e_assist_tecnica ast where extract (year from ast.data_termino_conserto) =  extract (year from (select cast('Now' as date) from rdb$database)) and   extract (month from ast.data_termino_conserto) =    extract (month from (select cast('Now' as date) from rdb$database))'"

    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":row[4]})
    

    con.close()
    return(consulta)


def get_awaiting_start_repair():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,a.loja_os, cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is null  and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')


    querycwb = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'PR', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is null  and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    
    querysp = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'SP', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is null  and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    
    queryrj = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'RJ', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is null  and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})

    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()
    return(consulta)



def get_awaiting_finish():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,a.loja_os, cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is NOT null and a.data_TERMINO_CONSERTO is null and  fase_atual not in (7,8,3)""".replace('\n\t', ' ')

    querycwb = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'PR', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is NOT null and a.data_TERMINO_CONSERTO is null and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    
    querysp = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'SP', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is NOT null and a.data_TERMINO_CONSERTO is null and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    
    queryrj = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'RJ', cast('now' as date) - cast(data_aprovado as date) ,coalesce(
cast (

case 

when             a.codigo_cliente IN('210120','209184','208212','209310','208901','S059873','208383')
          then
             ( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
                    WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                         atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA )


when a.tipo_reparo in (1,2,5,7) and (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) is not null
 then
          cast( (Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR = '43' AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ) as double precision) + coalesce(((Select
             Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
            from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
            WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' )- a.VALOR_DESCONTO ),0)




     when a.codigo_cliente = 'S042591' and a.valor_desconto = 0
          then
         (Select
     Sum(Case when atps_.peca_ou_servico = 'P' then VALOR_UNITARIO *atps_.QTDE * 0.77 else VALOR_UNITARIO * atps_.QTDE * 0.70 end)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' ) - a.VALOR_DESCONTO
else

(Select
     Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and codigo_produto not in ('0101679','0184225')) - a.VALOR_DESCONTO end as double precision),0.0) VALOR

from e_assist_tecnica  a
where 
a.data_aprovado is not null and a.aprovado = 'S' and a.data_analise is not null and a.data_inicio_conserto is NOT null and a.data_TERMINO_CONSERTO is null and  fase_atual not in (7,8,3)
""".replace('\n\t', ' ')
    
    
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})

    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
          consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR":float(row[4])})
    con.close()


    return(consulta)



def get_awaiting_delivery():
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select codigo_os_assist_tecnica,grupo_os_assist_tecnica,a.loja_os, cast('now' as date) - cast(data_TERMINO_CONSERTO as date) , coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
          WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica and atps_.garantia = 'N')  ) - a.VALOR_DESCONTO,0) 
- coalesce((select sum(atf.valor) from e_assist_tecnica_pagto atf 
          where a.codigo_os_assist_tecnica = atf.codigo_os_assist_tecnica),0) valor_faltando

from e_assist_tecnica  a
where 
fase_atual =(6)

""".replace('\n\t', ' ')

    querycwb = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'PR', cast('now' as date) - cast(data_TERMINO_CONSERTO as date) , coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
          WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica and atps_.garantia = 'N')  ) - a.VALOR_DESCONTO,0) 
- coalesce((select sum(atf.valor) from e_assist_tecnica_pagto atf 
          where a.codigo_os_assist_tecnica = atf.codigo_os_assist_tecnica),0) valor_faltando

from e_assist_tecnica  a
where 
fase_atual =(6)

""".replace('\n\t', ' ')
    querysp = """select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'SP', cast('now' as date) - cast(data_TERMINO_CONSERTO as date) , coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
          WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica and atps_.garantia = 'N')  ) - a.VALOR_DESCONTO,0) 
- coalesce((select sum(atf.valor) from e_assist_tecnica_pagto atf 
          where a.codigo_os_assist_tecnica = atf.codigo_os_assist_tecnica),0) valor_faltando

from e_assist_tecnica  a
where 
fase_atual =(6)

""".replace('\n\t', ' ')
    queryrj ="""select codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = a.CODIGO_OS_ASSIST_TECNICA ),'RJ', cast('now' as date) - cast(data_TERMINO_CONSERTO as date) , coalesce((Select Sum(atps_.VALOR_UNITARIO*atps_.QTDE) from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
          WHERE (a.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica and atps_.garantia = 'N')  ) - a.VALOR_DESCONTO,0) 
- coalesce((select sum(atf.valor) from e_assist_tecnica_pagto atf 
          where a.codigo_os_assist_tecnica = atf.codigo_os_assist_tecnica),0) valor_faltando

from e_assist_tecnica  a
where 
fase_atual =(6)

""".replace('\n\t', ' ')
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
         consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR_restante":float(row[4])})

    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
         consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR_restante":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
         consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR_restante":float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
         consulta.append({"OS":row[0],"MARCA":row[1],"LOJA":row[2],"TEMPO":row[3],"VALOR_restante":float(row[4])})
    con.close()


    return(consulta)

def get_invoiced():

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select ast.codigo_os_assist_tecnica,grupo_os_assist_tecnica,LOJA_OS,pg.inclusao_data,coalesce(pg.valor,0)valor
from e_assist_tecnica  ast
left join e_assist_tecnica_pagto pg on ast.codigo_os_assist_tecnica = pg.codigo_os_assist_tecnica
where 
extract (year from pg.inclusao_data) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from pg.inclusao_data) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'
""".replace('\n\t', ' ')

    querycwb = """select ast.codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'PR',pg.inclusao_data,coalesce(pg.valor,0)valor
from e_assist_tecnica  ast
left join e_assist_tecnica_pagto pg on ast.codigo_os_assist_tecnica = pg.codigo_os_assist_tecnica
where 
extract (year from pg.inclusao_data) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from pg.inclusao_data) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'
""".replace('\n\t', ' ')
    
    querysp = """select ast.codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'SP',pg.inclusao_data,coalesce(pg.valor,0)valor
from e_assist_tecnica  ast
left join e_assist_tecnica_pagto pg on ast.codigo_os_assist_tecnica = pg.codigo_os_assist_tecnica
where 
extract (year from pg.inclusao_data) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from pg.inclusao_data) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'
""".replace('\n\t', ' ')
    
    queryrj = """select ast.codigo_os_assist_tecnica,( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=1 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ),'RJ',pg.inclusao_data,coalesce(pg.valor,0)valor
from e_assist_tecnica  ast
left join e_assist_tecnica_pagto pg on ast.codigo_os_assist_tecnica = pg.codigo_os_assist_tecnica
where 
extract (year from pg.inclusao_data) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from pg.inclusao_data) =    extract (month from (select cast('Now' as date) from rdb$database)) and ast.aprovado = 'S'
""".replace('\n\t', ' ')
    
    
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
        consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})

    con.close()

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice_cwb.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querycwb)
    for row in cur.fetchall():
          consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wservice.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(querysp)
    for row in cur.fetchall():
          consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()
    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/wtime.cdb', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()
    cur.execute(queryrj)
    for row in cur.fetchall():
          consulta.append({"OS": row[0],"MARCA":row[1],"LOJA":row[2],"DATA_TERMINO_CONSERTO": row[3].strftime('%m/%d/%Y'),"VALOR": float(row[4])})
    con.close()
    return(consulta)

def brands():

    con = fb.connect(host='172.31.3.114',database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB', port = '3050',user ='SYSDBA', password ='masterkey')
    cur = con.cursor()


    query = """select gr.codigo_grupo_os,gr.descricao_grupo_os
    from e_grupo_os_assist_tecnica   gr

""".replace('\n\t', ' ')

 
    cur.execute(query)
    consulta = list()
    for row in cur.fetchall():
         consulta.append({"CODIGO_MARCA":row[0],"DESCRICAO_MARCA":row[1]})

    con.close()
    return(consulta)


def get_reproved_orders():
     estoklus = Estoklus()
     query = """select codigo_os_assist_tecnica,cg.nome,ast.loja_os,        COALESCE((Select
    Sum(atps_.VALOR_UNITARIO*atps_.QTDE)
    from E_ASSIST_TECNICA_PECAS_SERVICOS atps_
    WHERE (ast.codigo_os_assist_tecnica = atps_.codigo_os_assist_tecnica) and atps_.garantia = 'N' and atps_.extra <> 'S') - ast.VALOR_DESCONTO,0), coalesce(( Select atca.RESPOSTA FROM E_ASSIST_TECNICA_CAMPO_AUXILIAR atca
           WHERE atca.CODIGO_CAMPO_AUXILIAR=88 AND
                 atca.CODIGO_OS_ASSIST_TECNICA = ast.CODIGO_OS_ASSIST_TECNICA ) ,0),ast.data_aprovado,grupo_os_assist_tecnica


from e_assist_tecnica ast
join g_cadastro_geral cg on ast.codigo_cliente = cg.codigo_cadastro_geral


where ast.aprovado = 'N' and
    extract (year from ast.data_aprovado) =    extract (year from (select cast('Now' as date) from rdb$database))

 and   extract (month from ast.data_aprovado) =    extract (month from (select cast('Now' as date) from rdb$database))"""
     
     return [{"OS": row[0],
              "nome": row[1],
              "loja": row[2],
              "valor": float(row[3]),
              "motivo": row[4],
              "data_reprovacao":row[5].strftime('%m/%d/%Y'),
              "marca": row[6]
     }
     
     for row in estoklus.fetchall(query)]




