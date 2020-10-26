from __future__ import print_function 
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
import json
import collections
import cx_Oracle

app = Flask(__name__)
api = Api(app)              #Nos indica que vamos a encerrar nuestra app como un REST API



#Clase para las Consultas a la base de datos 
class DataBase():
    connection = cx_Oracle.connect("d4n11083/root@localhost/xe")
    cursor = connection.cursor()

    #Retorna toda la info de la tabla
    def getUsers(self):
        sql = "SELECT * FROM USUARIO"              #Query 
        self.cursor.execute(sql)                   #Ejecuta el SQL 
        rows = self.cursor.fetchall()              #Carga la variable con todas las filas de la respuesta 

        objects_list = []                          #Lista para convertir todas las filas en json 
        for row in rows:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["name"] = row[1]
            d["location"] = row[2]
            objects_list.append(d)
        j = json.dumps(objects_list)               #Convierte a Json
        return j
    
    #Retorna la iformacion de un usuario dependiendo de su id 
    def getUser(self, pUserId):
        sql = "SELECT * FROM USUARIO WHERE IDUSUARIO =" + pUserId
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        if( len(row) > 0):                         #Si todo salio bien envia el json
            d = collections.OrderedDict()
            d["id"] = row[0][0]
            d["name"] = row[0][1]
            d["location"] = row[0][2]
            j = json.dumps(d)
            return j
        else:   
            return 404                              #Si no retorna 404 User Not Found 
    
    #Aniade un nuevo usuario en la base de datos 
    def addUser(self, pUserJson):   
        IDUSUARIO = pUserJson['id']
        NOMBREUSUARIO = pUserJson['name']
        DIRECCIONUSUARIO = pUserJson['address']
        sql = "INSERT INTO USUARIO VALUES (" + str(IDUSUARIO)+",'"+NOMBREUSUARIO+"','"+DIRECCIONUSUARIO+"'" ")"
        self.cursor.execute(sql)
        self.connection.commit()
        return 201
    
    #Actualiza los campos de un usuario ya existente
    def editUser(self,pUserId, pUserEditJson ):
        if( self.getUser(pUserId) != 404 ):
            NEW_NOMBREUSUARIO = pUserEditJson['name']
            NEW_DIRECCIONUSUARIO = pUserEditJson['address']
            sql = "UPDATE USUARIO SET NOMBREUSUARIO ='"+NEW_NOMBREUSUARIO+"',DIRECCIONUSUARIO = '"+NEW_DIRECCIONUSUARIO+"' WHERE IDUSUARIO ="+pUserId
            self.cursor.execute(sql)
            self.connection.commit()
        else:
            return 404

    def deleteUser(self, pUserId):
        user = self.getUser(pUserId)
        if( user != 404 ):
            sql = "DELETE FROM USUARIO WHERE IDUSUARIO ="+pUserId
            self.cursor.execute(sql)
            self.connection.commit()
            return user
        else:
            return 404       
        
    
#Objeto Base de datos
db = DataBase()

#Funcion oara crear errores
def json_abort(pStatusCode, data=None):
    response = jsonify(data or {'error': 'There was an error'})
    response.status_code = pStatusCode
    abort(response)

#Get incial para ver si el server funciona correctamente
@app.route('/ping', methods=['GET'])
def ping():
    return {"message": "pong"}

#GET para obetner todos los usuarios de la tabla Usuario 
@app.route('/users', methods=['GET'])
def getUsers():
    return {"Users": json.loads(db.getUsers())}

#GET que retorna el usuario bucandolo por medio de id 
@app.route('/users/<string:pUserId>', methods=['GET'])
def getUser(pUserId):
    user = db.getUser(pUserId)
    if(user!=404):
        return {"User": json.loads(user)}
    else:
        return json_abort(404, {'error': 'User not found'})     #Retorna un json con el codigo de error y un mensaje de error al cliente 

@app.route('/users', methods=['POST'])
def addUser():
    print(request.json)
    if(db.addUser(request.json) == 201):
        return jsonify( {"message": "User Added Succesfully", "status_code":201} )

#PUT edita un usuario buscandolo por id 
@app.route('/users/<string:pUserId>', methods=['PUT'])
def editUser(pUserId):
    user = db.editUser(pUserId, request.json)
    if(user!=404):
        return {"User Updated": json.loads(db.getUser(pUserId))}
    else:
        return json_abort(404, {'error': 'User not found cannot change it'})     #Retorna un json con el codigo de error y un mensaje de error al cliente 

#DELETE borra un usuario buscandolo por id
@app.route('/users/<string:pUserId>', methods=['DELETE'])
def deleteUser(pUserId):
    user = db.deleteUser(pUserId)
    if(user!=404):
        return {"UserDeleted": json.loads(user)}
    else:
        return json_abort(404, {'error': 'User not found cannot delete it'})     #Retorna un json con el codigo de error y un mensaje de error al cliente 



if __name__ == "__main__":   #Inicializa el server en modo debug 
    app.run(debug=True)     