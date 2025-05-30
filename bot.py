

import asyncio
from synthesizer import Synthesizer
from recognizer import Recognizer
from intent_classifier import IntentClassifier
from language_model import LanguageModel
import json

async def main():
    """Основная функция программы."""

    with open('keys.json', 'r', encoding='utf-8') as file:
        keys = json.load(file)
    proxy_api_openai = keys['proxy_api_openai']
    api_yandex = keys['api_yandex']


    model_path = '/Users/oadanilin/local/VA_RASA/project_with_rasa/models/nlu-20250530-214024-blaring-stack.tar.gz'
    json_path = 'knowledge_base.json'
    prompt_path = 'prompt.txt'

    synth_model = Synthesizer(api_yandex)
    rec_model = Recognizer(proxy_api_openai)
    classifier = IntentClassifier(model_path, json_path)
    lang_model = LanguageModel(proxy_api_openai, prompt_path, 10)
   

    # Константы для записи аудио
    THRESHOLD = 0.01
    SILENCE_DURATION = 1  # продолжительность тишины до остановки записи (в секундах)
    SAMPLERATE = 44100
    CHANNELS = 1

    try:
        # print("Голосовой ассистент запущен.")
        
        # Приветственное сообщение
        welcome_message = "Привет! Я голосовой ассистент Банка Икс. Чем могу помочь?"
        # print(f"Ассистент: {welcome_message}")
        synth_model.synthesize(welcome_message)
        
        # Первое сообщение ассистента в истории
        lang_model.append_to_history("assistant", welcome_message)
        need_to_listen = True
        
        while True:
            if need_to_listen:
                user_msg = rec_model.listen()
                # print(f"Вы сказали: {user_msg}")
            else:
                need_to_listen = True

            # Проверка на команду выхода
            if user_msg.lower() in [""]:
                if not turn_off:
                    turn_off = True
                    goodbye_message = "Подскажите, вы еще со мной?."
                    # print(f"Ассистент: {goodbye_message}")
                    synth_model.check()
                    continue
                else: 
                    break
                

            turn_off = False
            # Добавление сообщения пользователя в историю

            add = await classifier.get_info(user_msg)

            if add == "OPERATOR":
                synth_model.to_operator()
                break
            elif add == "END":
                synth_model.goodbye()
                break
            
    
            # Получение ответа от модели с системным промптом
            answer_from_ai = lang_model.get_answer(user_msg + add)

            # print(f"Ассистент: {answer_from_ai}")
            # Синтез и воспроизведение ответа
            synth_model.synthesize(answer_from_ai)

            
            while add:
                user_msg = rec_model.listen()
                # print(f"Вы сказали: {user_msg}")

                # Проверка на команду выхода
                if user_msg.lower() in [""]:
                    if not turn_off:
                        turn_off = True
                        goodbye_message = "Подскажите, вы еще со мной?."
                        # print(f"Ассистент: {goodbye_message}")
                        synth_model.check()
                        continue
                    else:
                        answer_from_ai = "OUT"    
                        break
                turn_off = False
                
                answer_from_ai = lang_model.get_answer(user_msg)
                print(answer_from_ai)
                if answer_from_ai in {'END', 'CHANGE', 'OPERATOR'}:
                    if answer_from_ai == 'CHANGE':
                        need_to_listen = False
                        synth_model.to_operator()
                    elif answer_from_ai == 'END':
                        synth_model.goodbye()
                        evaluation = lang_model.evaluate()
                        synth_model.synthesize(evaluation)
                        return
                    break
                # Получение ответа от модели с системным промптом
            
                # print(f"Ассистент: {answer_from_ai}")

                # Синтез и воспроизведение ответа
                synth_model.synthesize(answer_from_ai)
        

            if answer_from_ai == 'END':
                synth_model.goodbye()
                evaluation = lang_model.evaluate()
                synth_model.synthesize(evaluation)
                break
            elif answer_from_ai == 'OPERATOR':
                synth_model.to_operator()
                evaluation = lang_model.evaluate()
                synth_model.synthesize(evaluation)
                break
            elif answer_from_ai == "OUT":
                evaluation = lang_model.evaluate()
                synth_model.synthesize(evaluation)
                break
        
        

    
    except KeyboardInterrupt:
        # print("\nПрограмма прервана пользователем.")
        
        # Прощальное сообщение при прерывании
        goodbye_message = "Окей, закрываюсь. Пока!"
        # print(f"Ассистент: {goodbye_message}")
        synth_model.synthesize(goodbye_message)
    
    

if __name__ == "__main__":
    asyncio.run(main())





