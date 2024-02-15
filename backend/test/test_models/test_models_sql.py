import unittest

from models.sql import build_where, build_order, build_limit, build_sql, build_columns, build_column, is_distinct, build_select

TABLE = "table"
JSON = "data"
FIELDS = ["id", "data"]


class TestSql(unittest.TestCase):

    def test_build_column(self):
        self.assertEqual("data", build_column("data", FIELDS))
        self.assertEqual("data->>'column'", build_column("column", FIELDS))

    def test_build_columns(self):
        self.assertEqual({"id": "id", "data": "data"}, build_columns(FIELDS, {}))
        self.assertEqual({"column": "data->>'column'"}, build_columns(FIELDS, {"_select": "column"}))
        self.assertEqual({"column1": "data->>'column1'", "column2": "data->>'column2'"}, build_columns(FIELDS, {"_select": "column1,column2"}))
        self.assertEqual({"id": "id", "column": "data->>'column'"}, build_columns(FIELDS, {"_select": "id,column"}))

    def test_is_distinct(self):
        self.assertFalse(is_distinct({}))
        self.assertFalse(is_distinct({"_distinct": False}))
        self.assertFalse(is_distinct({"_distinct": ""}))
        self.assertFalse(is_distinct({"_distinct": "a"}))
        self.assertTrue(is_distinct({"_distinct": True}))
        self.assertTrue(is_distinct({"_distinct": "True"}))
        self.assertTrue(is_distinct({"_distinct": "true"}))

    def test_build_select(self):
        self.assertEqual("count(*) over()", build_select({}, False))
        self.assertEqual("col1, count(*) over()", build_select({"col1": "col1"}, False))
        self.assertEqual("col1, col2, count(*) over()", build_select({"col1": "col1", "col2": "col2"}, False))
        self.assertEqual("distinct ", build_select({}, True))
        self.assertEqual("distinct col1", build_select({"col1": "col1"}, True))
        self.assertEqual("distinct col1, col2", build_select({"col1": "col1", "col2": "col2"}, True))

    def test_where(self):
        self.assertEqual("where id = '1'", build_where(FIELDS, {"id": "1"}))
        self.assertEqual("where id = '1' and data->>'name' = 'name'", build_where(FIELDS, {"id": "1", "name": "name"}))
        self.assertEqual("where data->>'other' = 'name'", build_where(FIELDS, {"other": "name"}))
        self.assertEqual("where id in ('n1', 'n2')", build_where(FIELDS, {"id": ["n1", "n2"]}))
        self.assertEqual("where data->>'date' > '2022-01-01'", build_where(FIELDS, {"date.gt": "2022-01-01"}))
        self.assertEqual("where lower(data->>'column') like lower('text')", build_where(FIELDS, {"column.lk": "text"}))
        self.assertEqual("where (lower(data->>'col1') like lower('text') or lower(data->>'col2') like lower('text'))", build_where(FIELDS, {"col1.lk,col2.lk": "text"}))

    def test_order(self):
        self.assertEqual("order by id", build_order(FIELDS, {"_order_a": "id"}))
        self.assertEqual("order by data->>'other'", build_order(FIELDS, {"_order_a": "other"}))
        self.assertEqual("order by id desc", build_order(FIELDS, {"_order_d": "id"}))

    def test_limit(self):
        self.assertEqual("limit 10", build_limit({"_limit": "10"}))
        self.assertEqual("limit 10 offset 10", build_limit({"_limit": "10", "_offset": "10"}))

    def test_build_sql(self):
        self.assertEqual("select id, data, count(*) over() from table", build_sql(TABLE, FIELDS, {}, build_columns(FIELDS, {})))
        self.assertEqual("select id, data->>'column1', count(*) over() from table", build_sql(TABLE, FIELDS, {"_select": "id, column1"}, build_columns(FIELDS, {"_select": "id, column1"})))
        self.assertEqual("select data->>'column1', data->>'column2', count(*) over() from table", build_sql(TABLE, FIELDS, {"_select": "column1, column2"}, build_columns(FIELDS, {"_select": "column1, column2"})))

        self.assertEqual("select distinct id, data from table", build_sql(TABLE, FIELDS, {"_distinct": True}, build_columns(FIELDS, {"_distinct": True})))
        self.assertEqual("select distinct data->>'column1' from table", build_sql(TABLE, FIELDS, {"_select": "column1", "_distinct": True}, build_columns(FIELDS, {"_select": "column1", "_distinct": True})))

        self.assertEqual("select id, data, count(*) over() from table where id = '1'", build_sql(TABLE, FIELDS, {"id": "1"}, build_columns(FIELDS, {"id", "1"})))
        self.assertEqual("select id, data, count(*) over() from table where data->>'col1' = '1'", build_sql(TABLE, FIELDS, {"col1": "1"}, build_columns(FIELDS, {"col1", "1"})))
        self.assertEqual("select id, data, count(*) over() from table where data->>'col1' = '1' order by data->>'col1'", build_sql(TABLE, FIELDS, {"col1": "1", "_order_a": "col1"}, build_columns(FIELDS, {"col1": "1", "_order_a": "col1"})))
        self.assertEqual(
            "select id, data, count(*) over() from table where data->>'col1' = '1' order by data->>'col1' limit 10 offset 10",
            build_sql(
                TABLE,
                FIELDS,
                {"col1": "1", "_order_a": "col1", "_limit": 10, "_offset": 10},
                build_columns(
                    FIELDS,
                    {"col1": "1", "_order_a": "col1", "_limit": 10, "_offset": 10}
                )
            )
        )
