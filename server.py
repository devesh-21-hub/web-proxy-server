import socket
import threading

BLACKLIST = [
    "www.bad-site.com",
    "www.another-bad-site.com"
]

def handle_request(client_socket, client_address):
    # Receive the request from the client
    request = client_socket.recv(4096)

    # Parse the request to get the requested URL
    lines = request.split(b'\n')
    request_line = lines[0]
    words = request_line.split()
    if len(words) < 3:
        return
    method, url, version = words[:3]
    url = url.decode()

    # Check if the requested URL is in the blacklist
    for blacklisted_url in BLACKLIST:
        if blacklisted_url in url:
            # If it is, send a "Forbidden" response to the client
            response = "HTTP/1.0 403 Forbidden\n\n"
            client_socket.send(response.encode())
            client_socket.close()
            return

    # If the requested URL is not in the blacklist, send the request to the
    # server and get the response
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(("www.example.com", 80))
    server_socket.send(request)
    response = server_socket.recv(4096)

    # Send the response back to the client
    client_socket.send(response)
    client_socket.close()

def run_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a local address
    server_socket.bind(("localhost", 8000))

    # Start listening for incoming connections
    server_socket.listen()
    print("Listening on port 8000")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()

        # Handle the request in a separate thread
        t = threading.Thread(target=handle_request, args=(client_socket, client_address))
        t.start()

if __name__ == "__main__":
    run_server()
