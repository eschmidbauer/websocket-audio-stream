#!/usr/bin/env python3
import asyncio
import websockets
import numpy as np
import scipy.io.wavfile

sr = 8000

async def audio_stream(websocket, path):
    frames = []

    while True:
        try:

            message = await websocket.recv()
            if isinstance(message, str):
                continue

            audio = np.frombuffer(message, dtype=np.int16)
            frames.append(audio)

        except websockets.ConnectionClosed:
            sound = np.hstack(frames)
            l = sound.shape[0] / sr
            print(f"length {l}")
            scipy.io.wavfile.write("mysound.wav", sr, sound)

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
