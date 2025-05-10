from openai import OpenAI




class LanguageModel:
    def __init__(self, PROXY_API_KEY, prompt_path, window_size):
        self.window_size = window_size
        self.client = OpenAI(api_key=PROXY_API_KEY, base_url="https://api.proxyapi.ru/openai/v1")
        self.total_cost = 0
        self.history = []

        with open (prompt_path, 'r', encoding='utf-8') as file:
            self.SYSTEM_PROMPT = file.read()

        
    
    def mini_chat(self, messages):
        chat_completion = self.client.chat.completions.create(max_tokens=1024, model="gpt-4.1-nano", messages=messages)

        input_tokens, output_tokens = chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens
        input_cost, output_cost = 0.0288, 0.1152

        self.total_cost += round((input_tokens / 1000 * input_cost + output_tokens / 1000 * output_cost), 2)

        return chat_completion.choices[0].message.content
          
    
    def create_msg(self, role, text):
        """Создает сообщение в формате для OpenAI API."""
        return {"role": role, "content": [{"type": "text", "text": text}]}
    
    def get_answer(self, user_msg):
        """
        Функция для общения с моделью, использующая скользящее окно для истории.
    
        Parameters:
        messages (list): История сообщений
        window_size (int): Размер окна (количество пар вопрос-ответ)
    
        Returns:
        tuple: (ответ модели, стоимость)
        """
        self.append_to_history("user", user_msg)

        # Берем только последние сообщения (размер окна * 2 - для пар вопрос-ответ)
        recent_messages = self.history[-self.window_size*2:] if len(self.history) > self.window_size*2 else self.history
    
        # Добавляем системный промпт
        messages_with_system = [self.create_msg("system", self.SYSTEM_PROMPT)] + recent_messages

        answer = self.mini_chat(messages=messages_with_system)

        self.append_to_history('assistant', answer)
    
        return answer
    
    def append_to_history(self, role, msg):
        self.history.append(self.create_msg(role, msg))

    def evaluate(self):

        messages_with_system = [self.create_msg("system", 'Проанализируй весь диалог и предположи и оцени какую бы оценку диалога выдал клиента, 5 - очень хорошо, 1 - очень плохо')] + self.history
        answer = self.mini_chat(messages=messages_with_system)
        return answer