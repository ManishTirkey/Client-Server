import asyncio
import json


class MultiClientServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store the IP mapping
        self.is_listening = True

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client,
            host=self.host,
            port=self.port
        )

        print(f"Server listening on {self.host}:{self.port}")

        try:
            async with server:
                await server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_listening = False

    async def handle_client(self, reader, writer):
        client_address = writer.get_extra_info('peername')
        print(f"New connection from {client_address[0]}:{client_address[1]}")
        name = await self.receive_name(reader)
        self.add_client_mapping(name, client_address[0])

        try:
            while self.is_listening:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"{name}: {message}")

        except (asyncio.CancelledError, ConnectionResetError):
            pass

        finally:
            print(f"Connection closed with {name} ({client_address[0]})")
            self.remove_client_mapping(client_address[0])
            writer.close()
            await writer.wait_closed()

    async def receive_name(self, reader):
        data = await reader.read(1024)
        message = json.loads(data.decode('utf-8'))
        return message['name'] if 'name' in message else "Unknown"

    def add_client_mapping(self, name, ip_address):
        self.clients[ip_address] = name

    def remove_client_mapping(self, ip_address):
        if ip_address in self.clients:
            del self.clients[ip_address]


if __name__ == "__main__":

    server = MultiClientServer('192.168.149.190', 65432)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(server.start())
    except KeyboardInterrupt:
        server.stop()
    finally:
        loop.close()
