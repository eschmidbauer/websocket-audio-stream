#!/usr/bin/env python3
import asyncio
import websockets
import numpy
import pyaudio

p = pyaudio.PyAudio()

async def audio_stream(websocket, path):
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=8000,
                    output=True)
    while True:
        try:
            message = await websocket.recv()
            if isinstance(message, str):
                continue

            audio = numpy.frombuffer(message, numpy.int8)
            stream.write(audio)

        except websockets.ConnectionClosed:
            stream.stop_stream()
            stream.close()
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
    p.terminate()
