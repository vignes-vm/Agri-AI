# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Flask Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))

    # --- FIX: Change the model name ---
    MODEL_NAME ="models/gemini-pro-latest" # Use this reliable model instead of 1.5-flash

    # Chatbot Config
    MAX_TOKENS = 500
    TEMPERATURE = 0.7

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///agriculture.db')

    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in .env file")
        return True