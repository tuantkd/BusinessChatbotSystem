from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .constant import RASA_ENDPOINT

# Create your views here.

def chatbot(request):
    return render(request, 'chatbot.html')

class ChatbotView(APIView):
    def post(self, request, format=None):
        try:
            user_message = request.data.get('message')
            session_id = request.data.get('session_id')
            sender = request.data.get('sender')

            # Send message and sender_id to Rasa
            data = {"message": user_message, "session_id": session_id, "sender": sender}
            response = requests.post(RASA_ENDPOINT, json=data)

            # Return Rasa's response
            return Response(response.json(), status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)