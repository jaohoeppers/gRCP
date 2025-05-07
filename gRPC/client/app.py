from __future__ import print_function

import grpc
import users_pb2
import users_pb2_grpc
import uuid

def create_user(stub, name, email, password):
    user = users_pb2.User(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=password
    )
    response = stub.CreateUser(users_pb2.CreateUserRequest(user=user))
    return response.user

def display_users(users):
    print("\n=== Lista de Usuários ===")
    print("ID | Nome | Email | Password")
    print("-" * 50)
    for user in users:
        print(f"{user.id[:8]}... | {user.name} | {user.email} | {user.password}")
    print("-" * 50)
    
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        
        # Criar alguns usuários de exemplo
        print("Criando usuários...")
        users_to_create = [
            ("João Silva", "joao@email.com", "senha123"),
            ("Maria Santos", "maria@email.com", "senha456"),
            ("Pedro Souza", "pedro@email.com", "senha789")
        ]
        
        for name, email, password in users_to_create:
            try:
                user = create_user(stub, name, email, password)
                print(f"Usuário criado: {user.name}")
            except grpc.RpcError as e:
                print(f"Erro ao criar usuário: {e.details()}")
        
        # Buscar e mostrar todos os usuários
        print("\nBuscando todos os usuários...")
        try:
            response = stub.GetUsers(users_pb2.GetUsersRequest())
            display_users(response.users)
        except grpc.RpcError as e:
            print(f"Erro ao buscar usuários: {e.details()}")

if __name__ == '__main__':
    run()