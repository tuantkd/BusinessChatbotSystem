from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .constant import RASA_ENDPOINT

from interactive_chatbot.models import Bot
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
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

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
class BotsView(TemplateView):
    template_name = 'bots/bots.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['botList'] = Bot.objects.all()  # Get all bots
        return context
class EditBotView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'bots/edit_bot.html')

class AddBotView(View):
    def get(self, request, *args, **kwargs):
        # Your code here
        pass

class ImportBotView(View):
    def get(self, request, *args, **kwargs):
        # Your code here
        pass
    
class ActionsView(TemplateView):
    # Assuming there might be a specific template for actions that hasn't been listed
    template_name = 'actions/edit_action.html'  # Adjust if there's an actual path

class AddIntentView(TemplateView):
    template_name = 'intents/add_intent.html'

class EditIntentView(TemplateView):
    template_name = 'intents/edit_intent.html'

class StoriesView(TemplateView):
    template_name = 'stories/stories.html'

class EntitiesView(TemplateView):
    # Assuming entities list view might be missing, using 'entities.html' if exists
    template_name = 'entities/entities.html'  # Adjust if there's an actual path

class AddEntityView(TemplateView):
    template_name = 'entities/add_entity.html'

class EditEntityView(TemplateView):
    template_name = 'entities/edit_entity.html'

class AddRegexView(TemplateView):
    template_name = 'regex/add_regex.html'

class EditRegexView(TemplateView):
    template_name = 'regex/edit_regex.html'

class AddSynonymView(TemplateView):
    template_name = 'synonyms/add_synonym.html'

class EditSynonymView(TemplateView):
    template_name = 'synonyms/edit_synonym.html'

class RasaConfigView(TemplateView):
    template_name = 'rasaconfig/rasa_config.html'

class LogsView(TemplateView):
    template_name = 'logs/logs.html'

class HistoryView(TemplateView):
    # Assuming there might be a specific template for history that hasn't been listed
    template_name = 'history/history.html'  # Adjust if there's an actual path

class ConversationView(TemplateView):
    # Assuming conversation view might need a specific template
    template_name = 'conversation/conversation.html'  # Adjust if there's an actual path

class InsightsView(TemplateView):
    template_name = 'insights/insights.html'

class TrainingView(TemplateView):
    template_name = 'training/training.html'

class SettingsView(TemplateView):
    template_name = 'settings/settings.html'

class ModelView(TemplateView):
    # Assuming models list view might be missing, using 'models/models.html' if exists
    template_name = 'models/models.html'  # Adjust if there's an actual path

class AddModelView(TemplateView):
    # Assuming add model view might need a specific template
    template_name = 'models/add_model.html'  # Adjust if there's an actual path

class ResponseView(TemplateView):
    template_name = 'responses/responses.html'

class AddActionView(TemplateView):
    template_name = 'responses/add_action.html'
