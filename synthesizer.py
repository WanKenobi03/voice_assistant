from speechkit import model_repository, configure_credentials, creds
import tempfile
import os
import soundfile as sf
import sounddevice as sd


class Synthesizer:
    def __init__(self, API_KEY):
        # Аутентификация через API-ключ.
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=API_KEY
            )
        )
        self.model_synthes = model_repository.synthesis_model()
        self.model_synthes.voice = 'alexander'
        self.model_synthes.role = 'good'
        self.model_synthes.speed = 1.1
    
    def say(self, file_path):
        try:
            # Проверяем, создан ли файл
            if not os.path.exists(file_path):
                
                return
                # Загружаем и воспроизводим аудио

            print('AI говорит:')
            data, samplerate = sf.read(file_path, dtype='float32')
            sd.play(data, samplerate)
            sd.wait()  # Ждем окончания воспроизведения
        
        except Exception as e:
            print(f"Ошибка при синтезе или воспроизведении речи: {e}")
    
        finally:
            # Очистка: удаляем временный файл после воспроизведения
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении временного файла: {e}")


    def synthesize(self, text):
        result = self.model_synthes.synthesize(text)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        temp_file_path = temp_file.name

        result.export(temp_file_path, 'wav')

        self.say(file_path=temp_file_path)

    def hello(self):
        self.synthesize("Привет! Я голосовой ассистент Банка Икс. Чем могу помочь?")

    def goodbye(self):
        self.synthesize("До свидания и хорошего вам дня!")
    
    def to_operator(self):
        self.synthesize("Переключаю вас на оператора, это может занять некторое время, оставайтесь на линии.")

    def change(self):
        self.synthesize("Я уже обрабатываю ваш запрос, оставайтесь на линии")

    def check(self):
        self.synthesize("Подскажите, вы еще со мной?")

    
    




