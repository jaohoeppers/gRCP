from concurrent import futures
import json
import logging
import os

import grpc
import users_pb2
import users_pb2_grpc


# Implementação do serviço gRPC
class Users(users_pb2_grpc.UsersServicer):
    def __init__(self):
        self.users_file = "users.txt"

    def GetUsers(self, request, context):
        try:
            users_list = []
            
            # Verifica se o arquivo existe
            if os.path.exists(self.users_file):
                # Lê os usuários do arquivo
                with open(self.users_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            # Converte cada linha JSON em um objeto User
                            user_data = json.loads(line)
                            user = users_pb2.User(
                                id=user_data['id'],
                                name=user_data['name'],
                                email=user_data['email'],
                                password=user_data['password']
                            )
                            users_list.append(user)
            
            # Retorna a lista de usuários
            return users_pb2.GetUsersResponse(users=users_list)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error getting users: {str(e)}')
            return users_pb2.GetUsersResponse()


# Função para iniciar o servidor gRPC
def serve():
    # Criação do servidor gRPC com um pool de threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Registro do serviço Users na instância do servidor
    users_pb2_grpc.add_UsersServicer_to_server(Users(), server)

    # Adiciona uma porta de escuta não segura (insecure) no servidor
    server.add_insecure_port('[::]:50051')

    # Inicia o servidor
    server.start()

    # Aguarda a finalização do servidor
    server.wait_for_termination()


if __name__ == '__main__':
    # Configuração do logging básico
    logging.basicConfig()
    print("Starting server in: %s" % ('127.0.0.1:50051'))

    # Inicia o servidor
    serve()