import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# 1. Load environment variables
load_dotenv()

# 2. Initialize the Google GenAI Client
# Automatically picks up GEMINI_API_KEY from environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Initialize chat session with the target model
chat = client.chats.create(model="gemini-2.5-flash")

def send_chat_message(user_input, max_retries=3):
    """Sends a message to the chat session with exponential backoff retry for transient errors."""
    for attempt in range(max_retries):
        try:
            response = chat.send_message(user_input)
            return response.text
        except APIError as e:
            # Handle 503 Service Unavailable or transient rate limits
            if e.code == 503 or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt  # Wait 1s, 2s, 4s
                    print(f"Server busy (503). Retrying in {sleep_time}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue
            print(f"API Error: {e}")
            return "The server is currently busy or encountered an error. Please try again shortly."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return "An unexpected error occurred. Please try again."

# Test the connection
if __name__ == "__main__":
    print("Testing Gemini Connection...")
    reply = send_chat_message("Hello, are you connected?")
    print("\nAPI Response:")
    print(reply)