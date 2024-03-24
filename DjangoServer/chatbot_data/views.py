from datetime import datetime, timezone
import json
import os
import pdb
import re
from django.core import serializers
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseServerError, JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
import requests
from rest_framework.renderers import JSONRenderer
from .serializers import ExpressionParameterSerializer, LookupVariantSerializer, RegexVariantSerializer, ResponseSerializer, SynonymVariantSerializer
from .models import Bot, Action, Entity, Expression, ExpressionParameter, Intent, Lookup, LookupVariant, Regex, RegexVariant, Response, Story, ModelModel, Conversation, Synonym, SynonymVariant
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BotForm, ImportBotForm, ActionForm, IntentForm, LookupForm, RegexForm, ResponseForm, StoryForm, EntityForm, SynonymForm
from django.shortcuts import redirect
from django.contrib import messages
from enterprise_registration_app.settings import RASA_PREDICT_URL
import yaml
from django.db import transaction
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
class BotsView(TemplateView):
    template_name = 'bots/bots.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['botList'] = Bot.objects.all()  # Get all bots
        return context
    
def delete_bot(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    bot.delete()
    return redirect('bots') 
class EditBotView(View):
    form_class = BotForm
    template_name = 'bots/edit_bot.html'

    def get(self, request, bot_id, *args, **kwargs):
        # Lấy đối tượng bot dựa trên bot_id, nếu không tồn tại thì trả về 404
        bot = get_object_or_404(Bot, pk=bot_id)
        # Khởi tạo form với instance là đối tượng bot
        form = self.form_class(instance=bot)
        # Lấy danh sách các Intent, Entity, Synonym, và Regex liên quan đến bot
        intents = bot.intents.all()
        entities = bot.entities.all()
        synonyms = bot.synonyms.all()
        regexes = bot.regexes.all()
        # Render template kèm theo form và các danh sách
        return render(request, self.template_name, {
            'form': form,
            'bot': bot,
            'intents': intents,
            'entities': entities,
            'synonyms': synonyms,
            'regexes': regexes,
        })

    def post(self, request, bot_id, *args, **kwargs):
        # Lấy lại đối tượng bot như ở phương thức GET
        bot = get_object_or_404(Bot, pk=bot_id)
        # Khởi tạo form với dữ liệu POST và instance là bot cần cập nhật
        form = self.form_class(request.POST, instance=bot)
        if form.is_valid():
            # Lưu thay đổi vào cơ sở dữ liệu
            form.save()
            # Chuyển hướng người dùng tới trang danh sách bot hoặc trang chi tiết của bot vừa cập nhật
            # Giả sử bạn có một view tên là 'bot_detail' để hiển thị chi tiết bot
            return redirect('bots')
        
        # If the form is not valid, re-render the page with existing form data
        return render(request, self.template_name, {'form': form})



class AddBotView(View):
    form_class = BotForm
    template_name = 'bots/add_bot.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_dir, 'data/config.yml')
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config_default = file.read()
        form.fields['bot_config'].initial = config_default
        form.fields['output_folder'].initial = 'models'
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a new URL, assuming you have a view named 'bots'
            # that lists all bots or shows a success page
            return redirect('bots')
        
        # If the form is not valid, re-render the page with existing form data
        return render(request, self.template_name, {'form': form})

def extract_entities(expression):
        pattern = r'\[(.*?)\]\((.*?)\)'
        matches = re.finditer(pattern, expression)
        entities = []
        for match in matches:
            value = match.group(1).strip()
            entity = match.group(2).strip()
            start = match.start()
            end = match.end()
            entities.append({'entity': entity, 'value': value, 'start': start, 'end': end})
        return entities
class ImportBotView(View):
    form_class = ImportBotForm
    template_name = 'bots/import_bot.html'  # Đường dẫn đến template của bạn

    def get(self, request, *args, **kwargs):
        form = self.form_class()  # Khởi tạo form rỗng
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    bot_name = form.cleaned_data['bot_name']
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    config_file_path = os.path.join(current_dir, 'data/config.yml')
                    with open(config_file_path, 'r', encoding='utf-8') as file:
                        config_default = file.read()

                    output_folder = 'models'

                    bot_find = Bot.objects.filter(bot_name=bot_name).first()
                    if bot_find:
                        raise Exception('Bot name already exists')
                    
                    new_bot = Bot.objects.create(
                        bot_name=bot_name,
                        bot_config=config_default,
                        output_folder=output_folder
                    )
                bot_file = request.FILES['file']
                bot_data = yaml.safe_load(bot_file)
                
                for data in bot_data['nlu']:
                    if 'intent' in data:
                        # create new intent
                        intent_name = data['intent']
                        intent_find = Intent.objects.filter(intent_name=intent_name, bot=new_bot).first()
                        if not intent_find:
                            new_intent = Intent.objects.create(
                                intent_name=intent_name,
                                bot=new_bot
                            )
                        else:
                            new_intent = intent_find

                        expressions = data['examples'].split('\n')
                        for expression in expressions:
                            # remove - at the beginning of the expression
                            expression = re.sub(r'^\s*-\s*', '', expression)
                            expression = expression.strip()
                            if expression == '':
                                continue
                            entities = extract_entities(expression)
                            stand_expression = expression
                            match_expression = expression
                            new_parameters = []
                            for entity in entities:
                                stand_expression = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', stand_expression, 1)
                                match_expression = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', match_expression, 1)
                                entity['start'] = match_expression.find(entity['value'])
                                entity['end'] = entity['start'] + len(entity['value'])
                                # replace matched value with * to avoid duplicate search
                                match_expression = match_expression[:entity['start']] + '*' * len(entity['value']) + match_expression[entity['end']:]
                            
                                # check if entity not exist in database, create new entity
                                entity_find = Entity.objects.filter(entity_name=entity['entity'], bot=new_bot).first()
                                if not entity_find:
                                    new_entity = Entity.objects.create(entity_name=entity['entity'], bot=new_bot, slot_data_type='text')
                                else :
                                    new_entity = entity_find
                                    
                                new_parameter = {
                                    'entity': new_entity,
                                    'start': entity['start'],
                                    'end': entity['end'],
                                    'value': entity['value'],
                                    'intent': new_intent,
                                }
                                new_parameters.append(new_parameter)

                            # check if expression not exist in database, create new expression
                            expression_find = Expression.objects.filter(expression_text=stand_expression, intent=new_intent).first()
                            if not expression_find:
                                new_expression = Expression.objects.create(
                                    expression_text=stand_expression,
                                    intent=new_intent
                                )
                            else:
                                new_expression = expression_find

                            for parameter in new_parameters:

                                parameters_find = ExpressionParameter.objects.filter(
                                    intent=new_intent,
                                    expression=new_expression,
                                    entity=parameter['entity']
                                ).all()
                                # check conflict parameter
                                if not parameters_find or all([False if\
                                            param.parameter_start < parameter['start'] <= param.parameter_end\
                                        or  param.parameter_start < parameter['end'] <= param.parameter_end\
                                        or (parameter['start'] < param.parameter_start and parameter['end'] > param.parameter_end)\
                                        else True
                                        for param in parameters_find]):
                                    ExpressionParameter.objects.create(
                                        parameter_start=parameter['start'],
                                        parameter_end=parameter['end'],
                                        parameter_value=parameter['value'],
                                        intent=new_intent,
                                        expression=new_expression,
                                        entity=parameter['entity']
                                    )

                    elif 'regex' in data:
                        regex_name = data['regex']
                        # check if regex not exist in database, create new regex
                        regex_find = Regex.objects.filter(regex_name=regex_name, bot=new_bot).first()
                        if not regex_find:
                            new_regex = Regex.objects.create(
                                regex_name=regex_name,
                                bot=new_bot
                            )
                            
                    elif 'synonym' in data:
                        synonym_reference = data['synonym']
                        synonym_reference = synonym_reference.strip()
                        if synonym_reference == '':
                            continue
                        synonym_variants = data['examples'].split('\n')
                        # check if synonym not exist in database, create new synonym
                        synonym_find = Synonym.objects.filter(synonym_reference=synonym_reference, bot=new_bot).first()
                        if not synonym_find:
                            new_synonym = Synonym.objects.create(
                                synonym_reference=synonym_reference,
                                bot=new_bot
                            )
                        else:
                            new_synonym = synonym_find
                        for synonym_variant in synonym_variants:
                            synonym_variant = re.sub(r'^\s*-\s*', '', synonym_variant)
                            synonym_variant = synonym_variant.strip()
                            if synonym_variant == '':
                                continue
                            synonym_variant_find = SynonymVariant.objects.filter(synonym=new_synonym, synonym_value=synonym_variant).first()
                            if not synonym_variant_find:
                                new_synonym_variant = SynonymVariant.objects.create(
                                    synonym=new_synonym,
                                    synonym_value=synonym_variant
                                )
            return redirect('bots')

        except Exception as e:
            messages.error(request, 'Error importing bot: ' + str(e))
            return render(request, self.template_name, {'form': form})
        
            
    
class ActionsView(TemplateView):
    # Assuming there might be a specific template for actions that hasn't been listed
    template_name = 'actions/edit_action.html'  # Adjust if there's an actual path

class AddIntentView(View):
    template_name = 'intents/add_intent.html'
    def get(self, request, bot_id):
        bot = Bot.objects.get(id=bot_id)  # Replace with your actual query
        return render(request, self.template_name, {'bot': bot})

    def post(self, request, bot_id):
        bot = Bot.objects.get(id=bot_id)  # Replace with your actual query
        intent_name = request.POST.get('intent_name')
        Intent.objects.create(bot=bot, intent_name=intent_name)  # Replace with your actual creation logic
        return redirect('bot_detail', bot_id=bot.id)  # Replace with your actual redirect

class EditIntentView(View):
    template_name = 'intents/edit_intent.html'
    
    def get(self, request, intent_id, *args, **kwargs):
        intent = get_object_or_404(Intent, pk=intent_id)
        bot = intent.bot
        form = IntentForm(instance=intent)
        parameter_list = ExpressionParameter.objects.filter(intent=intent).all()
        serializer = ExpressionParameterSerializer(parameter_list, many=True)
        serialized_parameters = JSONRenderer().render(serializer.data)
        context = {
            'form': form,
            'bot': bot,
            'intent': intent,
            'entity_list': bot.entities.all(),
            'expression_list': intent.expressions.all(),
            'parameter_list': parameter_list,
            'parameter_json': serialized_parameters.decode('utf-8')

        }
        return render(request, self.template_name, context)

    def post(self, request, bot_id, intent_id, *args, **kwargs):
        bot = get_object_or_404(Bot, pk=bot_id)
        intent = get_object_or_404(Intent, pk=intent_id)
        form = IntentForm(request.POST, instance=intent)
        if form.is_valid():
            form.save()
            return redirect('edit_intent', intent_id=intent.id)
        return render(request, self.template_name, {'form': form, 'bot': bot, 'intent': intent})
    
class AddExpressionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            expression_text = data.get('expression_text')
            intent_id = kwargs.get('intent_id')
            intent = Intent.objects.get(pk=intent_id) if intent_id else None
            bot = intent.bot if intent else None
            Expression.objects.create(expression_text=expression_text, intent=intent)
            return redirect('edit_intent', intent_id=intent_id)
        except Exception as e:
            # Handle the exception here
            # You can log the error or return an error response
            return HttpResponseServerError("An error occurred: " + str(e))


def delete_expression(request, intent_id ,expression_id):
    if request.method == 'POST':
        try:
            expression = Expression.objects.get(id=expression_id)
            intent = Intent.objects.get(id=intent_id)
            expression.delete()
            return redirect('edit_intent', intent_id=intent_id)
        except Expression.DoesNotExist:
            return JsonResponse({'error': 'Expression not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def add_parameter(request, intent_id ,expression_id):
    if request.method == 'POST':
        try:
            expression = Expression.objects.get(id=expression_id)
            intent = Intent.objects.get(id=intent_id)
            data = json.loads(request.body)
            parameter_start = data.get('parameter_start')
            parameter_end = data.get('parameter_end')
            parameter_value = data.get('parameter_value')
            new_parameter = ExpressionParameter.objects.create(
                parameter_start = parameter_start,
                parameter_end = parameter_end,
                parameter_value = parameter_value,
                intent = intent,
                expression = expression,
            )
            return redirect('edit_intent', intent_id=intent.id)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))

def update_parameter(request, intent_id, parameter_id):
    if request.method == 'POST':
        try:
            parameter = ExpressionParameter.objects.get(id=parameter_id)
            data = json.loads(request.body)
            entity_id = data.get('entity_id')
            entity = Entity.objects.get(id=entity_id) if entity_id else None
            parameter.entity = entity
            parameter.save()
            return JsonResponse({'message': 'Parameter updated successfully.'}, status=200)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def delete_parameter(request, intent_id, parameter_id):
    if request.method == 'POST':
        try:
            parameter = ExpressionParameter.objects.get(id=parameter_id)
            parameter.delete()
            return JsonResponse({'message': 'Parameter deleted successfully.'}, status=200)
        except ExpressionParameter.DoesNotExist:
            return JsonResponse({'error': 'Parameter not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def predict_expression(request, intent_id, expression_id):
    try:
        # Parse dữ liệu từ AJAX request
        data = json.loads(request.body)
        expression_text = data.get('expression_text')
        # URL của RASA server endpoint

        # Gửi dữ liệu đến RASA server
        response = requests.post(RASA_PREDICT_URL, json={'text': expression_text})
        response_data = response.json()
        if response_data is not None:
            entities = response_data.get('entities', [])
            for entity in entities:
                entity_name = entity.get('entity')
                entity_obj = Entity.objects.filter(entity_name=entity_name).first()
                expression = Expression.objects.get(pk=expression_id)
                intent = Intent.objects.get(pk=intent_id)
                if not entity_obj:
                    entity_obj = Entity.objects.create(
                        entity_name=entity_name,
                        slot_data_type='text',
                        bot_id=intent.bot.id
                    )
                # Save entity and database using expression parameter
                expression_parameter = ExpressionParameter.objects.create(
                    parameter_start=entity.get('start'),
                    parameter_end=entity.get('end'),
                    parameter_value=entity.get('value'),
                    intent=intent,
                    expression=expression,
                    entity=entity_obj
                )
                expression_parameter.save()
        return JsonResponse({'success': True, 'data': response_data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
class StoriesView(View):
    template_name = 'stories/stories.html'

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        stories = Story.objects.filter(bot_id=bot_id) if bot_id else []
        bots = Bot.objects.all()
        selected_bot = Bot.objects.get(pk=bot_id) if bot_id else None
        selected_bot_id = selected_bot.id if selected_bot else 0
        return render(request, self.template_name, {'storyList': stories, 'botList': bots, 'selectedBot': selected_bot_id})

    def post(self, request, *args, **kwargs):
        # This method would be used if you're creating a story via a form submission
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stories_view')
        return render(request, self.template_name, {'form': form})
    
def search_text(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    data = json.loads(request.body)
    results_search = []
    intent_filter = Intent.objects.filter(bot=bot)
    results_search += [{
        'text' : intent.intent_name,
        'type' : 'intent',
    } for intent in intent_filter]
    entity_filter = Entity.objects.filter(bot=bot)
    results_search += [{
        'text' : entity.entity_name,
        'type' : 'entity',
    } for entity in entity_filter]
    action_filter = Action.objects.filter(bot=bot)
    results_search += [{
        'text' : action.action_name,
        'type' : 'action',
    } for action in action_filter]
    
    return JsonResponse({'items': results_search}, status=200)

class AddStoryView(View):
    template_name = 'stories/add_story.html'

    def get(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        timestamp = int(time.mktime(datetime.now().timetuple()))
        story_name = "story_" + str(timestamp)
        return render(request, self.template_name, {'bot': bot, 'story_name': story_name})
    
    def post(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        story_name = request.POST.get('story_name')
        timestamp = datetime.now(timezone.utc)
        
        Story.objects.create(bot=bot, story_name=story_name, timestamp=timestamp)
        return redirect('stories', bot_id=bot_id)
    
class EditStoryView(View):
    template_name = 'stories/edit_story.html'

    def get(self, request, *args, **kwargs):
        story = get_object_or_404(Story, pk=kwargs.get('story_id'))
        bot_id = story.bot.id
        bot = Bot.objects.get(id=bot_id)
        form = StoryForm(instance=story)
        return render(request, self.template_name, {'form': form, 'story': story, 'bot': bot})
    
    def post(self, request, *args, **kwargs):
        try:
            story = get_object_or_404(Story, pk=kwargs.get('story_id'))
            form = StoryForm(request.POST, instance=story)
            story.story_name = form.data['story_name']
            story.timestamp = datetime.now(timezone.utc)
            story.save()
            return redirect('stories', bot_id=story.bot.id)
        except Exception as e:
            return render(request, self.template_name, {'form': form, 'story': story})
class StoryDetailView(View):
    template_name = 'stories/story_detail.html'

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        return render(request, self.template_name, {'story': story})

def delete_story(request, bot_id, story_id):
    try:
        story = Story.objects.get(id=story_id)
        story.delete()
        return redirect('stories', bot_id=bot_id)
    except Story.DoesNotExist:
        return JsonResponse({'error': 'Story not found.'}, status=404)
    
def save_story_step(request, bot_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        story_id = data.get('story_id')
        story_text = data.get('yaml_text')
        story = Story.objects.get(id=story_id)
        story.story = story_text
        story.save()
        return JsonResponse({'message': 'Story saved successfully.'}, status=200)
class EntitiesView(TemplateView):
    # Assuming entities list view might be missing, using 'entities.html' if exists
    template_name = 'entities/entities.html'  # Adjust if there's an actual path

class AddEntityView(View):
    template_name = 'entities/add_entity.html'

    def get(self, request,  *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        return render(request, self.template_name, {'bot': bot})
    
    def post(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        entity_name = request.POST.get('entity_name')
        slot_data_type = request.POST.get('slot_data_type')
        Entity.objects.create(entity_name=entity_name, slot_data_type=slot_data_type, bot=bot)
        return redirect('bot_detail', bot_id=bot_id)

def delete_entity(request, bot_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        entity.delete()
        return redirect('bot_detail', bot_id=bot_id)
    except Entity.DoesNotExist:
        return JsonResponse({'error': 'Entity not found.'}, status=404)

class EditEntityView(View):
    template_name = 'entities/edit_entity.html'

    def get(self, request, *args, **kwargs):
        entity = get_object_or_404(Entity, pk=kwargs.get('entity_id'))

        form = EntityForm(instance=entity)
        return render(request, self.template_name, {'form': form, 'entity': entity})
    
    def post(self, request, *args, **kwargs):
        entity = get_object_or_404(Entity, pk=kwargs.get('entity_id'))
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            return redirect('bot_detail', bot_id=entity.bot.id)
        return render(request, self.template_name, {'form': form, 'entity': entity})

class AddRegexView(View):
    template_name = 'regex/add_regex.html'

    def get(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        return render(request, self.template_name, {'bot': bot})
    
    def post(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        regex_name = request.POST.get('regex_name')
        Regex.objects.create(regex_name=regex_name, bot=bot)
        return redirect('bot_detail', bot_id=bot_id)
class AddLookupView(View):
    template_name = 'lookup/add_lookup.html'

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        return render(request, self.template_name, {'bot': bot})
    
    def post(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        lookup_name = request.POST.get('lookup_name')
        Lookup.objects.create(lookup_name=lookup_name, bot=bot)
        return redirect('bot_detail', bot_id=bot_id)
    
class EditLookupView(View):
    template_name = 'lookup/edit_lookup.html'

    def get(self, request, *args, **kwargs):
        lookup = get_object_or_404(Lookup, pk=kwargs.get('lookup_id'))
        form = LookupForm(instance=lookup)
        lookup_variants = LookupVariant.objects.filter(lookup=lookup)
        serializer = LookupVariantSerializer(lookup_variants, many=True)
        serialized_lookups = JSONRenderer().render(serializer.data)
        lookups_json = serialized_lookups.decode('utf-8')
        return render(request, self.template_name, {'form': form, 'lookup': lookup, 'lookup_values_json': lookups_json})
    
    def post(self, request, *args, **kwargs):
        lookup = get_object_or_404(Lookup, pk=kwargs.get('lookup_id'))
        form = LookupForm(request.POST, instance=lookup)
        if form.is_valid():
            form.save()
            return redirect('bot_detail', bot_id=lookup.bot.id)
        return render(request, self.template_name, {'form': form, 'lookup': lookup})
    
def delete_lookup(request, bot_id, lookup_id):
    try:
        lookup = Lookup.objects.get(id=lookup_id)
        lookup.delete()
        return redirect('bot_detail', bot_id=bot_id)
    except Lookup.DoesNotExist:
        return JsonResponse({'error': 'Lookup not found.'}, status=404)
    
def add_lookup_variant(request, bot_id, lookup_id):
    if request.method == 'POST':
        try:
            lookup = Lookup.objects.get(id=lookup_id)
            data = json.loads(request.body)
            lookup_value = data.get('lookup_value')
            lookup_variant = LookupVariant.objects.create(lookup=lookup, value=lookup_value)
            serializer = LookupVariantSerializer(lookup_variant)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def remove_lookup_variant(request, bot_id, lookup_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lookup_variant_id = data.get('lookup_variant_id')
            lookup_variant = LookupVariant.objects.get(id=lookup_variant_id)
            lookup_variant.delete()
            return JsonResponse({'message': 'Lookup variant deleted successfully.'}, status=200)
        except LookupVariant.DoesNotExist:
            return JsonResponse({'error': 'Lookup variant not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
class EditRegexView(View):
    template_name = 'regex/edit_regex.html'

    def get(self, request, *args, **kwargs):
        regex = get_object_or_404(Regex, pk=kwargs.get('regex_id'))
        form = RegexForm(instance=regex)

        return render(request, self.template_name, {'form': form, 'regex': regex, 'bot': regex.bot})

    def post(self, request, *args, **kwargs):
        regex = get_object_or_404(Regex, pk=kwargs.get('regex_id'))
        form = RegexForm(request.POST, instance=regex)
        if form.is_valid():
            form.save()
            return redirect('bot_detail', bot_id=regex.bot.id)
        return render(request, self.template_name, {'form': form, 'regex': regex})
    
def add_regex_variant(request, bot_id, regex_id):
    if request.method == 'POST':
        try:
            regex = Regex.objects.get(id=regex_id)
            data = json.loads(request.body)
            regex_value = data.get('regex_value')
            regex_variant = RegexVariant.objects.create(regex=regex, pattern=regex_value)
            serializer = RegexVariantSerializer(regex_variant)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def remove_regex_variant(request, bot_id, regex_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            regex_variant_id = data.get('regex_variant_id')
            regex_variant = RegexVariant.objects.get(id=regex_variant_id)
            regex_variant.delete()
            return JsonResponse({'message': 'Regex variant deleted successfully.'}, status=200)
        except RegexVariant.DoesNotExist:
            return JsonResponse({'error': 'Regex variant not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def delete_regex(request, bot_id, regex_id):
    try:
        regex = Regex.objects.get(id=regex_id)
        regex.delete()
        return redirect('bot_detail', bot_id=bot_id)
    except Regex.DoesNotExist:
        return JsonResponse({'error': 'Regex not found.'}, status=404)
class AddSynonymView(View):
    template_name = 'synonyms/add_synonym.html'
    def get(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        return render(request, self.template_name, {'bot': bot})
    
    def post(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id)
        synonym_reference = request.POST.get('synonym_reference')
        Synonym.objects.create(synonym_reference=synonym_reference, bot=bot)
        return redirect('bot_detail', bot_id=bot_id)

class EditSynonymView(View):
    template_name = 'synonyms/edit_synonym.html'

    def get(self, request, *args, **kwargs):
        synonym = get_object_or_404(Synonym, pk=kwargs.get('synonym_id'))
        form = SynonymForm(instance=synonym)
        synonym_variants = SynonymVariant.objects.filter(synonym=synonym)
        serializer = SynonymVariantSerializer(synonym_variants, many=True)
        serialized_synonyms = JSONRenderer().render(serializer.data)
        synonyms_json = serialized_synonyms.decode('utf-8')
        return render(request, self.template_name, {'form': form, 'synonym': synonym,'synonym_json': synonyms_json})
    
    def post(self, request, *args, **kwargs):
        synonym = get_object_or_404(Synonym, pk=kwargs.get('synonym_id'))
        form = SynonymForm(request.POST, instance=synonym)
        if form.is_valid():
            form.save()
            return redirect('bot_detail', bot_id=synonym.bot.id)
        return render(request, self.template_name, {'form': form, 'synonym': synonym})
    
def remove_synonym_variant(request, bot_id, synonym_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            synonym_variant_id = data.get('synonym_variant_id')
            synonym_variant = SynonymVariant.objects.get(id=synonym_variant_id)
            synonym_variant.delete()
            return JsonResponse({'message': 'Synonym variant deleted successfully.'}, status=200)
        except SynonymVariant.DoesNotExist:
            return JsonResponse({'error': 'Synonym variant not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def add_synonym_variant(request, bot_id, synonym_id):
    if request.method == 'POST':
        try:
            synonym = Synonym.objects.get(id=synonym_id)
            data = json.loads(request.body)
            synonym_value = data.get('synonym_value')
            synonym_variant = SynonymVariant.objects.create(synonym=synonym, synonym_value=synonym_value)
            serializer = SynonymVariantSerializer(synonym_variant)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def delete_synonym(request, bot_id, synonym_id):
    try:
        synonym = Synonym.objects.get(id=synonym_id)
        synonym.delete()
        return redirect('bot_detail', bot_id=bot_id)
    except Synonym.DoesNotExist:
        return JsonResponse({'error': 'Synonym not found.'}, status=404)
    
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

class TrainingView(View):
    template_name = 'training/training.html'

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        context = {
            'botList': bots,
            'selectedBot': selected_bot,
        }
        return render(request, self.template_name, context)

def load_training_data(request, bot_id):
    # replace with your actual logic for loading training data
    bot = Bot.objects.get(id=bot_id)
    # read file data/config.yml
    config_data = bot.bot_config
    raw_data = ""
    raw_data += config_data

    intents = Intent.objects.filter(bot=bot)
    entities = Entity.objects.filter(bot=bot)
    actions = Action.objects.filter(bot=bot)
    regexes = Regex.objects.filter(bot=bot)
    synonyms = Synonym.objects.filter(bot=bot)
    stories = Story.objects.filter(bot=bot)

    nlu_data = "version: '3.1'\n"
    nlu_data_raw = "nlu:\n"
    for intent in intents:
        nlu_data_raw += "  - intent: " + intent.intent_name + "\n"
        nlu_data_raw += "    examples: |\n"
        expressions = Expression.objects.filter(intent=intent)
        for expression in expressions:
            parameters = ExpressionParameter.objects.filter(expression=expression, intent=intent)
            # sort parameter desc by parameter_start
            parameters = sorted(parameters, key=lambda x: x.parameter_start, reverse=True)
            expression_text = expression.expression_text
            for parameter in parameters:
                parameter_entity = entities.get(id=parameter.entity.id)
                if not parameter_entity:
                    continue
                parameter_value = f"[{parameter.parameter_value}]({parameter_entity.entity_name})"
                expression_text = expression_text[:parameter.parameter_start] + parameter_value + expression_text[parameter.parameter_end:]
            nlu_data_raw += "      - " + expression_text + "\n"
        nlu_data_raw += "\n"
    nlu_data_raw += "\n"
            
    for regex in regexes:
        nlu_data_raw += "  - regex: " + regex.regex_name + "\n"
        nlu_data_raw += "    examples: |\n"
        nlu_data_raw += "      - " + regex.regex_pattern + "\n"

        nlu_data_raw += "\n"

    for synonym in synonyms:
        nlu_data_raw += "  - synonym: " + synonym.synonym_reference + "\n"
        nlu_data_raw += "    examples: |\n"
        synonym_variants = SynonymVariant.objects.filter(synonym=synonym)
        for synonym_variant in synonym_variants:
            nlu_data_raw += "      - " + synonym_variant.synonym_value + "\n"
        nlu_data_raw += "\n"

    nlu_data += nlu_data_raw
    raw_data += nlu_data_raw + "\n"

    stories_data = "version: '3.1'\n"
    stories_data_raw = "stories:\n"
    for story in stories:
        stories_data_raw += "  - story: " + story.story_name + "\n"
        stories_data_raw += "    steps:\n"
        steps = story.story.split("\n")
        for step in steps:
            stories_data_raw += "      " + step + "\n"
        stories_data_raw += "\n"
    stories_data += stories_data_raw
    raw_data += stories_data_raw + "\n"

    domain_data = "version: '3.1'\n"
    domain_data_raw = "intents:\n"
    for intent in intents:
        domain_data_raw += "  - " + intent.intent_name + "\n"
    domain_data_raw += "\n"
    domain_data_raw += "entities:\n"
    for entity in entities:
        domain_data_raw += "  - " + entity.entity_name + "\n"
    domain_data_raw += "\n"
    domain_data_raw += "actions: []\n"
    # for action in actions:
    #     domain_data_raw += "  - " + action.action_name + "\n"
    domain_data_raw += "slots:\n"
    for entity in entities:
        domain_data_raw += "  " + entity.entity_name + ":\n"
        domain_data_raw += "    type: " + entity.slot_data_type + "\n"
    domain_data_raw += "\n"
    domain_data_raw += "responses:\n"
    for action in actions:
        responses = Response.objects.filter(action=action)
        for response in responses:
            domain_data_raw += "  " + action.action_name + ":\n"
            domain_data_raw += "    - text: " + response.response_text + "\n"
        domain_data_raw += "\n"
    domain_data_raw += "\n"
    domain_data_raw += "session_config:\n"
    domain_data_raw += "  session_expiration_time: 60\n"
    domain_data_raw += "  carry_over_slots_to_new_session: true\n"

    domain_data += domain_data_raw
    raw_data += domain_data_raw
    
    data = {
        'raw': raw_data,
        'config': config_data,
        'nlu': nlu_data,
        'stories': stories_data,
        'domain': domain_data
    }
    return JsonResponse(data, status=200)
    


def download_file(request):
    # replace 'filepath' with the actual path to the file you want to serve
    filepath = '/path/to/your/file'
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='your_filename')
class SettingsView(TemplateView):
    template_name = 'settings/settings.html'

class ModelView(View):
    template_name = 'models/models.html'

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        context = {
            'botList': bots,
            'selectedBot': selected_bot,
        }
        return render(request, self.template_name, context)

def load_model(request, server_path):
    # replace with your actual logic for loading a model
    model = ModelModel.objects.get(server_path=server_path)
    model.load()  # assuming you have a method to load the model
    messages.success(request, 'Model loaded successfully.')
    return redirect('models')  # replace with the name of your models page

def delete_model(request, model_id):
    # replace with your actual logic for deleting a model
    model = ModelModel.objects.get(id=model_id)
    model.delete()
    messages.success(request, 'Model deleted successfully.')
    return redirect('models')  # replace with the name of your models page
class AddModelView(TemplateView):
    # Assuming add model view might need a specific template
    template_name = 'models/add_model.html'  # Adjust if there's an actual path

class ResponseView(TemplateView):
    template_name = 'responses/responses.html'

    def get_context_data(self, **kwargs):
        context = super(ResponseView, self).get_context_data(**kwargs)
        bots = Bot.objects.all()
        context['bots'] = bots

        selected_bot_id = self.kwargs.get('bot_id')
        
        if selected_bot_id:
            selected_bot = get_object_or_404(Bot, pk=selected_bot_id)
            actions = Action.objects.filter(bot=selected_bot)
            responses = Response.objects.filter(action__bot=selected_bot)
        else:
            actions = Action.objects.none()  # Tránh lỗi khi không có bot nào được chọn
            responses = Response.objects.none()
        responseType = [
            {
                'id': 'text',
                'type': 'Text'
            },
            {
                'id': 'button',
                'type': 'Button'
            }
        ]
        context= {
            'bots' : bots,
            'selectedBot': selected_bot_id,
            'actionsList': actions,
            'responseList': responses,
            'responseTypeList': responseType
        }
        
        return context
    
def delete_action(request, bot_id):
    try:
        data = json.loads(request.body)
        action_id = data.get('action_id')
        action = Action.objects.get(id=action_id)
        action.delete()
        return JsonResponse({'message': 'Action deleted successfully.'}, status=200)
    except Action.DoesNotExist:
        return JsonResponse({'error': 'Action not found.'}, status=404)
    
def add_response(request, bot_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action_id = data.get('action_id')
            response_text = data.get('response_text')
            response_type = data.get('response_type')
            action = Action.objects.get(id=action_id)
            response = Response.objects.create(
                response_text=response_text,
                response_type=response_type,
                action=action
            )
            serializer = ResponseSerializer(response)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def update_response(request, bot_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_id = data.get('response_id')
            response_text = data.get('response_text')
            response_type = data.get('response_type')
            response = Response.objects.get(id=response_id)
            response.response_text = response_text
            response.response_type = response_type
            response.save()
            serializer = ResponseSerializer(response)
            return JsonResponse(serializer.data, status=200)
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def delete_response(request, bot_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_id = data.get('response_id')
            response = Response.objects.get(id=response_id)
            response.delete()
            return JsonResponse({'message': 'Response deleted successfully.'}, status=200)
        except Response.DoesNotExist:
            return JsonResponse({'error': 'Response not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
class AddActionView(View):
    form_class = ActionForm
    template_name = 'responses/add_action.html'

    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')  # Giả sử bot_id được truyền qua URL
        form = self.form_class(initial={'bot': bot_id})
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        bot_id = kwargs.get('bot_id')  # Giả sử bot_id được truyền qua URL
        if form.is_valid():
            new_action = form.save(commit=False)
            new_action.bot_id = bot_id  # Đặt bot_id cho action mới
            new_action.save()
            return HttpResponseRedirect(reverse('responses', kwargs={'bot_id': bot_id}))
        else:
            return render(request, self.template_name, {'form': form, 'bot_id': bot_id})

class ChatView(TemplateView):
    template_name = 'chat/chat.html'  # Điều chỉnh nếu có đường dẫn thực tế

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        conversations = Conversation.objects.filter(bot=selected_bot)
        context = {
            'botList': bots,
            'bot': selected_bot,
            'conversations': conversations
        }
        # Thêm logic của bạn ở đây
        return render(request, self.template_name, context)
    
class DeleteActionView(View):
    def post(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')
        action_id = kwargs.get('action_id')
        
        # Tìm và xóa action nếu nó tồn tại
        action = get_object_or_404(Action, id=action_id, bot_id=bot_id)
        action.delete()
        
        # Redirect người dùng về trang danh sách các response của bot sau khi xóa
        # Đảm bảo bạn đã định nghĩa 'responses_for_bot' URL pattern trong urls.py
        return redirect('responses', bot_id=bot_id)


class AddResponseToActionView(View):
    form_class = ResponseForm
    template_name = 'responses/add_response.html'
    def get(self, request, bot_id, action_id):
        form = self.form_class()
        return render(request, self.template_name , {'form': form, 'bot_id': bot_id, 'action_id': action_id})

    def post(self, request, bot_id, action_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.action = Action.objects.get(id=action_id)  # Ensure this action exists and you handle potential DoesNotExist exception
            response.save()
            return redirect('responses', bot_id=bot_id)  # Replace 'responses_for_bot' with the actual name of your view that lists responses for a bot
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'action_id': action_id})

class DeleteResponseView(View):
    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')
        response_id = kwargs.get('response_id')
        
        # Tìm và xóa response nếu nó tồn tại
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        response.delete()
        
        # Redirect người dùng về trang danh sách các response của bot sau khi xóa
        # Đảm bảo bạn đã định nghĩa 'responses_for_bot' URL pattern trong urls.py
        return redirect('responses', bot_id=bot_id)


class EditResponseView(View):
    form_class = ResponseForm
    template_name = 'responses/edit_response.html'

    def get(self, request, bot_id, response_id):
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        form = self.form_class(instance=response)
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'response_id': response_id})

    def post(self, request, bot_id, response_id):
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        form = self.form_class(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('responses', bot_id=bot_id)
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'response_id': response_id})