__author__ = 'xxd'
from django.db import connection

def get_sql_data(sql):
    cursor = connection.cursor()

    cursor.execute(sql)

    return dictfetchall(cursor)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_sql_data_params(sql,params):
    cursor = connection.cursor()

    cursor.execute(sql,params)

    return dictfetchall(cursor)