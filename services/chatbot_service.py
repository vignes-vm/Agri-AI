# services/chatbot_service.py
import google.generativeai as genai
from config import Config
from models.agriculture_data import AgricultureData
from services.knowledge_base import AgricultureKnowledgeBase

# Configure the Gemini client
genai.configure(api_key=Config.GOOGLE_API_KEY)

class ChatbotService:
    def __init__(self):
        self.ag_data = AgricultureData()
        self.knowledge_base = AgricultureKnowledgeBase()
        # Initialize the Gemini model using the name from config
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.conversation_history = {}

    # ... (the detect_intent, get_app_data_context, and generate_system_prompt methods do not need to change) ...
    def detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        if any(word in message_lower for word in ['order', 'delivery', 'track', 'status', 'ord']):
            return 'order_query'
        if any(word in message_lower for word in ['crop', 'grow', 'cultivate', 'plant', 'farming']):
            return 'crop_info'
        if any(word in message_lower for word in ['yield', 'production', 'harvest', 'output']):
            return 'yield_query'
        if any(word in message_lower for word in ['pest', 'disease', 'insect', 'bug', 'infection']):
            return 'pest_disease'
        if any(word in message_lower for word in ['soil', 'fertilizer', 'manure', 'compost']):
            return 'soil_fertilizer'
        return 'general_query'

    def get_app_data_context(self, message, intent):
        """Get relevant data from app database"""
        context = ""
        if intent == 'order_query':
            words = message.upper().split()
            for word in words:
                if word.startswith('ORD'):
                    order = self.ag_data.get_order_by_id(word)
                    if order:
                        context += f"\nOrder Information:\n{self.ag_data.format_order_info(order)}"
        elif intent in ['crop_info', 'yield_query', 'pest_disease']:
            for crop_name in self.ag_data.get_all_crops():
                if crop_name.lower() in message.lower():
                    crop = self.ag_data.get_crop_by_name(crop_name)
                    if crop:
                        context += f"\nCrop Data:\n{self.ag_data.format_crop_info(crop)}"
                        break
        kb_info = self.knowledge_base.search_knowledge(message)
        if kb_info:
            context += f"\n\nRelevant Information:\n{kb_info}"
        return context

    def generate_system_prompt(self, intent):
        """Generate system prompt based on intent"""
        base_prompt = self.knowledge_base.get_agriculture_context()
        intent_specific = {
            'order_query': "\nFocus on providing clear order status and delivery information.",
            'crop_info': "\nProvide detailed cultivation steps and requirements.",
            'yield_query': "\nFocus on factors affecting yield and optimization strategies.",
            'pest_disease': "\nProvide pest/disease identification and management solutions.",
            'soil_fertilizer': "\nFocus on soil health and appropriate fertilization methods.",
            'general_query': "\nProvide helpful agriculture guidance."
        }
        return base_prompt + intent_specific.get(intent, intent_specific['general_query'])


    def chat(self, user_id, message):
        """Main chat function"""
        try:
            intent = self.detect_intent(message)
            app_context = self.get_app_data_context(message, intent)

            if user_id not in self.conversation_history:
                system_prompt = self.generate_system_prompt(intent)
                self.conversation_history[user_id] = self.model.start_chat(
                    history=[
                        {'role': 'user', 'parts': [system_prompt]},
                        {'role': 'model', 'parts': ["Yes, I am ready to help. How can I assist you with your farming needs today?"]}
                    ]
                )

            chat_session = self.conversation_history[user_id]
            user_message_with_context = message
            if app_context:
                user_message_with_context += f"\n\n--- Additional Context ---\n{app_context}"

            response = chat_session.send_message(user_message_with_context)
            bot_response = response.text

            return {
                "success": True,
                "response": bot_response,
                "intent": intent
            }

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": "I'm sorry, I encountered an error. Please try again."
            }

    def clear_history(self, user_id):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        return {"success": True, "message": "Conversation history cleared"}