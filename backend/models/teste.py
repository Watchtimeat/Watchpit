import psycopg2.pool
import psycopg2.extras
import time

sql_echo = "false"
class DatabasePool:
    def __init__(self):
        self.database_url = None
        self.pool = None
        self.initialized = False

    def initialize(self):
        self.database_url = "postgresql://postgres:%25Ekemvm6g@172.31.3.114:5432/watchtime"
        
        if not self.database_url:
            raise Exception("Database URL not configured")
        pool_enabled = "true"
        if pool_enabled:
            pool_min = 1
            pool_max = 4
            self.pool = psycopg2.pool.ThreadedConnectionPool(minconn=pool_min, maxconn=pool_max, dsn=self.database_url)
        self.initialized = True

    def get_connection(self):
        if not self.initialized:
            self.initialize()
        if self.pool:
            return self.pool.getconn()
        else:
            return psycopg2.connect(self.database_url)

    def put_connection(self, connection):
        if self.pool:
            self.pool.putconn(connection)
        else:
            connection.close()


databasePool = DatabasePool()


def set_sql_echo(echo):
    global sql_echo
    sql_echo = echo


def execute(sql, *args, connection=None):
    conn = connection if connection else databasePool.get_connection()
    cur = conn.cursor()
    try:
        start = time.time()
        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        if not connection:
            conn.commit()
        if sql_echo:
            print('--> execute: {}, {}'.format(sql, args))
            print('{}ms'.format(int((time.time() - start) * 1000)))
    except Exception as e:
        if not connection:
            conn.rollback()
        raise e
    finally:
        cur.close()
        if not connection:
            databasePool.put_connection(conn)


def execute_values(sql, args_list, fetch=False, connection=None):
    conn = connection if connection else databasePool.get_connection()
    cur = conn.cursor()
    try:
        start = time.time()
        result = psycopg2.extras.execute_values(cur, sql, args_list, fetch=fetch)
        if not connection:
            conn.commit()
        if sql_echo:
            print('--> execute_values: {}, {}'.format(sql, args_list))
            print('{}ms'.format(int((time.time() - start) * 1000)))
        return result
    except Exception as e:
        if not connection:
            conn.rollback()
        raise e
    finally:
        cur.close()
        if not connection:
            databasePool.put_connection(conn)


def fetchall(sql, *args, connection=None):
    conn = connection if connection else databasePool.get_connection()
    cur = conn.cursor()
    try:
        start = time.time()
        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        result = cur.fetchall()
        if not connection:
            conn.commit()
        if sql_echo:
            print('--> fetchall: {}, {}'.format(sql, args))
            if result:
                print('<--', result)
            print('{}ms'.format(int((time.time() - start) * 1000)))
        return result
    except Exception as e:
        if not connection:
            conn.rollback()
        raise e
    finally:
        cur.close()
        if not connection:
            databasePool.put_connection(conn)


def fetchone(sql, *args, connection=None):
    conn = connection if connection else databasePool.get_connection()
    cur = conn.cursor()
    try:
        start = time.time()
        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        result = cur.fetchone()
        if sql_echo:
            print('--> fetchone: {}, {}'.format(sql, args))
            if result:
                print('<--', result)
            print('{}ms'.format(int((time.time() - start) * 1000)))
        if not connection:
            conn.commit()
        return result
    except Exception as e:
        if not connection:
            conn.rollback()
        raise e
    finally:
        cur.close()
        if not connection:
            databasePool.put_connection(conn)




resultado = get_product_resquested_quantity("HF1000")

print (resultado)

