import socket
import json

catalogo = {
    "mesa": {"nome": "mesa", "preco": 900.0, "quantidade": 50},
    "cadeira": {"nome": "cadeira","preco": 150.0, "quantidade": 100},
    "geladeira": {"nome": "geladeira","preco": 3000.0, "quantidade": 20},
}

def processar_comando(comando):
    """Processa os comandos recebidos do cliente."""
    partes = comando.split(" ")
    operacao = partes[0]

    if operacao == "consultar_nome":
        nome = partes[1].lower()
        print(nome)
        produto = catalogo.get(nome)
        return json.dumps(produto) if produto else "Produto não encontrado."
    
    elif operacao == "consultar_preco":
        preco_max = float(partes[1])
        produtos = [p for p in catalogo if catalogo[p]["preco"] < preco_max]
        return json.dumps(produtos)
    
    elif operacao == "atualizar_estoque":
        nome = partes[1].lower()
        quantidade = int(partes[2])
        if nome in catalogo:
            catalogo[nome]["quantidade"] = quantidade
            return "Estoque atualizado."
        else:
            return "Produto não encontrado."

    return "Comando inválido."

def servidor():
    """Inicia o servidor."""
    host = "localhost"
    port = 12347

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor rodando em {host}:{port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexão estabelecida com {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    comando = data.decode()
                    resposta = processar_comando(comando)
                    conn.sendall(resposta.encode())

servidor()
