import socket

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    message = input("Введіть текст для відправлення на сервер (або 'exit' для закриття): ")

    client_socket.send(message.encode('utf-8'))

    if message.lower() == 'exit':
        break  

response = client_socket.recv(1024).decode('utf-8')
print(response)

client_socket.close()
