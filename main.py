import os
import socket

# Set the directory that contains your static files
# Replace '/path/to/directory' with the actual path to your directory
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Set the port number
PORT = 8000


def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(request)
    # Extract the requested file path from the request
    try:
        # Extracting the path from the HTTP request
        path = request.split(' ')[1]
        # Checking if it's the root path and serving index.html
        if path == '/':
            file_path = os.path.join(DIRECTORY, 'index.html')
        else:
            file_path = os.path.join(DIRECTORY, path[1:])

        # Check if the requested file exists
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response_content = file.read()
                response = "HTTP/1.1 200 OK\nContent-Length: {}\n\n".format(len(response_content)).encode(
                    'utf-8') + response_content
        else:
            response = b"HTTP/1.1 404 Not Found\n\n404 Not Found"

        # Send the response back to the client
        client_socket.sendall(response)
    except Exception as e:
        print("Error handling request:", e)

    # Close the client socket
    client_socket.close()


# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(('localhost', PORT))

# Listen for incoming connections
server_socket.listen(5)

print(f"Serving at port {PORT}")

try:
    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Handle the request from the client
        handle_request(client_socket)
finally:
    # Close the server socket
    server_socket.close()
