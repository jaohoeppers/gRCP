from flask import Flask, request, jsonify
import argparse

import uuid
import grpc
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root_dir)

from Servidor_gRCP.gRPC.server import users_pb2
from Servidor_gRCP.gRPC.server import users_pb2_grpc


app = Flask(__name__)
channel = None
stub = None

def init_grpc():
    global channel, stub
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = users_pb2_grpc.UsersStub(channel)

@app.teardown_appcontext
def cleanup(exception=None):
    global channel
    if channel is not None:
        channel.close()

@app.route('/item', methods=['POST'])
def create_item():
    
    init_grpc()
    
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    try:
        user = users_pb2.User(
            id=str(uuid.uuid4()),
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        response = stub.CreateUser(users_pb2.CreateUserRequest(user=user))
        return jsonify({"id": response.user.id, 
                       "name": response.user.name, 
                       "email": response.user.email}), 201
    except grpc.RpcError as e:
        return jsonify({"error": str(e.details())}), 500

# Read - GET (all items)
@app.route('/items', methods=['GET'])
def get_items():
    init_grpc()
    
    try:
        response = stub.GetUsers(users_pb2.GetUsersRequest())
        
        # Convert gRPC response to JSON-serializable format
        users_list = []
        for user in response.users:
            users_list.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password
            })
        
        return jsonify({"users": users_list}), 200
        
    except grpc.RpcError as e:
        return jsonify({"error": str(e.details())}), 500
    
#search by id
@app.route('/item/<string:user_id>', methods=['GET'])
def get_item_by_id(user_id):
    init_grpc()
    
    try:
        response = stub.GetUserById(users_pb2.GetUserByIdRequest(id=user_id))
        return jsonify({
            "id": response.user.id,
            "name": response.user.name,
            "email": response.user.email,
            "password": response.user.password
        }), 200
    except grpc.RpcError as e:
        return jsonify({"error": str(e.details())}), 500

#update by id
@app.route('/item/<string:user_id>', methods=['PUT'])
def update_item(user_id):
    init_grpc()
    
    data = request.get_json()
    
    if not any(key in data for key in ['name', 'email', 'password']):
        return jsonify({'error': 'At least one field to update is required'}), 400
    
    try:
        user = users_pb2.User(
            id=user_id,
            name=data.get('name', ''),
            email=data.get('email', ''),
            password=data.get('password', '')
        )
        response = stub.UpdateUser(users_pb2.UpdateUserRequest(user=user))
        return jsonify({
            "id": response.user.id,
            "name": response.user.name,
            "email": response.user.email
        }), 200
    except grpc.RpcError as e:
        return jsonify({"error": str(e.details())}), 500

#delete by id
@app.route('/item/<string:user_id>', methods=['DELETE'])
def delete_item(user_id):
    init_grpc()
    
    try:
        response = stub.DeleteUser(users_pb2.DeleteUserRequest(id=user_id))
        return jsonify({"message": "User deleted successfully"}), 200
    except grpc.RpcError as e:
        return jsonify({"error": str(e.details())}), 500


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=os.getenv('PORT', 5000))
    args = parser.parse_args()
    
    init_grpc()
    port = args.port
    print(f"Servidor rodando em http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
