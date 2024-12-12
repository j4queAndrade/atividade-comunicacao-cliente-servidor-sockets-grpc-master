import grpc
import sys
sys.path.append('../proto')
import catalogo_pb2
import catalogo_pb2_grpc

def cliente():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = catalogo_pb2_grpc.CatalogoServiceStub(channel)

        resposta = stub.ConsultarNome(catalogo_pb2.ConsultaNomeRequest(nome="geladeira"))
        print(resposta)

        resposta = stub.ConsultarPreco(catalogo_pb2.ConsultaPrecoRequest(precoMaximo=300))
        print(resposta.produtos)

        resposta = stub.AtualizarEstoque(catalogo_pb2.AtualizarEstoqueRequest(nome="mesa", quantidade=80))
        print(resposta)

cliente()
