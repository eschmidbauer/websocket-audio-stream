#!/usr/bin/env python3
import asyncio
import websockets
import numpy as np
import wave

async def audio_stream(websocket, path):

    wavefile = wave.open("mysound.wav", 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(8000)

    while True:
        try:

            message = await websocket.recv()
            if isinstance(message, str):
                continue

            audio = np.frombuffer(message, dtype=np.uint8)
            wavefile.writeframes(audio)


        except websockets.ConnectionClosed:
            wavefile.close()
            break


def start():
    loop = asyncio.get_event_loop()

    listen_addr = "0.0.0.0"
    listen_port = 2700

    start_server = websockets.serve(
        audio_stream, listen_addr, listen_port)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    start()
