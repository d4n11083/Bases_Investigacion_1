from __future__ import print_function 

import cx_Oracle

connection = cx_Oracle.connect("d4n11083/root@localhost/xe")

sql = "SELECT * FROM USUARIO"

cursor = connection.cursor()

for result in cursor.execute(sql):
    print(result)