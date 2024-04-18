from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member)



@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    jackson_family.add_member(data)
    return jsonify({"message": "Member added successfully"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if not result:
        return jsonify({'message': 'Member not found'}), 404
    return jsonify({'done': True})


@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    updated_member = jackson_family.update_member(member_id, data)
    if updated_member:
        return jsonify({"message": "Member updated successfully"}), 200
    return jsonify({"message": "Member not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

