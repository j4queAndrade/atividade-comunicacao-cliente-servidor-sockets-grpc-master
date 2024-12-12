import socket

def cliente():
    """Cliente que se conecta ao servidor."""
    host = "localhost"
    port = 12347

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        
        comando = "consultar_nome mesa"
        s.sendall(comando.encode())
        resposta = s.recv(1024)
        print("Resposta do servidor:", resposta.decode())

        comando = "consultar_preco 300"
        s.sendall(comando.encode())
        resposta = s.recv(1024)
        print("Produtos encontrados:", resposta.decode())

        comando = "atualizar_estoque geladeira 50"
        s.sendall(comando.encode())
        resposta = s.recv(1024)
        print("Resposta do servidor:", resposta.decode())

cliente()
