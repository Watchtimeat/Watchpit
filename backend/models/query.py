

def consulta_usuario_cliente_OS(filter):
    query = f"""select f.nome,f.email,cg.nome,cg.email

from b_usuario f
join e_assist_tecnica ast on ast.inclusao_por = f.codigo_usuario
join g_cadastro_geral cg on cg.codigo_cadastro_geral = ast.codigo_cliente 


where ast.codigo_os_assist_tecnica = {filter} """
    return query


