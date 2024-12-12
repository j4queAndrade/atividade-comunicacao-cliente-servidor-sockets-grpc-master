from concurrent import futures
import sys
sys.path.append('../proto')
import catalogo_pb2
import catalogo_pb2_grpc
import grpc

catalogo = {
    "mesa": {"preco": 900.0, "quantidade": 50},
    "cadeira": {"preco": 150.0, "quantidade": 100},
    "geladeira": {"preco": 3000.0, "quantidade": 20},
}

class CatalogoService(catalogo_pb2_grpc.CatalogoServiceServicer):
    def ConsultarNome(self, request, context):
        produto = catalogo.get(request.nome.lower())
        if produto:
            return catalogo_pb2.ProdutoResponse(
                nome=request.nome, preco=produto["preco"], quantidade=produto["quantidade"], mensagem="Produto encontrado"
            )
        return catalogo_pb2.ProdutoResponse(mensagem="Produto não encontrado")

    def ConsultarPreco(self, request, context):
        produtos = [
            catalogo_pb2.ProdutoResponse(nome=nome, preco=info["preco"], quantidade=info["quantidade"])
            for nome, info in catalogo.items()
            if info["preco"] < request.precoMaximo
        ]
        return catalogo_pb2.ProdutosResponse(produtos=produtos)

    def AtualizarEstoque(self, request, context):
        produto = catalogo.get(request.nome.lower())
        if produto:
            produto["quantidade"] = request.quantidade
            return catalogo_pb2.AtualizarEstoqueResponse(mensagem="Estoque atualizado")
        return catalogo_pb2.AtualizarEstoqueResponse(mensagem="Produto não encontrado")

def servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalogo_pb2_grpc.add_CatalogoServiceServicer_to_server(CatalogoService(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

servidor()
