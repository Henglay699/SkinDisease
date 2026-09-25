import traceback
from flask import Blueprint, jsonify, request
from extensions import csrf
from app.services.chatbot_services import get_chat_response

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/chat', methods=['POST'])
@csrf.exempt
def chat():
    user_message = ""
    image_file = None

    # Handle FormData (multipart/form-data for file uploads) or standard JSON payload
    if request.files or request.form:
        user_message = request.form.get("message", "").strip()
        image_file = request.files.get("image")
    else:
        data = request.get_json() or {}
        raw_message = data.get("message", "")
        if isinstance(raw_message, dict):
            user_message = str(raw_message.get("text", "")).strip()
        else:
            user_message = str(raw_message).strip()

    # Ensure at least text or image is provided
    if not user_message and not image_file:
        return jsonify({"error": "Please enter a message or upload an image."}), 400

    try:
        reply = get_chat_response(user_message=user_message, image_file=image_file)
        return jsonify({"reply": reply})
    except Exception as e:
        print("=== CHATBOT API ERROR TRACEBACK ===")
        traceback.print_exc()
        print("===================================")
        
        error_msg = str(e) if str(e) else "An unexpected error occurred."
        return jsonify({"error": f"AI Error: {error_msg}"}), 500