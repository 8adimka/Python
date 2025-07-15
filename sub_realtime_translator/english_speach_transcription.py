import asyncio
import json
import os
import queue
import sys

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from websockets.client import connect as websocket_connect

# for i, d in enumerate(sd.query_devices()):
#     print(
#         f"{i}: {d['name']} — {d['max_input_channels']} in, {d['max_output_channels']} out"
#     )


load_dotenv()

# Конфигурация
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_CHUNK_MS = 200  # Размер аудиочанка в миллисекундах


class AudioRecorder:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stream = None
        self.chunk_size = int(SAMPLE_RATE * AUDIO_CHUNK_MS / 1000)

    def start(self):
        def callback(indata, frames, time, status):
            self.audio_queue.put(indata.copy())

        self.stream = sd.InputStream(
            device=14,  # 👈 ключевая строка, 14 или 15е устройство - микрофон
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=callback,
            dtype="float32",
            blocksize=self.chunk_size,
        )
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

    async def get_audio_chunk(self):
        while True:
            try:
                chunk = self.audio_queue.get_nowait()
                return chunk
            except queue.Empty:
                await asyncio.sleep(0.001)


class RealTimeSubtitles:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.session_active = False
        self.websocket = None
        self.last_interim_len = 0

    def clear_last_line(self):
        """Очищает предыдущую строку вывода"""
        sys.stdout.write("\r" + " " * self.last_interim_len + "\r")
        sys.stdout.flush()

    def print_interim(self, text):
        """Печатает промежуточный текст, затирая старый"""
        self.clear_last_line()
        sys.stdout.write(text)
        sys.stdout.flush()
        self.last_interim_len = len(text)

    def print_final(self, text):
        """Очищает промежуточный, печатает финальный результат"""
        self.clear_last_line()
        print(text)
        self.last_interim_len = 0

    async def process_audio_stream(self):
        """Основной цикл обработки аудио"""
        while self.session_active:
            try:
                async with websocket_connect(
                    "wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1&model=nova-2&language=en&punctuate=true&interim_results=true&endpointing=300",
                    extra_headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
                    ping_interval=None,
                ) as ws:
                    sys.stdout.write("\033[2J\033[H")
                    print("Deepgram connection established")
                    self.websocket = ws

                    # Задача для получения результатов
                    receive_task = asyncio.create_task(self.receive_results(ws))

                    # Отправка аудио
                    while self.session_active:
                        chunk = await self.recorder.get_audio_chunk()
                        if chunk is not None:
                            # Конвертируем в 16-bit PCM
                            audio_data = (chunk * 32767).astype(np.int16).tobytes()
                            try:
                                await ws.send(audio_data)
                            except Exception as e:
                                print(f"Send error: {e}")
                                break
                        await asyncio.sleep(0.001)

                    receive_task.cancel()
                    await ws.send(json.dumps({"type": "CloseStream"}))
            except Exception as e:
                print(f"Connection error: {e}")
                await asyncio.sleep(1)  # Переподключение через 1 секунду

    async def receive_results(self, ws):
        """Обработка результатов от Deepgram"""
        while self.session_active:
            try:
                result = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(result)

                if "channel" in data:
                    transcript = data["channel"]["alternatives"][0]["transcript"]
                    if not transcript.strip():
                        continue  # игнор пустых промежуточных

                    if data.get("is_final", False):
                        self.print_final(transcript)
                    else:
                        self.print_interim(transcript)

            except asyncio.TimeoutError:
                print("Timeout waiting for Deepgram response")
                break
            except Exception as e:
                print(f"Receive error: {e}")
                break

    def run(self):

        self.session_active = True
        self.recorder.start()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self.process_audio_stream())
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
            loop.close()

    def stop(self):
        self.session_active = False
        self.recorder.stop()


if __name__ == "__main__":
    translator = RealTimeSubtitles()
    try:
        translator.run()
    except KeyboardInterrupt:
        translator.stop()
