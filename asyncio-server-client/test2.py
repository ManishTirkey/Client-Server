import asyncio
import json


class Client:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name

    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print(f"Connected to server {self.host}:{self.port}")

            await self.send_name(writer)
            await self.send_messages(writer)

        except (ConnectionRefusedError, asyncio.TimeoutError):
            print("Failed to connect to the server.")
            return

    async def send_name(self, writer):
        message = json.dumps({'name': self.name})
        writer.write(message.encode('utf-8'))
        await writer.drain()

    async def send_messages(self, writer):
        try:
            while True:
                message = input(f"{self.name}: ")
                if message.lower() == 'exit':
                    break

                writer.write(message.encode('utf-8'))
                await writer.drain()

        except asyncio.CancelledError:
            pass

        finally:
            print("Connection closed.")
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    name = input("Enter your name: ")
    client = Client('192.168.94.190', 12345, name)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
