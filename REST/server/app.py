from flask import Flask, request, jsonify
import os
import argparse
import REST.client.users_pb2 as users_pb2
import REST.client.users_pb2_grpc as users_pb2_grpc
import uuid
import grpc

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

@app.route('/items', methods=['POST'])
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=os.getenv('PORT', 5000))
    args = parser.parse_args()
    
    init_grpc()
    port = args.port
    print(f"Servidor rodando em http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
