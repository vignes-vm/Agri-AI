# check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Attempting to connect to Google AI...")

try:
    # Get the API key from your environment
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("\nERROR: GOOGLE_API_KEY not found in .env file!")
        print("Please make sure your .env file is in the 'agriculture-chatbot' root directory.")
    else:
        # Configure the client library
        genai.configure(api_key=api_key)

        print("Successfully configured. Fetching available models...")
        print("="*30)

        # List all available models
        for m in genai.list_models():
            # Check if the model supports the 'generateContent' method (used for chatbots)
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")

        print("="*30)
        print("\nTest complete. Please use one of the model names listed above in your config.py file.")

except Exception as e:
    print(f"\nAn error occurred: {e}")