import datetime
import json
import uuid
from django.shortcuts import render
from .utils import markdown_to_html
from chatbot_data.models import ChatUser, History
import requests

from enterprise_registration_app.settings import RASA_CONVERSATIONS_ENDPOINT, RASA_WEBHOOKS_ENDPOINT
from django.views.generic.base import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def save_conversation(sender_id, user_say, response):
    get_conversation_url = RASA_CONVERSATIONS_ENDPOINT.replace('<sender_id>', sender_id)
    result = requests.get(f'{get_conversation_url}')
    if result.status_code != 200:
        return 
    tracker = result.json()
    last_message = tracker.get('latest_message', {})
    intent = last_message.get('intent', {})
    entities = last_message.get('entities', [])
    slot_values = tracker.get('slots', {})
    intent_ranking = tracker.get('latest_message', {}).get('intent_ranking', [])

    saved_slots = []
    for key, value in slot_values.items():
        if value:
            saved_slots.append({'name': key, 'value': value})
    History.objects.create(
                        intent=intent.get('name', ''),
                        entities=entities,
                        slot_values=saved_slots,
                        sender_id=tracker.get('sender_id', ''),
                        confidence=last_message.get('intent', {}).get('confidence', 0),
                        user_say=user_say,
                        response=response,
                        intent_ranking=intent_ranking,
                        timestamp=datetime.datetime.now())
    
class ChatbotView(View):
    template_name = 'chatbot.html'
    def get(self, request, *args, **kwargs):
        sender_id = kwargs.get('sender_id')
        chat_user = ChatUser.objects.filter(sender_id=sender_id).first()
        if not sender_id and not chat_user:
            return render(request, self.template_name, {'error': 'Sender not found'})
        history = History.objects.filter(sender_id=sender_id).order_by('timestamp')
        history = [{'user_say': h.user_say, 
                    'response': markdown_to_html(h.response), 
                    'timestamp': h.timestamp,
                    } for h in history]
        if len(history) == 0:
            chatlog_id = uuid.uuid4().hex
            data = {"message": "/session_start", "sender": sender_id, "metadata": {"chatlog_id": chatlog_id, "sender_name": chat_user.sender_name}}
            response = requests.post(RASA_WEBHOOKS_ENDPOINT, json=data)
        
            if response.status_code != 200:
                return JsonResponse({'error': 'Rasa server error'}, status=500)
            response_data = response.json()
            response_text = 'Xin lỗi, tôi không hiểu câu hỏi của bạn'
            if len(response_data) > 0:
                response_text = response_data[0].get('text', '')
            save_conversation(sender_id, "Bắt đầu", response_text)
            history = [
                
            ]

        return render(request, self.template_name, {'chat_user': chat_user, 'chat_history': history})
    
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            sender_id = data.get('sender')
            sender = ChatUser.objects.filter(sender_id=sender_id).first()
            if not sender:
                return JsonResponse({'error': 'Sender not found'}, status=404)
            chatlog_id = uuid.uuid4().hex

            # Send message and sender_id to Rasa
            data = {"message": user_message, "sender": sender.sender_id, "metadata": {"chatlog_id": chatlog_id, "sender_name": sender.sender_name}}
            response = requests.post(RASA_WEBHOOKS_ENDPOINT, json=data)
            if response.status_code != 200:
                return JsonResponse({'error': 'Rasa server error'}, status=500)
            data_json = response.json()
            response_text = 'Xin lỗi, tôi không hiểu câu hỏi của bạn'
            if len(data_json) > 0:
                # return JsonResponse({'text': 'Xin lỗi, tôi không hiểu câu hỏi của bạn'}, status=200)
                response_text = data_json[0].get('text', '')
            save_conversation(sender_id, user_message, response_text)
            # Return Rasa's response
            response_data = {
                "text" : markdown_to_html(response_text),
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@method_decorator(csrf_exempt, name='dispatch')
class InitChatView(View):
    
    def post(self, request, format=None):
        sender_name = request.POST.get('senderName')
        sender_id = uuid.uuid4().hex
        ChatUser.objects.create(sender_id=sender_id, sender_name=sender_name)
        return redirect('chatbot', sender_id=sender_id)
    
def get_current_user(request, *args, **kwargs):
    sender_id = kwargs.get('sender_id')
    chat_user = ChatUser.objects.filter(sender_id=sender_id).first()
    return JsonResponse({'senderName': chat_user.sender_name}, status=200)

# views.py
def csrf_failure(request, reason=""):
    return JsonResponse({'status':'ok'}, status=200)

