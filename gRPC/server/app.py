from concurrent import futures
import json
import logging
import os

import grpc
import users_pb2
import users_pb2_grpc


# Função para iniciar o servidor gRPC
def serve():
    # Criação do servidor gRPC com um pool de threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Registro do serviço Users na instância do servidor
    users_pb2_grpc.add_UsersServicer_to_server(users_pb2_grpc.UsersServicer(), server)

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