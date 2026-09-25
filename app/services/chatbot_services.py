import io
from PIL import Image
from extensions import gemini_client

# System instructions to strictly restrict AI scope to skin health and dermatology
SKIN_HEALTH_SYSTEM_INSTRUCTION = (
    "You are an AI assistant exclusively for a Skin Disease Diagnosis Platform. "
    "Your ONLY duty is to answer questions and analyze images related to skin health, dermatology, "
    "rashes, lesions, and skin symptoms. "
    "STRICT BOUNDARY: If a user asks about anything unrelated to skin health, skin conditions, or medical dermatology "
    "(such as history, coding, math, general trivia, weather, cooking, general conversation, etc.), politely decline by saying: "
    "'I am specialized only in skin health and dermatology. Please ask me a question related to skin conditions.' "
    "Always clarify that your responses are for informational purposes only and advise users to consult a certified dermatologist."
)

def get_symptom_analysis(symptoms: str) -> str:
    """
    Sends text-based symptoms to Gemini API for diagnostic breakdown and general advice.
    """
    prompt = f"Analyze these skin symptoms and give brief precautions: {symptoms}"
    
    response = gemini_client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={"system_instruction": SKIN_HEALTH_SYSTEM_INSTRUCTION}
    )
    return response.text


def get_chat_response(user_message: str, image_file=None) -> str:
    """
    Processes user messages and optional skin images through Gemini API.
    Enforces strict skin disease domain guardrails.
    """
    contents = []

    # 1. Process uploaded skin image if provided
    if image_file:
        try:
            image_bytes = image_file.read()
            pil_image = Image.open(io.BytesIO(image_bytes))
            contents.append(pil_image)
        except Exception as img_err:
            print(f"Error processing image file: {img_err}")
            return "Error: Could not read the uploaded image. Please upload a valid JPEG or PNG image file."

    # 2. Add text prompt
    text_prompt = user_message.strip() if user_message else "Please analyze this skin image and provide guidance."
    contents.append(text_prompt)

    # 3. Call Gemini API
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents,
            config={"system_instruction": SKIN_HEALTH_SYSTEM_INSTRUCTION}
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise e