import threading
import socket

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
messages = []  # lista para armazenar as mensagens transmitidas


#Enviar mensagem para todos os presentes no servidor:
# Em síntese ela recebe a mensagem e efetua um loop na lista de clientes,
#enviando a mensagem pra cada cliente presente na lista
def broadcast(message):
    messages.append(message)  # adiciona a mensagem à lista de mensagens
    for client in clients:
        client.send(message)
        
#Função para lidar com as conexões dos clientes:
#verifica se o cliente existe, caso não exclui ele?
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} saiu do chat!'.encode('utf-8'))
            aliases.remove(alias)
            break
        
# Função principal do programa!
def receive():
    while True:
        print('Server on!')
        client, address = server.accept()
        print(f'Conexão estabelecida com: {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'Nick do user é {alias}'.encode('utf-8'))
        broadcast(f'{alias} se conectou ao chat!'.encode('utf-8'))
        client.send('você está conectado!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
