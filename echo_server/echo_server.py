import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 3005))
server_socket.listen()

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')

    request = client_socket.recv(1024).decode()
    if (not request) or ('favicon.ico' in request):
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    http_method, path_basep, version = request_line.split(' ')
    if '?' in path_basep:
        path, basep = path_basep.split('?')
        basep = basep.split('&')

        params = {}
        for param in basep:
            key, value = param.split('=')
            params[key] = value
    else:
        path = path_basep
        params = {}
    
    number = int(params.get('number', 0))

    response_body = (f'''
<html>
    <head>
        <title>Dice Rolls</title>
    </head>
    <body>
        <h1>HTTP Request Information:</h1>
        <p><strong>Request Line:</strong> {request_line}</p>
        <p><strong>HTTP Method:</strong> {http_method}</p>
        <p><strong>Path:</strong> {path}</p>
        <p><strong>Parameters:</strong> {params}</p>
        <h2>Counter:</h2>
        <p style="color: red;">The current number is: {number}
        <a href="?number={number + 1}">Add one</a>
        &nbsp;&nbsp
        <a href='?number={number - 1}'>Subtract one</a>
    </body>
</html>
'''
                    )

    response = ('HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html\r\n'
                f'Content-Length: {len(response_body)}\r\n'
                '\r\n'
                f'{response_body}\n')
    
    client_socket.sendall(response.encode())
    client_socket.close()

print("Server is running on localhost:3003")