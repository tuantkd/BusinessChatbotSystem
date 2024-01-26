from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.

def chatbot(request):
    return render(request, 'chatbot.html')

class ChatbotView(APIView):
    def post(self, request, format=None):
        message = request.data.get('message')
        sender_id = request.data.get('sender_id')

        # Send message and sender_id to Rasa
        rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook'  # Replace with your Rasa endpoint
        data = {"message": message, "sender": sender_id}
        response = requests.post(rasa_endpoint, json=data)

        # Return Rasa's response
        return Response(response.json())