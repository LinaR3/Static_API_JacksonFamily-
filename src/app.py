"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure 



app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
#llamad de TODOS los miembros con funcion: 
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e: 
        return jsonify({"error": str(e)}), 500

#llamado de miembro pero por ID, individual:
def get_one_member(member_id):
    try:
        member = jackson_family.get_member(id)
        if member == None:
            return jsonify({"msg": "Miembro no encontrado"}), 404
        return jsonify (member),200
    except Exception as e:
        return jsonify({"error":str (e)}), 5000

#codigo para agregar un miembro:
@app.route('/members', methods=['POST'])
def add_new_member():
    try:
        request_body = request.get_json()
        # Con validación básica de campos
        if not request_body or "first_name" not in request_body or "age" not in request_body or "lucky_numbers" not in request_body:
            return jsonify({"msg": "Bad request, missing required fields"}), 400

        new_member = jackson_family.add_member(request_body)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return jsonify({"done": False, "msg": "Miembro no encontrado"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
