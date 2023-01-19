"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/addmember', methods=['POST'])
def add_member():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    age = request.json.get("age")
    lucky_numbers = request.json.get("lucky_numbers")
    member_data = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "lucky_numbers": lucky_numbers}
    jackson_family.add_member(member_data)
    return jsonify("usuario creado con exito", member_data), 200

@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member_by_id(int(id))
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "usuario no encontrado"}), 404

@app.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    if jackson_family.delete_member(int(id)):
        return jsonify({"message": "member eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "member no existe"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
