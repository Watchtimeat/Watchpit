from models.estoklus import Estoklus

def brands():
    query = """select descricao_grupo_os,codigo_grupo_os from e_grupo_os_assist_tecnica where metodo_planejamento = 2"""
    estoklus = Estoklus()
    retorno = list()
    for row in estoklus.fetchall(query) :
        

        retorno.append ({
            "brand": row[0],
            'brand_id': row[1],
            "agrupa": 'S'})
    data = list()
    data = {"data": retorno}
    return(data)