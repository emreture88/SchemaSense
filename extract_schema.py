# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:29:41 2025

@author: Emre.Ture
"""

import mysql.connector

def extract_mysql_schema(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    schema = []

    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [row[0] for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        fks = cursor.fetchall()
        foreign_keys = [
            {
                "column": col,
                "references": f"{ref_table}.{ref_col}"
            } for col, ref_table, ref_col in fks
        ]

        schema.append({
            "table": table,
            "columns": columns,
            "foreign_keys": foreign_keys
        })

    return schema