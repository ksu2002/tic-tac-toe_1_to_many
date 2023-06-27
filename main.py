import socket
import threading

def handle_client(client_socket,clients):
    while True:
        try:
            data = client_socket.recv(2)
        except ConnectionAbortedError:
            print("Соединение было разорвано хост-компьютером")
        index = clients.index(client_socket)
        if not data:
            break
        if index % 2 == 0:
            other_client_socket = clients[index + 1]
            other_client_socket.sendall(data)
        elif index % 2 == 1:
            other_client_socket = clients[index - 1]
            other_client_socket.sendall(data)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
server_socket.bind(server_address)
server_socket.listen(10)

print('Сервер запущен и ожидает подключения клиентов...')

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f'Клиент подключен: {client_address}')
    if(len(clients) % 2 == 0):
        thread1 = threading.Thread(target=handle_client, args=(client_socket, clients))
        thread2= threading.Thread(target=handle_client, args=(clients[-2], clients))
        thread1.start()
        thread2.start()