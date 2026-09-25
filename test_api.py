import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Configure the API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 2. Use gemini-2.5-flash to avoid high demand bottlenecks
model = genai.GenerativeModel("gemini-2.5-flash")

# 3. Create a chat instance (fixes the AFC warning)
chat = model.start_chat(history=[])

def send_chat_message(user_input):
    try:
        # Use send_message instead of generate_content
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        return "The server is currently busy. Please try again shortly."

# Test the connection
if __name__ == "__main__":
    print("Testing Gemini Connection...")
    reply = send_chat_message("Hello, are you connected?")
    print("API Response:")
    print(reply)