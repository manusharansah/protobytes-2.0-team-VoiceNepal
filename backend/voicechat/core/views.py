# Create your views here.
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
