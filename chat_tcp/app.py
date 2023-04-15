from flask import Flask, render_template, request
import threading
import socket

app = Flask(__name__)

alias = ""

#Função para lidar com as conexões dos clientes:
#verifica se o cliente existe, caso não exclui ele?
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            message_decoded = message.decode('utf-8')
            print(message_decoded)
        except:
            print('Error!')
            client.close()
            break

#Função para enviar mensagem para o servidor
def send_message(message):
    client.send(message.encode('utf-8'))

#Função para receber mensagem do servidor
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Error!')
            client.close()
            break

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connect", methods=["POST"])
def connect():
    global client, alias
    alias = request.form["alias"]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 59000))
    client.send(alias.encode('utf-8'))
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
    return render_template("chat.html", alias=alias)

@app.route("/send_message", methods=["POST"])
def send():
    message = request.form["message"]
    send_message(f"{alias}: {message}")
    return render_template("chat.html", alias=alias, message_sent=True)

if __name__ == "__main__":
    app.run(debug=True)
