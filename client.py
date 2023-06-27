import socket
import sys
import threading
import tkinter as tk
from tkinter import messagebox
order_of_priority = True
win = 0
lose = 0

root = tk.Tk()
root.title("Крестики-нолики")

board_frame = tk.Frame(root, padx=40, pady=40, bg="#B38DF9")
board_frame.pack()

label_frame = tk.Frame(root, bg="#ffffff")
label_frame.pack(side="top", fill="x")
label = tk.Label(label_frame, text=" ", font=("Arial", 16), bg="#ffffff")
label.pack(pady=10)

cells = []
for i in range(3):
    row = []
    for j in range(3):
        cell = tk.Button(board_frame, text=" ", font=("Arial", 20), width=4, height=2)
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
client_socket.connect(server_address)

def client_win():
    messagebox.showinfo("Игра окончена", "Вы выиграли")
    client_socket.close()
    root.quit()
    exit()

def client_lose():
    messagebox.showinfo("Игра окончена", "Вы проиграли")
    client_socket.close()
    root.quit()
    exit()

def check_win():
    global win
    global lose
    win  = 0
    lose = 0
    for i in range(3):
        if (cells[i][i]['text']=='X'):
            win +=1
        if (cells[i][i]['text']=='0'):
            lose +=1
    if  win == 3:
        client_win()
    if  lose == 3:
        client_lose()
    win = 0
    lose = 0
    for i in range(3):
        if (cells[i][2 - i]['text'] == 'X'):
            win += 1
        if (cells[i][2 - i]['text'] == '0'):
            lose += 1
    if win == 3:
        client_win()
    if lose == 3:
        client_lose()
    win = 0
    lose = 0
    for i in range(3):
        for j in range(3):
            if cells[i][j]['text']=='X':
                win +=1
                if win == 3:
                  client_win()
            if cells[i][j]['text'] == '0':
                lose += 1
                if lose == 3:
                    client_lose()
        win = 0
        lose = 0
    for i in range(3):
        for j in range(3):
            if cells[j][i]['text'] == 'X':
                win += 1
                if win == 3:
                    client_win()
            if cells[j][i]['text'] == '0':
                lose += 1
                if lose == 3:
                    client_lose()
        lose = 0
        win = 0
    free_cells = 0
    for i in range(3):
        for j in range(3):
            if cells[j][i]['text'] == ' ':
                free_cells+=1
    if free_cells == 0:
        messagebox.showinfo("Игра окончена", "Ничья")
        client_socket.close()
        root.quit()
        sys.exit()

def receive_data():
    while True:
        data = client_socket.recv(2)
        global order_of_priority
        if data:
            data = str(data.decode())
            r = int(data[0])
            c = int(data[1])
            if cells[r][c]['text'] == ' ':
                cells[r][c].config(text='0')
                label.config(text="Ваш ход")
                order_of_priority = True
                check_win()

receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

def make_move(row, col):
    global order_of_priority
    data = str(row)+str(col)
    if  data.isdigit():
        client_socket.sendall(data.encode())
        check_win()

def cell_click(row, col):
    global order_of_priority
    if cells[row][col]['text'] == ' ' and order_of_priority == True:
        cells[row][col].config(text= 'X')
        label.config(text="Ход соперника")
        order_of_priority = False
        make_move(row, col)


label.config(text="Успей сходить первым")
for i in range(3):
    for j in range(3):
        cells[i][j].config(command=lambda row=i, col=j: cell_click(row, col))
root.mainloop()
