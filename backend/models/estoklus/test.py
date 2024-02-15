import fdb


# Parâmetros de conexão
host = '172.31.3.114'
database = 'D:/CDSIS/Dat/WATCHTIME_GERAL.CDB'
user = 'SYSDBA'
password = 'masterkey'
port = 3050
charset = 'utf-8'

# Estabelecendo conexão
con = fdb.connect(dsn=host + '/' + str(port) + ':' + database, user=user, password=password)

# Criando um cursor
cur = con.cursor()

# Executando uma consulta SQL
cur.execute("""select codigo_cadastro_geral, nome,cg.tel_trabalho,cg.tel_celular,cg.tel_outros,cg.cpf,cg.cnpj,cg.codigo_tipo_pessoa,  logradouro,cg.numero, complemento, bairro,  cidade,cg.cep,cg.uf,cg.email


from g_cadastro_geral cg  where codigo_tipo_pessoa <> 'E'""")  # Substitua nome_da_tabela pelo nome real da tabela

# Recuperando e imprimindo os resultados
for row in cur.fetchall():
    print(row[0],row[1])

# Fechando o cursor e a conexão
cur.close()
con.close()
