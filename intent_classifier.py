from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
import json

class IntentClassifier:
    def __init__(self, model_path, json_path):
        """
        Инициализация классификатора интентов.
        
        Args:
            model_path (str): Путь к файлу модели Rasa.
        """
        self.model_path = model_path
        self.agent = Agent.load(self.model_path)

        with open(json_path, 'r', encoding='utf-8') as file:
            self.knowledge_base = json.load(file)
    
    
    async def predict(self, text):
        """
        Предсказание интента для входного текста.
        
        Args:
            text (str): Текст для классификации.
            
        Returns:
            tuple: (intent_name, confidence) - название интента и уверенность.
        """
        
        # Получение предсказания
        result = await self.agent.parse_message(text)
        
        # Извлечение результата
        intent = result.get("intent", {}).get("name")
        confidence = result.get("intent", {}).get("confidence")
        
        return intent, confidence
    
    async def get_info(self, text):
        intent, confidence = await self.predict(text)

        if intent not in self.knowledge_base:
            return ""
        
        return "SYSTEM_ADD: " + self.knowledge_base[intent]
    


    






