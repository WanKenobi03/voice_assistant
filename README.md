# Проектирование и реализация голосового помощника в банке

В рамках дипломной работы был реализован прототип голосового помощника для использования в банковской сфере. Прототип состоит из трех основных составляющих:

## Составляющие Прототипа

1. **Распознаватель речи**: 
   - Файл: `recognizer.py`
   - Осуществляет распознавание речи, используя [Whisper от OpenAI](https://openai.com/index/whisper/).

2. **Генератор речи**:
   - Файл: `synthesizer.py`
   - Генерирует речь на основе [Yandex Speech Kit](https://yandex.cloud/ru/docs/speechkit/).

3. **Диалоговый менеджер**:
   - Объединяет в себе классификатор намерений и языковую модель.
   - **Классификатор намерений**:
     - Файл: `intent_classifier.py`
     - Работает на базе обученной модели из фреймворка RASA. Использует мини-трансформер DIET, подробности можно найти в [блоге RASA](https://rasa.com/blog/introducing-dual-intent-and-entity-transformer-diet-state-of-the-art-performance-on-a-lightweight-architecture/).
   - **Языковая модель**:
     - Файл: `language_model.py`
     - Базируется на [GPT-4.1-nano](https://openai.com/index/gpt-4-1/), супермощной и быстрой языковой модели от OpenAI.

Основная логика диалога сосредоточена в файле `bot.py`.

## Установка

1. Убедитесь, что у вас установлена версия Python <= 3.10.
2. Установите все ключевые зависимости из файла `requirements.txt`:

   ```bash
   pip install -r requirements.txt

## Видеовизитка
В качестве демонстрации работы прототипа предлагается посмотреть короткое [видео](https://drive.google.com/drive/folders/15qvbHR7ujIeWmxH_ENl8Sg1VOP3g1uXt?usp=sharing) 