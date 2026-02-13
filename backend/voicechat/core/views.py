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
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from gtts import gTTS
from .models import Chat
import os
import logging
import base64
import re
from .rag_service import query_rag
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

def clean_tts_text(text):
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
    return cleaned.strip()


def home(request):
    return render(request, 'core/index.html')


@csrf_exempt
def speak_text(request):
    """Original view - keep for backward compatibility"""
    if request.method == 'POST':
        user_text = request.POST.get('speechText', 'You did not say anything!')
        try:
            model_response = query_rag(user_text)

            # Save chat
            Chat.objects.create(
                user_message=f"Aman Patel: {user_text}",
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

            return JsonResponse(
                {
                    "response_text": model_response,
                    "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
                }
            )

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    return HttpResponse("Invalid request", status=400)


@csrf_exempt
def chat_api(request):
    """
    New API endpoint for React frontend
    Accepts JSON with 'text' field
    Returns JSON with 'text' and 'audio_base64' fields
    """
    if request.method == 'POST':
        try:
            # Parse JSON body
            import json
            data = json.loads(request.body)
            user_text = data.get('text', '').strip()
            
            if not user_text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            
            # Get optional language parameter (default to 'en')
            language = data.get('language', 'en').strip().lower()
            
            # Query RAG model
            model_response = query_rag(user_text)

            # Save chat to database
            Chat.objects.create(
                user_message=f"User: {user_text}",
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

            # Return JSON response
            return JsonResponse({
                'text': model_response,
                'audio_base64': base64.b64encode(audio_bytes).decode("utf-8"),
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error in chat_api: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)