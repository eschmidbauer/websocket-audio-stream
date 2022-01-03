#!/usr/bin/env python3
import asyncio
import websockets
import numpy as np
import scipy.io.wavfile

sr = 8000
encode_float = True

async def audio_stream(websocket, path):
    sound = np.array([], dtype=np.int16)
    if encode_float == True:
        sound = np.array([], dtype=np.float32)

    print(f"starting recording")
    while True:
        try:

            message = await websocket.recv()
            if isinstance(message, str):
                continue

            audio = np.frombuffer(message, dtype=np.int16)
            if encode_float == True:
                audio = audio.astype(np.float32)/32767.0

            sound = np.append(sound, audio)

        except websockets.ConnectionClosed:
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
