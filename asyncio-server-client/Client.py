import asyncio
import json


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.name = None
        self.writer = None
        self.reader = None

    async def set_Client_name(self):
        self.name = input("Enter your Name: ")

    async def get_Client_name(self):
        return self.name

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"Connected to server {self.host}:{self.port}")

            await self.send_name()
            await self.send_messages()

        except (ConnectionRefusedError, asyncio.TimeoutError):
            print("Failed to connect to the server.")
            return

    async def send_name(self):
        message = json.dumps({'name': self.name})
        self.writer.write(message.encode('utf-8'))
        await self.writer.drain()

    async def send_messages(self, writer):
        try:
            while True:
                message = input(f"You: ")
                if message.lower() == 'exit':
                    break

                self.writer.write(message.encode('utf-8'))
                await self.writer.drain()

        except asyncio.CancelledError:
            pass

        finally:
            print("Connection closed.")
            writer.close()
            await writer.wait_closed()

    async def Close_session(self):
        self.writer.write("exit")


host = input("Enter server IP: ")
port = input("Enter server port: ")

client = Client(host, port)
loop = asyncio.get_event_loop()
loop.close()
print(loop.is_closed())
try:
    if not loop.is_closed():
        loop.run_until_complete(client.connect())
except KeyboardInterrupt:
    pass
finally:
    loop.close()

