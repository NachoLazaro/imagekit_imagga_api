from flask import Blueprint, request, make_response, jsonify
from . import controller
import requests
from datetime import datetime
import ast
import json

bp = Blueprint('views', __name__)

@bp.route('/')
def index():
    return '<h1>Bienvenido a mi Proyecto</h1>'


@bp.post("/post_image")
def post_image():

    try:
        parametros=dict(request.args)
        data=request.get_data().decode('utf-8')
        data_json=json.loads(data)
        parametros['imagenb64']=data_json["data"]
        image_id=controller.post_image(**parametros)
        return jsonify(image_id)
    except:
        return make_response({"error": "Imagen no válida"}, 400)

@bp.get("/images")
def get_images():

    data=request.args.get("data",None)
    
    try:
        if data is None:
            print("Entra if")
            imagenes=controller.get_images()
            print("Imagenes OK")
            return jsonify(imagenes)
        else:
            print("Entra else")
            parametros=ast.literal_eval(data)
            imagenes=controller.get_images(**parametros)
            return jsonify(imagenes)

    except:
         return make_response({"error": "Error al recuperar imagenes"}, 400)
    
@bp.get("/image_id")
def get_image_id():

    id=request.args.get("id",None)
    if id is not None:
        imagen=controller.get_image(id)
        print("Imagen recuperada OK")
        return jsonify(imagen)
    else:
        return make_response({"error": "La imagen no existe"}, 400)
    


    endpoint= "http://localhost:8080/post_image"

