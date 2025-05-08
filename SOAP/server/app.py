from spyne import Application, rpc, ServiceBase, String, Unicode
from spyne import ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import grpc
import gRPC.server.users_pb2 as users_pb2
import gRPC.server.users_pb2_grpc as users_pb2_grpc

# GRPC channel configuration
channel = grpc.insecure_channel('localhost:50051')
grpc_stub = users_pb2_grpc.UsersStub(channel)

class User(ComplexModel):
    id = String
    name = String
    email = String
    password = String

class UserService(ServiceBase):
    @rpc(String, String, String, _returns=User)
    def create_user(ctx, name, email, password):
        try:
            # Create gRPC request
            user = users_pb2.User(
                name=name,
                email=email,
                password=password
            )
            grpc_response = grpc_stub.CreateUser(users_pb2.CreateUserRequest(user=user))
            
            # Convert gRPC response to SOAP response
            return User(
                id=grpc_response.user.id,
                name=grpc_response.user.name,
                email=grpc_response.user.email,
                password=grpc_response.user.password
            )
        except grpc.RpcError as e:
            ctx.transport.resp_code = 500
            raise ValueError(f"gRPC error: {str(e)}")

    @rpc(_returns=Array(User))
    def get_users(ctx):
        try:
            # Make gRPC request
            grpc_response = grpc_stub.GetUsers(users_pb2.GetUsersRequest())
            
            # Convert gRPC response to SOAP response
            users = []
            for grpc_user in grpc_response.users:
                users.append(User(
                    id=grpc_user.id,
                    name=grpc_user.name,
                    email=grpc_user.email,
                    password=grpc_user.password
                ))
            return users
        except grpc.RpcError as e:
            ctx.transport.resp_code = 500
            raise ValueError(f"gRPC error: {str(e)}")
        
    @rpc(String, _returns=User)
    def get_user_by_id(ctx, user_id):
        try:
            # Make gRPC request
            grpc_response = grpc_stub.GetUserById(users_pb2.GetUserByIdRequest(id=user_id))
            
            # Convert gRPC response to SOAP response
            return User(
                id=grpc_response.user.id,
                name=grpc_response.user.name,
                email=grpc_response.user.email,
                password=grpc_response.user.password
            )
        except grpc.RpcError as e:
            ctx.transport.resp_code = 500
            raise ValueError(f"gRPC error: {str(e)}")

    @rpc(String, String, String, String, _returns=User)
    def update_user(ctx, user_id, name, email, password):
        try:
            # Create gRPC request
            user = users_pb2.User(
                id=user_id,
                name=name,
                email=email,
                password=password
            )
            grpc_response = grpc_stub.UpdateUser(users_pb2.UpdateUserRequest(user=user))
            
            # Convert gRPC response to SOAP response
            return User(
                id=grpc_response.user.id,
                name=grpc_response.user.name,
                email=grpc_response.user.email,
                password=grpc_response.user.password
            )
        except grpc.RpcError as e:
            ctx.transport.resp_code = 500
            raise ValueError(f"gRPC error: {str(e)}")

    @rpc(String, _returns=Unicode)
    def delete_user(ctx, user_id):
        try:
            # Make gRPC request
            grpc_stub.DeleteUser(users_pb2.DeleteUserRequest(id=user_id))
            return "User deleted successfully"
        except grpc.RpcError as e:
            ctx.transport.resp_code = 500
            raise ValueError(f"gRPC error: {str(e)}")


if __name__ == '__main__':
    try:
        application = Application(
            [UserService], 
            tns='users.soap',
            in_protocol=Soap11(validator='lxml'),
            out_protocol=Soap11()
        )
        
        wsgi_application = WsgiApplication(application)
        server = make_server('127.0.0.1', 8000, wsgi_application)
        
        print("SOAP Server running at http://127.0.0.1:8000")
        print("Connected to gRPC server at localhost:50051")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        channel.close()