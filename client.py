import socketio

async def main():
    async with socketio.AsyncSimpleClient() as sio:
        await sio.connect('http://127.0.0.1:8000/ws/20', transports=['websocket'])
        print('my transport is ', sio.transport)


if __name__ == '__main__':
    await main()