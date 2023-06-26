import socket
import sys
import threading
import tkinter as tk
from tkinter import messagebox
q = True
# создаем окно приложения
root = tk.Tk()
root.title("Крестики-нолики")

# создаем рамку для игровой доски
board_frame = tk.Frame(root, padx=40, pady=40, bg="#B38DF9")
board_frame.pack()
# создаем фрейм для метки
label_frame = tk.Frame(root, bg="#ffffff")
label_frame.pack(side="top", fill="x")

# добавляем метку во фрейм
label = tk.Label(label_frame, text=" ", font=("Arial", 16), bg="#ffffff")
label.pack(pady=10)
# создаем ячейки для игровой доски
cells = []
for i in range(3):
    row = []
    for j in range(3):
        cell = tk.Button(board_frame, text=" ", font=("Arial", 20), width=4, height=2)
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

# создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# задаем адрес и порт сервера
server_address = ('localhost', 5000)

# подключаемся к серверу
client_socket.connect(server_address)

def check_win():
    win  = 0
    lose = 0
    for i in range(3):
        if (cells[i][i]['text']=='X'):
            win +=1
        if (cells[i][i]['text']=='0'):
            lose +=1
    if  win == 3:
        messagebox.showinfo("Игра окончена", "Вы выиграли")
       # root.quit()
        client_socket.close()
        root.quit()
        exit()
    if  lose == 3:
        messagebox.showinfo("Игра окончена", "Вы проиграли")
        client_socket.close()
        # messagebox.showinfo("Игра окончена", "сокет зыкрылся")
        root.quit()
        exit()
    win = 0
    lose = 0
    for i in range(3):
        for j in range(3):
            if cells[i][j]['text']=='X':
                win +=1
                if win == 3:
                    messagebox.showinfo("Игра окончена", "Вы выиграли")
                   # root.quit()
                    client_socket.close()
                    root.quit()
                    exit()
        win = 0
    for i in range(3):
        for j in range(3):
            if cells[j][i]['text'] == 'X':
                win += 1
                if win == 3:
                    messagebox.showinfo("Игра окончена", "Вы выиграли")
                #    root.quit()
                    client_socket.close()
                    root.quit()
                    exit()
        win = 0
    for i in range(3):
        for j in range(3):
            if cells[i][j]['text']=='0':
                lose +=1
                if lose == 3:
                    messagebox.showinfo("Игра окончена", "Вы проиграли")
                    client_socket.close()
                   # messagebox.showinfo("Игра окончена", "сокет зыкрылся")
                    root.quit()
                    exit()
        lose = 0
    for i in range(3):
        for j in range(3):
            if cells[j][i]['text'] == '0':
                lose += 1
                if lose == 3:
                    messagebox.showinfo("Игра окончена", "Вы проиграли")
                    client_socket.close()
                    # messagebox.showinfo("Игра окончена", "сокет зыкрылся")
                    root.quit()
                    exit()
        lose = 0
    free_cells = 0
    for i in range(3):
        for j in range(3):
            if cells[j][i]['text'] == ' ':
                free_cells+=1
    if free_cells == 0 and (win < 3 or lose < 3):
        messagebox.showinfo("Игра окончена", "Ничья")
       # root.quit()
        client_socket.close()
        root.quit()
        sys.exit()



def receive_data():
    while True:
        data = client_socket.recv(2)
        global q
        if data:
            print(f'Получено от сервера: {data.decode()}')
            ##values = data.split()
            data = str(data.decode())

            r = int(data[0])
            c = int(data[1])
                ###  r, c = map(int, values)
                ##   if len(values) == 2:
            if cells[r][c]['text'] == ' ':
                cells[r][c].config(text='0')
                label.config(text="Ваш ход")
                q = True
                check_win()

# создаем поток для приема данных от сервера
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

def make_move(row, col):
    global q
    print('3')
    data = str(row)+str(col)
    if  data.isdigit():
        # отправляем цифру серверу
        client_socket.sendall(data.encode())
        check_win()
'''
        # читаем цифру от сервера
        data = client_socket.recv(2)
        if data:
            print(f'Получено от сервера: {data.decode()}')
            values = data.split()
            data = str(data.decode())
            r = int(data[0])
            c = int(data[1])
          ###  r, c = map(int, values)
         ##   if len(values) == 2:
            if cells[r][c]['text'] == ' ':
                cells[r][c].config(text='0')
            else:
                print('Ошибка: получено недостаточно значений от сервера', data, data[0], data[1])
'''
# обрабатываем клик по ячейке
def cell_click(row, col):
    global q
    print('1')
    if cells[row][col]['text'] == ' ' and q == True:
        cells[row][col].config(text= 'X')
        label.config(text="Ход соперника")
        q = False
        print('2')
        make_move(row, col)


label.config(text="Ваш ход")
for i in range(3):
    for j in range(3):
        cells[i][j].config(command=lambda row=i, col=j: cell_click(row, col))
root.mainloop()



# закрываем соединение и сокет
