from models import fetchall

OPERATORS = {
    "eq": "=",
    "ne": "<>",
    "gt": ">",
    "ge": ">=",
    "lt": "<",
    "le": "<=",
    "lk": "like"
}


def build_column(column, fields):
    return column if column in fields else "data->>'{}'".format(column)


def build_value(value, operator):
    if isinstance(value, str):
        return "'{}'".format(value)
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, list):
        return "({})".format(", ".join([build_value(v, operator) for v in value]))
    else:
        raise Exception("unable to build {}".format(value))


def build_columns(fields, filters):
    if "_select" in filters:
        return {key.strip(): build_column(key.strip(), fields) for key in filters["_select"].split(",")}
    else:
        return {field: field for field in fields}


def is_distinct(filters):
    return str(filters.get("_distinct", "")).lower() == "true"


def build_select(columns, distinct):
    return ("distinct " if distinct else "") + (", ".join(list(columns.values()) + (["count(*) over()"] if not distinct else [])))


def build_where(fields, filters):
    where = list()
    for key, value in filters.items():
        if not key.startswith("_"):
            terms = key.split(",")
            conditions = list()
            for term in terms:
                split = term.split(".")
                field = split[0] if split[0] in fields else "data->>'{}'".format(split[0])
                operator = OPERATORS.get(split[1], "?") if len(split) == 2 else "in" if isinstance(value, list) else "="
                if isinstance(value, int) or isinstance(value, float):
                    conditions.append("cast({} as float) {} {}".format(field, operator, build_value(value, operator)))
                elif operator == "like":
                    conditions.append("unaccent(lower({})) {} unaccent(lower({}))".format(field, operator, build_value(value, operator)))
                else:
                    conditions.append("{} {} {}".format(field, operator, build_value(value, operator)))
            where.append(
                ("(" if len(conditions) > 1 else "") + (" or ".join(conditions)) + (")" if len(conditions) > 1 else ""))
    return "where {}".format(" and ".join(where)) if where else ""


def build_order(fields, filters):
    if "_order_a" in filters:
        return "order by {}".format(
            ", ".join([key if key in fields else "data->>'{}'".format(key) for key in filters["_order_a"].split(",")]))
    elif "_order_d" in filters:
        return "order by {} desc".format(
            ", ".join([key if key in fields else "data->>'{}'".format(key) for key in filters["_order_d"].split(",")]))
    return ""


def build_limit(filters):
    result = list()
    if "_limit" in filters:
        result.append("limit {}".format(int(filters["_limit"])))
        if "_offset" in filters:
            result.append("offset {}".format(int(filters["_offset"])))
    return " ".join(result)


def build_sql(table, fields, filters, columns):
    return "select {} from {} {} {} {}".format(
        build_select(columns, is_distinct(filters)),
        table,
        build_where(fields, filters),
        build_order(fields, filters),
        build_limit(filters)
    ).strip()


def select_data(table, fields, json, filters=None, connection=None):
    if not filters:
        filters = dict()
    columns = build_columns(fields, filters)
    sql = build_sql(table, fields, filters, columns)
    data = list()
    rows = 0
    result = fetchall(sql, connection=connection)
    for row in result:
        keys = list(columns.keys())
        record = dict()
        for i in range(len(keys)):
            if keys[i] == json:
                record = {**record, **row[i]}
            else:
                record[keys[i]] = row[i]
        data.append(record)
        rows = len(result) if is_distinct(filters) else int(row[len(columns.keys())])
    return {"data": data, "rows": rows, "sql": sql}