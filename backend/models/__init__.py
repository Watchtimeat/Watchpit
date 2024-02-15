import os
import psycopg2.pool
import psycopg2.extras
import time

# Database configurations
sql_echo = os.environ.get("SQL_ECHO", "false").lower() == "true"

# SMS SMTP configuration
smtp_host = os.environ.get("SMTP_HOST")
smtp_port = os.environ.get("SMTP_PORT")
smtp_sender = os.environ.get("SMTP_SENDER")
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")


class DatabasePool:
    def __init__(self):
        self.database_url = None
        self.pool = None
        self.initialized = False

    def initialize(self):
        if "DATABASE_URL" in os.environ:  # required to connect to the database
            self.database_url = os.environ["DATABASE_URL"]
        elif "RDS_HOST" in os.environ:  # required to connect to the database when running on AWS Elastic Beanstalk or AWS Lambda
            self.database_url = "postgresql://{}:{}@{}:{}/{}".format(
                os.environ.get("RDS_USERNAME", ""),
                os.environ.get("RDS_PASSWORD", ""),
                os.environ.get("RDS_HOST", ""),
                os.environ.get("RDS_PORT", ""),
                os.environ.get("RDS_DB_NAME", "")
            )
        if not self.database_url:
            raise Exception("Database URL not configured")
        pool_enabled = os.environ.get("POOL", "false").lower() == "true"
        if pool_enabled:
            pool_min = int(os.environ.get("POOL_MIN", 1))
            pool_max = int(os.environ.get("POOL_MAX", 4))
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


def create_database():
    execute("create extension pg_trgm")
    execute('create schema watchtime')
    execute("create table watchtime.users (id text, email text, data jsonb, primary key (id))")
    execute("create index users_index1 on watchtime.users (email)")
    execute("create table watchtime.products (id text, data jsonb, primary key (id))")
    execute("create index products_index1 on watchtime.products using gin (lower(data->>'code') gin_trgm_ops)")
    execute("create index products_index2 on watchtime.products using gin (lower(data->>'name') gin_trgm_ops)")
    execute("create index products_index3 on watchtime.products ((data->>'brand'))")
    execute("create table watchtime.resources (id text, data jsonb, primary key (id))")
    execute("create table watchtime.files (id text, file bytea, primary key (id))")
    execute("create table watchtime.purchase_orders (id text, data jsonb, primary key (id))")
    execute("create table watchtime.purchase_order_items (id text, purchase_order_id text, data jsonb, primary key (id))")
    execute("create index purchase_order_index1 on watchtime.purchase_order_items (purchase_order_id)")
    execute("create table watchtime.purchase_invoices (id text, data jsonb, primary key (id))")
    execute("create table watchtime.purchase_invoice_items (id text, purchase_invoice_id text, data jsonb, primary key (id))")
    execute("create index purchase_invoice_index1 on watchtime.purchase_invoice_items (purchase_invoice_id)")


def drop_database():
    execute("drop table if exists watchtime.users cascade")
    execute("drop table if exists watchtime.resources cascade")
    execute("drop table if exists watchtime.files cascade")
    execute("drop table if exists watchtime.products cascade")
    execute("drop table if exists watchtime.purchase_orders cascade")
    execute("drop table if exists watchtime.purchase_order_items cascade")
    execute("drop table if exists watchtime.purchase_invoices cascade")
    execute("drop table if exists watchtime.purchase_invoice_items cascade")
    execute("drop schema watchtime")
