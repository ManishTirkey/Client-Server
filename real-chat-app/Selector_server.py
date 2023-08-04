import socket
import selectors
import json


class MultiClientServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.clients = {}  # Dictionary to store the IP mapping
        self.is_listening = True

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while self.is_listening:
                events = self.selector.select()
                for key, _ in events:
                    if key.data is None:  # New connection
                        self.accept_connection(key.fileobj)
                    else:  # Incoming data from existing client
                        self.receive_data(key.fileobj)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_listening = False
        self.selector.close()

    def accept_connection(self, server_socket):
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")
        client_socket.setblocking(False)
        self.selector.register(client_socket, selectors.EVENT_READ, data={})

    def receive_data(self, client_socket):
        try:
            data = client_socket.recv(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                if 'name' in message:
                    self.add_client_mapping(message['name'], client_socket.getpeername()[0])
                print(f"Message from {self.get_client_name(client_socket)}: {message['msg']}")
            else:
                self.remove_client(client_socket)

        except (socket.error, json.JSONDecodeError):
            self.remove_client(client_socket)

    def get_client_name(self, client_socket):
        ip_address = client_socket.getpeername()[0]
        return self.clients.get(ip_address, "Unknown")

    def add_client_mapping(self, name, ip_address):
        self.clients[ip_address] = name

    def remove_client(self, client_socket):
        ip_address = client_socket.getpeername()[0]
        if ip_address in self.clients:
            print(f"Connection closed with {self.get_client_name(client_socket)} ({ip_address})")
            self.selector.unregister(client_socket)
            client_socket.close()
            del self.clients[ip_address]


if __name__ == "__main__":
    server = MultiClientServer('0.0.0.0', 12345)  # Replace with your desired IP and port
    server.start()
