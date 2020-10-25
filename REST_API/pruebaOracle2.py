from __future__ import print_function 
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
import collections
import cx_Oracle

app = Flask(__name__)
api = Api(app)              #Nos indica que vamos a encerrar nuestra app como un REST API




class DataBase():
    connection = cx_Oracle.connect("d4n11083/root@localhost/xe")
    cursor = connection.cursor()

    def getAll(self):
        sql = "SELECT * FROM USUARIO"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["name"] = row[1]
            d["location"] = row[2]
            objects_list.append(d)
        j = json.dumps(objects_list)

        return j
    
    def 

db = DataBase()


class HelloWorld(Resource):  #Maneja los request
    def get(self):
        return {"Usuarios": json.loads(db.getAll()) }
    
    def post(self):
        return {"data":"posted"}

api.add_resource(HelloWorld, "/helloworld")  #root del resource cuando enviamos un request





if __name__ == "__main__":   #Inicializa el server en modo debug 
    app.run(debug=True)     