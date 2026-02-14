# # Create your views here.
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import JsonResponse
# from gtts import gTTS
# from .models import Chat
# import os
# import logging
# import base64
# import re
# from .rag_service import query_rag
# from django.views.decorators.csrf import csrf_exempt


# logger = logging.getLogger(__name__)

# def clean_tts_text(text):
#     cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
#     cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
#     return cleaned.strip()


# def home(request):
#     return render(request, 'core/index.html')


# @csrf_exempt
# def speak_text(request):
#     if request.method == 'POST':
#         user_text = request.POST.get('speechText', 'You did not say anything!')
#         try:
#             model_response = query_rag(user_text)

#             # Save chat
#             Chat.objects.create(
#                 user_message=f"Aman Patel: {user_text}",
#                 bot_response=model_response,
#             )

#             # Convert to speech
#             language = (request.POST.get('language') or 'en').strip().lower()
#             tts_lang = 'ne' if language == 'ne' else 'en'
#             tts_input = clean_tts_text(model_response)
#             tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

#             voice_file_path = "voice.mp3"
#             tts.save(voice_file_path)

#             with open(voice_file_path, "rb") as f:
#                 audio_bytes = f.read()

#             return JsonResponse(
#                 {
#                     "response_text": model_response,
#                     "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
#                 }
#             )

#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}", status=500)

#     return HttpResponse("Invalid request", status=400)


# Updated views.py for React integration
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import JsonResponse
# from gtts import gTTS
# from .models import Chat
# import os
# import logging
# import base64
# import re
# from .rag_service import query_rag
# from django.views.decorators.csrf import csrf_exempt


# logger = logging.getLogger(__name__)

# def clean_tts_text(text):
#     cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
#     cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
#     return cleaned.strip()


# def home(request):
#     return render(request, 'core/index.html')


# @csrf_exempt
# def speak_text(request):
#     """Original view - keep for backward compatibility"""
#     if request.method == 'POST':
#         user_text = request.POST.get('speechText', 'You did not say anything!')
#         try:
#             model_response = query_rag(user_text)

#             # Save chat
#             Chat.objects.create(
#                 user_message=f"Aman Patel: {user_text}",
#                 bot_response=model_response,
#             )

#             # Convert to speech
#             language = (request.POST.get('language') or 'en').strip().lower()
#             tts_lang = 'ne' if language == 'ne' else 'en'
#             tts_input = clean_tts_text(model_response)
#             tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

#             voice_file_path = "voice.mp3"
#             tts.save(voice_file_path)

#             with open(voice_file_path, "rb") as f:
#                 audio_bytes = f.read()

#             return JsonResponse(
#                 {
#                     "response_text": model_response,
#                     "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
#                 }
#             )

#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}", status=500)

#     return HttpResponse("Invalid request", status=400)


# @csrf_exempt
# def chat_api(request):
#     """
#     New API endpoint for React frontend
#     Accepts JSON with 'text' field
#     Returns JSON with 'text' and 'audio_base64' fields
#     """
#     if request.method == 'POST':
#         try:
#             # Parse JSON body
#             import json
#             data = json.loads(request.body)
#             user_text = data.get('text', '').strip()
            
#             if not user_text:
#                 return JsonResponse({'error': 'No text provided'}, status=400)
            
#             # Get optional language parameter (default to 'en')
#             language = data.get('language', 'en').strip().lower()
            
#             # Query RAG model
#             model_response = query_rag(user_text)

#             # Save chat to database
#             Chat.objects.create(
#                 user_message=f"User: {user_text}",
#                 bot_response=model_response,
#             )

#             # Convert to speech
#             tts_lang = 'ne' if language == 'ne' else 'en'
#             tts_input = clean_tts_text(model_response)
#             tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

#             # Save to temporary file
#             voice_file_path = "voice.mp3"
#             tts.save(voice_file_path)

#             # Read audio file and encode to base64
#             with open(voice_file_path, "rb") as f:
#                 audio_bytes = f.read()
            
#             # Clean up the temporary file
#             if os.path.exists(voice_file_path):
#                 os.remove(voice_file_path)

#             # Return JSON response
#             return JsonResponse({
#                 'text': model_response,
#                 'audio_base64': base64.b64encode(audio_bytes).decode("utf-8"),
#             })

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             logger.error(f"Error in chat_api: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from gtts import gTTS
# from .models import Chat
# import os
# import logging
# import base64
# import re
# import json

# # ===== LOAD .env FILE - ADD THIS SECTION =====
# from dotenv import load_dotenv
# import pathlib

# # Get the project root directory (where manage.py is)
# BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
# env_path = BASE_DIR / '.env'
# env_admin_key = getattr(settings,"ADMIN_API_KEY","")
# # Load .env file
# load_dotenv(dotenv_path=env_path)

# # Verify it loaded (you'll see this when Django starts)
# print("=" * 60)
# print("🔍 Loading .env file...")
# print(f"📁 .env path: {env_path}")
# print(f"✅ .env exists: {env_path.exists()}")
# print(f"🔑 ADMIN_API_KEY: '{os.getenv('ADMIN_API_KEY')}'")
# print("=" * 60)
# # ===== END .env LOADING =====

# from .rag_service import RAGService

# logger = logging.getLogger(__name__)
# rag_service = RAGService()


# def clean_tts_text(text):
#     """Remove markdown formatting for TTS"""
#     cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
#     cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
#     return cleaned.strip()


# def identify_user_role(request):
#     """
#     Identify if the request is from admin or regular user
#     Returns: 'admin' or 'user'
#     """
#     # Get admin key from environment
#     env_admin_key = os.getenv('ADMIN_API_KEY')
    
#     # Get admin key from request header
#     admin_key = request.headers.get('X-Admin-Key') or request.META.get('HTTP_X_ADMIN_KEY')
    
#     # DEBUG LOGGING
#     print("=" * 60)
#     print("🔍 CHECKING ADMIN ROLE")
#     print("=" * 60)
#     print(f"Environment ADMIN_API_KEY: '{env_admin_key}'")
#     print(f"Request X-Admin-Key: '{admin_key}'")
#     print(f"Match: {admin_key == env_admin_key}")
#     print("=" * 60)
    
#     # Method 1: Check Django user authentication
#     if hasattr(request, 'user') and request.user.is_authenticated:
#         if request.user.is_staff or request.user.is_superuser:
#             return 'admin'
    
#     # Method 2: Check for admin API key in headers
#     if admin_key and admin_key == env_admin_key:
#         print("✅ ADMIN AUTHENTICATED")
#         return 'admin'
    
#     # Method 3: Check for admin_key in request body (for POST JSON)
#     if request.method == 'POST':
#         try:
#             if request.content_type == 'application/json':
#                 data = json.loads(request.body)
#                 body_admin_key = data.get('admin_key')
                
#                 if body_admin_key and body_admin_key == env_admin_key:
#                     print("✅ ADMIN AUTHENTICATED (via body)")
#                     return 'admin'
#         except:
#             pass
    
#     print("❌ USER (not admin)")
#     return 'user'


# def home(request):
#     """Home page - API only, use React frontend"""
#     return JsonResponse({
#         'message': 'API is running. Use the React frontend to interact.',
#         'endpoints': {
#             'chat': '/api/chat/',
#             'check_role': '/api/check-role/',
#             'chat_history': '/api/chat-history/'
#         }
#     })


# @csrf_exempt
# def speak_text(request):
#     """
#     Original view - keep for backward compatibility
#     Enhanced with role detection
#     """
#     if request.method == 'POST':
#         user_text = request.POST.get('speechText', 'You did not say anything!')
        
#         try:
#             # Identify role
#             role = identify_user_role(request)
            
#             # Query RAG with role
#             rag_response = rag_service.query_rag(user_text, role=role)
            
#             # Handle error responses
#             if "error" in rag_response:
#                 return JsonResponse({
#                     'error': rag_response['error'],
#                     'role': role
#                 }, status=500)
            
#             model_response = rag_response['answer']

#             # Save chat
#             Chat.objects.create(
#                 user_message=f"User: {user_text}",
#                 bot_response=model_response,
#             )

#             # Convert to speech
#             language = (request.POST.get('language') or 'en').strip().lower()
#             tts_lang = 'ne' if language == 'ne' else 'en'
#             tts_input = clean_tts_text(model_response)
#             tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

#             voice_file_path = "voice.mp3"
#             tts.save(voice_file_path)

#             with open(voice_file_path, "rb") as f:
#                 audio_bytes = f.read()
            
#             # Clean up
#             if os.path.exists(voice_file_path):
#                 os.remove(voice_file_path)

#             response_data = {
#                 "response_text": model_response,
#                 "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
#                 "role": role,
#             }
            
#             # Add metadata for admin
#             if role == "admin":
#                 response_data["timestamp"] = rag_response.get('timestamp')
#                 response_data["response_id"] = rag_response.get('response_id')

#             return JsonResponse(response_data)

#         except Exception as e:
#             logger.error(f"Error in speak_text: {str(e)}")
#             return HttpResponse(f"Error: {str(e)}", status=500)

#     return HttpResponse("Invalid request", status=400)


# @csrf_exempt
# def chat_api(request):
#     """
#     Enhanced chat API endpoint for React frontend
#     Supports both user and admin roles
#     Accepts JSON with 'text' and optional 'admin_key' fields
#     Returns JSON with 'text', 'audio_base64', and role information
#     """
#     if request.method == 'POST':
#         try:
#             # Parse JSON body
#             data = json.loads(request.body)
#             user_text = data.get('text', '').strip()
            
#             if not user_text:
#                 return JsonResponse({'error': 'No text provided'}, status=400)
            
#             # Identify role
#             role = identify_user_role(request)
            
#             # Get optional language parameter (default to 'en')
#             language = data.get('language', 'en').strip().lower()
            
#             # Query RAG model with role
#             rag_response = rag_service.query_rag(user_text, role=role)
            
#             # Handle error responses
#             if "error" in rag_response:
#                 return JsonResponse({
#                     'error': rag_response['error'],
#                     'role': role
#                 }, status=500)
            
#             model_response = rag_response['answer']

#             # Save chat to database
#             Chat.objects.create(
#                 user_message=f"User ({role}): {user_text}",
#                 bot_response=model_response,
#             )

#             # Convert to speech
#             tts_lang = 'ne' if language == 'ne' else 'en'
#             tts_input = clean_tts_text(model_response)
#             tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

#             # Save to temporary file
#             voice_file_path = "voice.mp3"
#             tts.save(voice_file_path)

#             # Read audio file and encode to base64
#             with open(voice_file_path, "rb") as f:
#                 audio_bytes = f.read()
            
#             # Clean up the temporary file
#             if os.path.exists(voice_file_path):
#                 os.remove(voice_file_path)

#             # Build response
#             response_data = {
#                 'text': model_response,
#                 'audio_base64': base64.b64encode(audio_bytes).decode("utf-8"),
#                 'role': role,
#             }
            
#             # Add metadata for admin
#             if role == "admin":
#                 response_data['timestamp'] = rag_response.get('timestamp')
#                 response_data['response_id'] = rag_response.get('response_id')
#                 response_data['model'] = rag_response.get('model')

#             return JsonResponse(response_data)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             logger.error(f"Error in chat_api: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)


# # ==================== ADMIN ENDPOINTS ====================

# @csrf_exempt
# def admin_upload_document(request):
#     """
#     Admin endpoint: Upload document to vector store
#     POST with file upload and admin_key
#     """
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         # Check admin authentication
#         admin_key = request.POST.get('admin_key') or request.headers.get('X-Admin-Key')
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         # Check if file exists
#         if 'file' not in request.FILES:
#             return JsonResponse({'error': 'No file provided'}, status=400)
        
#         uploaded_file = request.FILES['file']
        
#         # Save file temporarily
#         temp_path = f"/tmp/{uploaded_file.name}"
#         with open(temp_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
        
#         # Upload to vector store
#         result = rag_service.upload_document(temp_path, admin_key)
        
#         # Clean up temp file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         return JsonResponse(result)
    
#     except Exception as e:
#         logger.error(f"Error in admin_upload_document: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# def admin_upload_text(request):
#     """
#     Admin endpoint: Upload text content to vector store
#     POST JSON with 'content', 'filename', and 'admin_key'
#     """
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         data = json.loads(request.body)
        
#         admin_key = data.get('admin_key') or request.headers.get('X-Admin-Key')
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         content = data.get('content')
#         filename = data.get('filename')
        
#         if not content or not filename:
#             return JsonResponse({'error': 'content and filename are required'}, status=400)
        
#         # Upload text to vector store
#         result = rag_service.upload_text(content, filename, admin_key)
        
#         return JsonResponse(result)
    
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     except Exception as e:
#         logger.error(f"Error in admin_upload_text: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# def admin_upload_voice(request):
#     """
#     Admin endpoint: Upload and transcribe voice to vector store
#     POST with audio file upload and admin_key
#     """
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         admin_key = request.POST.get('admin_key') or request.headers.get('X-Admin-Key')
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         if 'file' not in request.FILES:
#             return JsonResponse({'error': 'No audio file provided'}, status=400)
        
#         uploaded_file = request.FILES['file']
        
#         # Save audio file temporarily
#         temp_path = f"/tmp/{uploaded_file.name}"
#         with open(temp_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
        
#         # Transcribe and upload
#         result = rag_service.upload_voice_transcription(temp_path, admin_key)
        
#         # Clean up temp file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         return JsonResponse(result)
    
#     except Exception as e:
#         logger.error(f"Error in admin_upload_voice: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# def admin_submit_feedback(request):
#     """
#     Admin endpoint: Submit feedback on model responses
#     POST JSON with feedback details and admin_key
#     """
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         data = json.loads(request.body)
        
#         admin_key = data.get('admin_key') or request.headers.get('X-Admin-Key')
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         result = rag_service.submit_feedback(
#             question=data.get('question'),
#             response=data.get('response'),
#             feedback_type=data.get('feedback_type', 'improvement'),
#             feedback_text=data.get('feedback_text'),
#             admin_key=admin_key,
#             rating=data.get('rating')
#         )
        
#         return JsonResponse(result)
    
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     except Exception as e:
#         logger.error(f"Error in admin_submit_feedback: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# def admin_feedback_summary(request):
#     """
#     Admin endpoint: Get feedback summary and analytics
#     POST JSON with admin_key or GET with X-Admin-Key header
#     """
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             admin_key = data.get('admin_key') or request.headers.get('X-Admin-Key')
#         elif request.method == 'GET':
#             admin_key = request.headers.get('X-Admin-Key')
#         else:
#             return JsonResponse({'error': 'Method not allowed'}, status=405)
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         result = rag_service.get_feedback_summary(admin_key)
        
#         return JsonResponse(result)
    
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     except Exception as e:
#         logger.error(f"Error in admin_feedback_summary: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# def admin_list_files(request):
#     """
#     Admin endpoint: List all files in vector store
#     GET or POST with admin_key
#     """
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             admin_key = data.get('admin_key') or request.headers.get('X-Admin-Key')
#         elif request.method == 'GET':
#             admin_key = request.headers.get('X-Admin-Key')
#         else:
#             return JsonResponse({'error': 'Method not allowed'}, status=405)
        
#         if not admin_key or admin_key != os.getenv('ADMIN_API_KEY'):
#             return JsonResponse({'error': 'Unauthorized - Admin access required'}, status=401)
        
#         result = rag_service.list_vector_store_files(admin_key)
        
#         return JsonResponse(result)
    
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     except Exception as e:
#         logger.error(f"Error in admin_list_files: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


# # ==================== UTILITY ENDPOINTS ====================

# @csrf_exempt
# def check_role(request):
#     """
#     Utility endpoint to check current user's role
#     """
#     role = identify_user_role(request)
#     return JsonResponse({
#         'role': role,
#         'is_admin': role == 'admin'
#     })


# @csrf_exempt
# def chat_history(request):
#     """
#     Get chat history
#     Optionally filter by role for admin
#     """
#     try:
#         role = identify_user_role(request)
        
#         # Get query parameters
#         limit = int(request.GET.get('limit', 50))
        
#         # Fetch chats
#         chats = Chat.objects.all().order_by('-created_at')[:limit]
        
#         chat_data = []
#         for chat in chats:
#             chat_data.append({
#                 'id': chat.id,
#                 'user_message': chat.user_message,
#                 'bot_response': chat.bot_response,
#                 'created_at': chat.created_at.isoformat(),
#             })
        
#         return JsonResponse({
#             'chats': chat_data,
#             'total': len(chat_data),
#             'role': role
#         })
    
#     except Exception as e:
#         logger.error(f"Error in chat_history: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from gtts import gTTS
from .models import Chat
import os
import logging
import base64
import re
import json

# ===== LOAD .env FILE =====
from dotenv import load_dotenv
import pathlib

# Get the project root directory (where manage.py is)
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

# Load .env file
load_dotenv(dotenv_path=env_path)

# Verify it loaded (you'll see this when Django starts)
print("=" * 60)
print("🔍 Loading .env file...")
print(f"📁 .env path: {env_path}")
print(f"✅ .env exists: {env_path.exists()}")
print(f"🔑 ADMIN_API_KEY loaded: {bool(os.getenv('ADMIN_API_KEY'))}")
print("=" * 60)
# ===== END .env LOADING =====

from .rag_service import RAGService

logger = logging.getLogger(__name__)
rag_service = RAGService()


def clean_tts_text(text):
    """Sanitize model output so TTS does not read formatting symbols aloud."""
    if not text:
        return ""

    cleaned = str(text)

    # Remove markdown/code/link syntax that sounds noisy in speech.
    cleaned = re.sub(r"```[\s\S]*?```", " ", cleaned)
    cleaned = re.sub(r"`{1,3}", " ", cleaned)
    cleaned = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", cleaned)
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)

    # Strip list/heading/quote markers and common formatting characters.
    cleaned = re.sub(r"^\s*[-+*]\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"[#*_~>|]", " ", cleaned)
    cleaned = cleaned.replace("_", " ")

    # Keep speech-friendly punctuation; remove other symbols.
    cleaned = re.sub(r"[^\w\s.,!?;:'\"()\-\u0900-\u097F।]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def identify_user_role(request):
    """
    Identify if the request is from admin or regular user
    Returns: 'admin' or 'user'
    """
    # Get admin key from environment
    env_admin_key = os.getenv('ADMIN_API_KEY')
    
    if not env_admin_key:
        logger.warning("ADMIN_API_KEY not set in environment!")
        return 'user'
    
    # Check for admin key in header (PRIMARY METHOD)
    admin_key = request.headers.get('X-Admin-Key')
    
    # Fallback: Check in request body for POST requests
    if not admin_key and request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                admin_key = data.get('admin_key')
        except (json.JSONDecodeError, AttributeError):
            pass
    
    # DEBUG LOGGING (optional - remove in production)
    if settings.DEBUG:
        print("=" * 60)
        print("🔍 CHECKING ADMIN ROLE")
        print(f"Environment key exists: {bool(env_admin_key)}")
        print(f"Request key exists: {bool(admin_key)}")
        print(f"Match: {admin_key == env_admin_key if admin_key else False}")
        print("=" * 60)
    
    # Validate admin key
    if admin_key and admin_key == env_admin_key:
        return 'admin'
    
    return 'user'


def home(request):
    """Home page - API only, use React frontend"""
    return JsonResponse({
        'message': 'SajiloSewa API is running',
        'version': '1.0',
        'endpoints': {
            'chat': '/api/chat/',
            'check_role': '/api/check-role/',
            'chat_history': '/api/chat-history/',
            'admin': {
                'upload_document': '/api/admin/upload-document/',
                'upload_text': '/api/admin/upload-text/',
                'upload_voice': '/api/admin/upload-voice/',
                'feedback': '/api/admin/feedback/',
                'feedback_summary': '/api/admin/feedback-summary/',
                'list_files': '/api/admin/list-files/',
            }
        }
    })


@csrf_exempt
def speak_text(request):
    """
    Original view - keep for backward compatibility
    Enhanced with role detection
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    user_text = request.POST.get('speechText', '').strip()
    
    if not user_text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    
    try:
        # Identify role
        role = identify_user_role(request)
        
        # Query RAG with role
        rag_response = rag_service.query_rag(user_text, role=role)
        
        # Handle error responses
        if "error" in rag_response:
            return JsonResponse({
                'error': rag_response['error'],
                'role': role
            }, status=500)
        
        model_response = rag_response['answer']

        # Save chat
        Chat.objects.create(
            user_message=f"User ({role}): {user_text}",
            bot_response=model_response,
        )

        # Convert to speech
        language = (request.POST.get('language') or 'en').strip().lower()
        tts_lang = 'ne' if language == 'ne' else 'en'
        tts_input = clean_tts_text(model_response)
        tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

        voice_file_path = "voice.mp3"
        tts.save(voice_file_path)

        with open(voice_file_path, "rb") as f:
            audio_bytes = f.read()
        
        # Clean up
        if os.path.exists(voice_file_path):
            os.remove(voice_file_path)

        response_data = {
            "response_text": model_response,
            "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
            "role": role,
        }
        
        # Add metadata for admin
        if role == "admin":
            response_data["timestamp"] = rag_response.get('timestamp')
            response_data["response_id"] = rag_response.get('response_id')

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in speak_text: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
def chat_api(request):
    """
    Enhanced chat API endpoint for React frontend
    Supports both user and admin roles
    Accepts JSON with 'text' and 'language' fields
    Returns JSON with 'text', 'audio_base64', and role information
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        
        user_text = data.get('text', '').strip()
        
        if not user_text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        # Identify role
        role = identify_user_role(request)
        
        # Get optional language parameter (default to 'en')
        language = data.get('language', 'en').strip().lower()
        
        # Query RAG model with role
        rag_response = rag_service.query_rag(user_text, role=role)
        
        # Handle error responses
        if "error" in rag_response:
            return JsonResponse({
                'error': rag_response['error'],
                'role': role
            }, status=500)
        
        model_response = rag_response['answer']

        # Save chat to database
        Chat.objects.create(
            user_message=f"User ({role}): {user_text}",
            bot_response=model_response,
        )

        # Convert to speech
        tts_lang = 'ne' if language == 'ne' else 'en'
        tts_input = clean_tts_text(model_response)
        tts = gTTS(text=tts_input, lang=tts_lang, slow=False)

        # Save to temporary file
        voice_file_path = "voice.mp3"
        tts.save(voice_file_path)

        # Read audio file and encode to base64
        with open(voice_file_path, "rb") as f:
            audio_bytes = f.read()
        
        # Clean up the temporary file
        if os.path.exists(voice_file_path):
            os.remove(voice_file_path)

        # Build response
        response_data = {
            'text': model_response,
            'audio_base64': base64.b64encode(audio_bytes).decode("utf-8"),
            'role': role,
        }
        
        # Add metadata for admin
        if role == "admin":
            response_data['timestamp'] = rag_response.get('timestamp')
            response_data['response_id'] = rag_response.get('response_id')
            response_data['model'] = rag_response.get('model')

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in chat_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


# ==================== ADMIN ENDPOINTS ====================

def verify_admin(request):
    """
    Helper function to verify admin authentication
    Returns (is_admin, admin_key, error_response)
    """
    env_admin_key = os.getenv('ADMIN_API_KEY')
    
    if not env_admin_key:
        return False, None, JsonResponse(
            {'error': 'Admin functionality not configured'}, 
            status=500
        )
    
    # Check header first (preferred method)
    admin_key = request.headers.get('X-Admin-Key')
    
    # Fallback to POST/GET parameters
    if not admin_key:
        if request.method == 'POST':
            try:
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                    admin_key = data.get('admin_key')
                else:
                    admin_key = request.POST.get('admin_key')
            except (json.JSONDecodeError, AttributeError):
                pass
        elif request.method == 'GET':
            admin_key = request.GET.get('admin_key')
    
    if not admin_key or admin_key != env_admin_key:
        return False, None, JsonResponse(
            {'error': 'Unauthorized - Admin access required'}, 
            status=401
        )
    
    return True, admin_key, None


@csrf_exempt
def admin_upload_document(request):
    """
    Admin endpoint: Upload document to vector store
    POST with file upload and admin_key
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        # Check if file exists
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Save file temporarily
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Upload to vector store
        result = rag_service.upload_document(temp_path, admin_key)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error in admin_upload_document: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)


@csrf_exempt
def admin_upload_text(request):
    """
    Admin endpoint: Upload text content to vector store
    POST JSON with 'content', 'filename', and 'admin_key'
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        data = json.loads(request.body)
        
        content = data.get('content')
        filename = data.get('filename')
        
        if not content or not filename:
            return JsonResponse(
                {'error': 'content and filename are required'}, 
                status=400
            )
        
        # Upload text to vector store
        result = rag_service.upload_text(content, filename, admin_key)
        
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        logger.error(f"Error in admin_upload_text: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)


@csrf_exempt
def admin_upload_voice(request):
    """
    Admin endpoint: Upload and transcribe voice to vector store
    POST with audio file upload and admin_key
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Save audio file temporarily
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Transcribe and upload
        result = rag_service.upload_voice_transcription(temp_path, admin_key)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error in admin_upload_voice: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)


@csrf_exempt
def admin_submit_feedback(request):
    """
    Admin endpoint: Submit feedback on model responses
    POST JSON with feedback details and admin_key
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        data = json.loads(request.body)
        
        result = rag_service.submit_feedback(
            question=data.get('question'),
            response=data.get('response'),
            feedback_type=data.get('feedback_type', 'improvement'),
            feedback_text=data.get('feedback_text'),
            admin_key=admin_key,
            rating=data.get('rating')
        )
        
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        logger.error(f"Error in admin_submit_feedback: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Feedback submission failed: {str(e)}'}, status=500)


@csrf_exempt
def admin_feedback_summary(request):
    """
    Admin endpoint: Get feedback summary and analytics
    GET or POST with admin_key
    """
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        result = rag_service.get_feedback_summary(admin_key)
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error in admin_feedback_summary: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Failed to fetch summary: {str(e)}'}, status=500)


@csrf_exempt
def admin_list_files(request):
    """
    Admin endpoint: List all files in vector store
    GET or POST with admin_key
    """
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Verify admin
    is_admin, admin_key, error_response = verify_admin(request)
    if not is_admin:
        return error_response
    
    try:
        result = rag_service.list_vector_store_files(admin_key)
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error in admin_list_files: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Failed to list files: {str(e)}'}, status=500)


# ==================== UTILITY ENDPOINTS ====================

@csrf_exempt
def check_role(request):
    """
    Utility endpoint to check current user's role
    GET or POST
    """
    try:
        role = identify_user_role(request)
        return JsonResponse({
            'role': role,
            'is_admin': role == 'admin',
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error in check_role: {str(e)}", exc_info=True)
        return JsonResponse({
            'role': 'user',
            'is_admin': False,
            'status': 'error',
            'error': str(e)
        }, status=500)


@csrf_exempt
def chat_history(request):
    """
    Get chat history
    GET with optional limit parameter
    """
    try:
        role = identify_user_role(request)
        
        # Get query parameters
        limit = int(request.GET.get('limit', 50))
        limit = min(limit, 200)  # Cap at 200 for performance
        
        # Fetch chats
        chats = Chat.objects.all().order_by('-created_at')[:limit]
        
        chat_data = []
        for chat in chats:
            chat_data.append({
                'id': chat.id,
                'user_message': chat.user_message,
                'bot_response': chat.bot_response,
                'created_at': chat.created_at.isoformat(),
            })
        
        return JsonResponse({
            'chats': chat_data,
            'total': len(chat_data),
            'role': role,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Error in chat_history: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'Failed to fetch history: {str(e)}',
            'status': 'error'
        }, status=500)
