from openai import OpenAI
import numpy as np
import queue
import sounddevice as sd
import time

import tempfile
import os
from scipy.io.wavfile import write

class Recognizer:

   def __init__(self, PROXY_API_KEY):
      self.client = OpenAI(api_key=PROXY_API_KEY, base_url="https://api.proxyapi.ru/openai/v1")
      self.THRESHOLD = 0.01
      self.SILENCE_DURATION = 1  # продолжительность тишины до остановки записи (в секундах)
      self.SAMPLERATE = 44100
      self.CHANNELS = 1
      self.MIN_SPEECH_DURATION = 0.3

      self.audio_queue = queue.Queue()
   
   # Функция обратного вызова для записи аудио
   def audio_callback(self, indata, frames, time, status):
      if status:
         print(status)
      self.audio_queue.put(indata.copy())

   # Функция проверки тишины
   def is_silent(self, data, threshold):
      return np.max(np.abs(data)) < threshold

   def listen(self):
      # Настройки записи
      
      recorded_frames = []
      

      with sd.InputStream(samplerate=self.SAMPLERATE, channels=self.CHANNELS, callback=self.audio_callback):
         non_silence_detected = False
         non_silence_duration = 0
         silence_start_time = time.time()
        
         while True:
            data = self.audio_queue.get()
            recorded_frames.append(data)
            
            if not self.is_silent(data, self.THRESHOLD):
                non_silence_detected = True
                silence_start_time = time.time()
                non_silence_duration += len(data) / self.SAMPLERATE
            else:
                if time.time() - silence_start_time > self.SILENCE_DURATION:
                    
                    break
      
      if not non_silence_detected or non_silence_duration < self.MIN_SPEECH_DURATION:
         return ""  # Возвращаем пустую строку, чтобы показать, что речь не была обнаружена
      
      # Конкатенация всех записанных фреймов
      recorded_audio = np.concatenate(recorded_frames, axis=0)
    
      # Создаем временный файл для записи аудио
      temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
      temp_file.close()
      temp_file_path = temp_file.name
    
      try:
         # Сохранение в файл
         write(temp_file_path, self.SAMPLERATE, recorded_audio)

         # Транскрипция
         with open(temp_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(model="whisper-1", file=audio_file)

         return transcript.text
    
      finally:
         # Очистка: удаляем временный файл после обработки
         if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
         
         with self.audio_queue.mutex:
            self.audio_queue.queue.clear()
         
      