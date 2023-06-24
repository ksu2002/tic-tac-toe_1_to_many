'''
import socket

# создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# задаем адрес и порт для прослушивания
server_address = ('localhost', 5000)
server_socket.bind(server_address)

# начинаем прослушивание
server_socket.listen(2)

print('Сервер запущен и ожидает подключения клиентов...')

# принимаем подключение первого клиента
client1_socket, client1_address = server_socket.accept()
print(f'Первый клиент подключен: {client1_address}')

# принимаем подключение второго клиента
client2_socket, client2_address = server_socket.accept()
print(f'Второй клиент подключен: {client2_address}')

while True:
    # читаем одну цифру от первого клиента
    data = client1_socket.recv(2)
    if not data:
        break
    print(f'Первый клиент отправил цифру: {data.decode()}')

    # отправляем цифру второму клиенту
    client2_socket.sendall(data)

    # читаем одну цифру от второго клиента
    data = client2_socket.recv(2)
    if not data:
        break
    print(f'Второй клиент отправил цифру: {data.decode()}')

    # отправляем цифру первому клиенту
    client1_socket.sendall(data)

# закрываем соединения и сокеты
client1_socket.close()
client2_socket.close()
server_socket.close()
'''
import socket
import threading

def handle_client(client_socket, client_address, clients):
    while True:

        '''
        if (clients[index] == clients[-1] and len(clients) % 2 == 1):
            print(f'66')
            client_socket.sendall(str(30).encode())
            continue
           ## client_socket.close()
           '''
        data = client_socket.recv(2)

        index = clients.index(client_socket)
        if not data:
            break
        print(f'Клиент {client_address} отправил цифру: {data.decode()}, {index}, {len(clients)}')
        ##   index = clients.index(client_socket)
        if index % 2 == 0 and index + 1 < len(clients):

            print(f'2')
            other_client_socket = clients[index + 1]
            other_client_socket.sendall(data)
        elif index % 2 == 1:
            print(f'3')
            other_client_socket = clients[index - 1]
            other_client_socket.sendall(data)
        else:

            print(f'Клиентправилfsfges')
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# прослушивание
server_address = ('localhost', 5000)
server_socket.bind(server_address)
server_socket.listen(10)

print('Сервер запущен и ожидает подключения клиентов...')

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f'Клиент подключен: {client_address}')
   ## if clients[-1] and len(clients) % 2 ==1:
    if(len(clients) % 2 == 0):
        thread1 = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        thread2= threading.Thread(target=handle_client, args=(clients[-2], 'нечетный', clients))
        thread1.start()
        thread2.start()