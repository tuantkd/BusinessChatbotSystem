from datetime import datetime, timezone
import json
import os
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg') 
import seaborn as sns
import numpy as np
import re
import zipfile
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponse, HttpResponseServerError, JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
import requests
from rest_framework.renderers import JSONRenderer
from django.apps import apps
from enterprise_registration_app import settings
from .serializers import ExpressionParameterSerializer, LookupVariantSerializer, RegexVariantSerializer, ResponseSerializer, SynonymVariantSerializer
from .models import Bot, Action, ChatUser, Entity, Expression, ExpressionParameter, History, Intent, Lookup, LookupVariant, Regex, RegexVariant, Response, Rule, Story, ModelModel, Conversation, Synonym, SynonymVariant, Test, TestResult
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BotForm, ImportBotForm, ActionForm, IntentForm, LookupForm, RegexForm, ResponseForm, RuleForm, StoryForm, EntityForm, SynonymForm
from django.shortcuts import redirect
from django.contrib import messages
from enterprise_registration_app.settings import RASA_PREDICT_URL, RASA_TEST_INTENTS_ENDPOINT, RASA_TEST_STORIES_ENDPOINT, RASA_TRAINING_URL
import yaml
from django.db import transaction
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
class BotsView(TemplateView):
    template_name = 'bots/bots.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bots = Bot.objects.all()
        paginator = Paginator(bots, 5)
        page = self.request.GET.get('page', 1)
        context['botList'] = paginator.get_page(page)
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
        intent_paginator = Paginator(bot.intents.all(), 5)
        entity_paginator = Paginator(bot.entities.all(), 5)
        synonym_paginator = Paginator(bot.synonyms.all(), 5)
        regex_paginator = Paginator(bot.regexes.all(), 5)
        lookup_paginator = Paginator(bot.lookups.all(), 5)
        
        intent_page = request.GET.get('intent_page', 1)
        entity_page = request.GET.get('entity_page', 1)
        synonym_page = request.GET.get('synonym_page', 1)
        regex_page = request.GET.get('regex_page', 1)
        lookup_page = request.GET.get('lookup_page', 1)

        # Render template kèm theo form và các danh sách
        return render(request, self.template_name, {
            'form': form,
            'bot': bot,
            'intents': intent_paginator.get_page(intent_page),
            'entities': entity_paginator.get_page(entity_page),
            'synonyms': synonym_paginator.get_page(synonym_page),
            'regexes': regex_paginator.get_page(regex_page),
            'lookups': lookup_paginator.get_page(lookup_page),
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
class ImportNLUView(View):
    form_class = ImportBotForm
    template_name = 'bots/import_bot.html'  # Đường dẫn đến template của bạn

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = Bot.objects.get(id=bot_id) if bot_id else None
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'bot': bot})

def import_nlu(request, bot_id):
    try:
        with transaction.atomic():
            bot = Bot.objects.get(id=bot_id) if bot_id else None
            if not bot:
                raise Exception('Bot not found')
            
            intents = bot.intents.all()
            entities = bot.entities.all()
            synonyms = bot.synonyms.all()
            regexes = bot.regexes.all()
            lookups = bot.lookups.all()

            if len(intents) > 0 or len(entities) > 0 or len(synonyms) > 0 or len(regexes) > 0 or len(lookups) > 0:
                raise Exception('Bot already has NLU data. Please clear the data before importing new data.')
            
            bot_file = request.FILES['file']
            bot_data = yaml.safe_load(bot_file)
            
            for data in bot_data['nlu']:
                if 'intent' in data:
                    # create new intent
                    intent_name = data['intent']
                    intent_find = Intent.objects.filter(intent_name=intent_name, bot=bot).first()
                    if not intent_find:
                        new_intent = Intent.objects.create(
                            intent_name=intent_name,
                            bot=bot
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
                            entity_find = Entity.objects.filter(entity_name=entity['entity'], bot=bot).first()
                            if not entity_find:
                                new_entity = Entity.objects.create(entity_name=entity['entity'], bot=bot, slot_data_type='text')
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
                    regex_name = regex_name.strip()
                    if regex_name == '':
                        continue
                    # check if regex not exist in database, create new regex
                    regex_find = Regex.objects.filter(regex_name=regex_name, bot=bot).first()
                    if not regex_find:
                        new_regex = Regex.objects.create(
                            regex_name=regex_name,
                            bot=bot
                        )
                    else:
                        new_regex = regex_find
                    regex_variants = data['examples'].split('\n')
                    for regex_variant in regex_variants:
                        regex_variant = re.sub(r'^\s*-\s*', '', regex_variant)
                        regex_variant = regex_variant.strip()
                        if regex_variant == '':
                            continue
                        regex_variant_find = RegexVariant.objects.filter(regex=new_regex, pattern=regex_variant).first()
                        if not regex_variant_find:
                            new_regex_variant = RegexVariant.objects.create(
                                regex=new_regex,
                                pattern=regex_variant
                            )
                        
                elif 'synonym' in data:
                    synonym_reference = data['synonym']
                    synonym_reference = synonym_reference.strip()
                    if synonym_reference == '':
                        continue
                    synonym_variants = data['examples'].split('\n')
                    # check if synonym not exist in database, create new synonym
                    synonym_find = Synonym.objects.filter(synonym_reference=synonym_reference, bot=bot).first()
                    if not synonym_find:
                        new_synonym = Synonym.objects.create(
                            synonym_reference=synonym_reference,
                            bot=bot
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
                elif 'lookup' in data:
                    lookup_name = data['lookup']
                    lookup_name = lookup_name.strip()
                    if lookup_name == '':
                        continue
                    lookup_find = Lookup.objects.filter(lookup_name=lookup_name, bot=bot).first()
                    if not lookup_find:
                        new_lookup = Lookup.objects.create(
                            lookup_name=lookup_name,
                            bot=bot
                        )
                    else:
                        new_lookup = lookup_find
                    lookup_variants = data['examples'].split('\n')
                    for lookup_variant in lookup_variants:
                        lookup_variant = re.sub(r'^\s*-\s*', '', lookup_variant)
                        lookup_variant = lookup_variant.strip()
                        if lookup_variant == '':
                            continue
                        lookup_variant_find = LookupVariant.objects.filter(lookup=new_lookup, lookup_value=lookup_variant).first()
                        if not lookup_variant_find:
                            new_lookup_variant = LookupVariant.objects.create(
                                lookup=new_lookup,
                                value=lookup_variant
                            )

        return redirect('bot_detail', bot_id=bot_id)

    except Exception as e:
        messages.error(request, 'Error importing bot: ' + str(e))
        return redirect('import_bot', bot_id=bot_id)

def clear_nlu_data(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    bot.intents.all().delete()
    bot.entities.all().delete()
    bot.synonyms.all().delete()
    bot.regexes.all().delete()
    bot.lookups.all().delete()
    return redirect('bot_detail', bot_id=bot_id)

def import_response(request, bot_id):
    try:
        bot = Bot.objects.get(id=bot_id)
        response_file = request.FILES['file']
        response_data = yaml.safe_load(response_file)
        for action_name in response_data['responses']:
            action = Action.objects.filter(action_name=action_name, bot=bot).first()
            if not action:
                action = Action.objects.create(action_name=action_name, action_type='utter', bot=bot)

            for res in response_data['responses'][action_name]:
                response = Response.objects.filter(action=action, response_type='text', response_text=res['text']).first()
                if not response:
                    response = Response.objects.create(
                        response_text=res['text'],
                        response_type='text',
                        action=action
                    )

        for action_name in response_data['actions']:
            action = Action.objects.filter(action_name=action_name, action_type='action', bot=bot).first()
            if not action:
                action = Action.objects.create(action_name=action_name, action_type='action', bot=bot)
                
        for action_name in response_data['slots']:
            action = Action.objects.filter(action_name=action_name, action_type='slot_set', bot=bot).first()
            if not action:
                action = Action.objects.create(action_name=action_name, action_type='slot_set', bot=bot)
            
            slots_yaml = yaml.dump(response_data['slots'][action_name])
            action.action_config = slots_yaml
            action.save()
    
        return redirect('responses', bot_id=bot_id)
    except Exception as e:
        messages.error(request, 'Error importing responses: ' + str(e))
        return redirect('bot_detail', bot_id=bot_id)
    
def clear_response(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    actions = Action.objects.filter(bot=bot)
    actions.delete()
    return redirect('bot_detail', bot_id=bot_id)

def import_story(request, bot_id):
    try:
        bot = Bot.objects.get(id=bot_id)
        story_file = request.FILES['file']
        story_data = yaml.safe_load(story_file)
        for sto in story_data['stories']:
            story_name = sto['story']
            story = Story.objects.filter(story_name=story_name, bot=bot).first()
            if not story:
                story = Story.objects.create(story_name=story_name, bot=bot, timestamp=datetime.now(timezone.utc))
            story_steps = sto['steps']
            story_text = ''
            for step in story_steps:
                if 'intent' in step:
                    intent_name = step['intent']
                    intent = Intent.objects.filter(intent_name=intent_name, bot=bot).first()
                    if not intent:
                        intent = Intent.objects.create(intent_name=intent_name, bot=bot)
                    story_text += f'- intent: {step["intent"]}\n'
                    if 'entities' in step:
                        entities = step['entities']
                        for en in entities:
                            entity = Entity.objects.filter(entity_name=en, bot=bot).first()
                            if not entity:
                                entity = Entity.objects.create(entity_name=en, bot=bot, slot_data_type='text')
                            story_text += f'  - {en}\n'
                elif 'action' in step:
                    action_name = step['action']
                    action = Action.objects.filter(action_name=action_name, bot=bot).first()
                    if not action:
                        action = Action.objects.create(action_name=action_name, action_type='action', bot=bot)
                    story_text += f'- action: {step["action"]}\n'

            story.story = story_text
            story.save()
        return redirect('stories', bot_id=bot_id)
    except Exception as e:
        messages.error(request, 'Error importing stories: ' + str(e))
        return redirect('bot_detail', bot_id=bot_id)
    
def clear_story(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    stories = Story.objects.filter(bot=bot)
    stories.delete()
    return redirect('bot_detail', bot_id=bot_id)

def import_rule(request, bot_id):
    try:
        bot = Bot.objects.get(id=bot_id)
        rule_file = request.FILES['file']
        rule_data = yaml.safe_load(rule_file)
        for ru in rule_data['rules']:
            rule_name = ru['rule']
            rule = Rule.objects.filter(rule_name=rule_name, bot=bot).first()
            if not rule:
                rule = Rule.objects.create(rule_name=rule_name, bot=bot, timestamp=datetime.now(timezone.utc))
            rule_steps = ru['steps']
            rule_text = ''
            for step in rule_steps:
                if 'intent' in step:
                    intent_name = step['intent']
                    intent = Intent.objects.filter(intent_name=intent_name, bot=bot).first()
                    if not intent:
                        intent = Intent.objects.create(intent_name=intent_name, bot=bot)
                    rule_text += f'- intent: {step["intent"]}\n'
                    if 'entities' in step:
                        entities = step['entities']
                        for en in entities:
                            entity = Entity.objects.filter(entity_name=en, bot=bot).first()
                            if not entity:
                                entity = Entity.objects.create(entity_name=en, bot=bot, slot_data_type='text')
                            rule_text += f'  - {en}\n'
                elif 'action' in step:
                    action_name = step['action']
                    action = Action.objects.filter(action_name=action_name, bot=bot).first()
                    if not action:
                        action = Action.objects.create(action_name=action_name, action_type='action', bot=bot)
                    rule_text += f'- action: {step["action"]}\n'

            rule.rule_steps = rule_text
            rule.save()
        return redirect('rules', bot_id=bot_id)
    except Exception as e:
        messages.error(request, 'Error importing rules: ' + str(e))
        return redirect('bot_detail', bot_id=bot_id)
    
def clear_rule(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    rules = Rule.objects.filter(bot=bot)
    rules.delete()
    return redirect('bot_detail', bot_id=bot_id)

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
        paginator = Paginator(intent.expressions.all(), 5)
        page = request.GET.get('page', 1)

        context = {
            'form': form,
            'bot': bot,
            'intent': intent,
            'entity_list': bot.entities.all(),
            'expression_list': paginator.get_page(page),
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
        paginator = Paginator(stories, 5)
        page = request.GET.get('page', 1)
        stories = paginator.get_page(page)
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

class RulesView(View):
    template_name = 'rules/rules.html'

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        rules = Rule.objects.filter(bot_id=bot_id) if bot_id else []
        bots = Bot.objects.all()
        selected_bot = Bot.objects.get(pk=bot_id) if bot_id else None
        selected_bot_id = selected_bot.id if selected_bot else 0
        paginator = Paginator(rules, 5)
        page = request.GET.get('page', 1)
        rules = paginator.get_page(page)
        return render(request, self.template_name, {'ruleList': rules, 'botList': bots, 'selectedBot': selected_bot_id})

    def post(self, request, *args, **kwargs):
        # This method would be used if you're creating a rule via a form submission
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rules_view')
        return render(request, self.template_name, {'form': form})
    
class AddRuleView(View):
    template_name = 'rules/add_rule.html'

    def get(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        default_name = "rule_" + str(int(time.mktime(datetime.now().timetuple())))
        return render(request, self.template_name, {'bot': bot, 'rule_name': default_name})
    
    def post(self, request, bot_id, *args, **kwargs):
        bot = Bot.objects.get(id=bot_id)
        rule_name = request.POST.get('rule_name')
        Rule.objects.create(bot=bot, rule_name=rule_name, timestamp=datetime.now(timezone.utc))
        return redirect('rules', bot_id=bot_id)
    
class EditRuleView(View):
    template_name = 'rules/edit_rule.html'

    def get(self, request, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=kwargs.get('rule_id'))
        bot_id = rule.bot.id
        bot = Bot.objects.get(id=bot_id)
        form = RuleForm(instance=rule)
        return render(request, self.template_name, {'form': form, 'rule': rule, 'bot': bot})
    
    def post(self, request, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=kwargs.get('rule_id'))
        form = RuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('rules', bot_id=rule.bot.id)
        return render(request, self.template_name, {'form': form, 'rule': rule})
    
class RuleDetailView(View):
    template_name = 'rules/rule_detail.html'

    def get(self, request, rule_id, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=rule_id)
        return render(request, self.template_name, {'rule': rule})
    
        
def delete_rule(request, bot_id, rule_id):
    try:
        rule = Rule.objects.get(id=rule_id)
        rule.delete()
        return redirect('rules', bot_id=bot_id)
    except Rule.DoesNotExist:
        return JsonResponse({'error': 'Rule not found.'}, status=404)
    
def save_rule_step(request, bot_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_id = data.get('rule_id')
        rule_text = data.get('yaml_text')
        rule = Rule.objects.get(id=rule_id)
        rule.rule = rule_text
        rule.save()
        return JsonResponse({'message': 'Rule saved successfully.'}, status=200)
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
        return render(request, self.template_name, {'form': form, 'entity': entity, 'bot': entity.bot})
    
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
        return render(request, self.template_name, {'form': form, 'lookup': lookup, 'lookup_values_json': lookups_json, 'bot': lookup.bot})
    
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
        return render(request, self.template_name, {'form': form, 'synonym': synonym,'synonym_json': synonyms_json, 'bot':synonym.bot})
    
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

@method_decorator(csrf_exempt, name='dispatch')
class HistoryView(View):
    template_name = 'history/history.html'

    def get(self, request, *args, **kwargs):
        history = History.objects.order_by('-timestamp').all()
        chat_users = ChatUser.objects.all()
        history = [{
                    'sender_id': h.sender_id,
                    'sender_name': chat_users.get(sender_id=h.sender_id).sender_name,
                    'timestamp': h.timestamp,
                    'user_say': h.user_say,
                    'response': h.response,
                    'intent': h.intent,
                    'confidence': h.confidence,
                    'entities': json.loads(h.entities.replace("'", "\"")),
                    'slot_values': json.loads(h.slot_values.replace("'", "\"").replace("True", "true").replace("False", "false").replace("None", "null")),
                    } for h in history]
        paginator = Paginator(history, 5)
        page = request.GET.get('page', 1)
        history = paginator.get_page(page)
        return render(request, self.template_name, {'historyList': history})
    
class UsersView(View):
    template_name = 'users/users.html'

    def get(self, request, *args, **kwargs):
        chat_users = ChatUser.objects.all()
        paginator = Paginator(chat_users, 5)
        page = request.GET.get('page', 1)
        chat_users = paginator.get_page(page)
        return render(request, self.template_name, {'userList': chat_users})

class ConversationView(TemplateView):
    # Assuming conversation view might need a specific template
    template_name = 'conversation/conversation.html'  # Adjust if there's an actual path

class InsightsView(TemplateView):
    template_name = 'insights/insights.html'

@csrf_exempt
def rasa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process the data from Rasa
            # For example, update the model information in your database
            # You can access the training result or error message from `data`
            
            # Log or handle the callback data as needed
            print("Rasa callback data:", data)

            # Return a success response
            return JsonResponse({"status": "success", "message": "Callback received successfully"})

        except Exception as e:
            # Log the error
            print("Error processing Rasa callback:", e)
            return HttpResponse(status=400, content="Error processing callback")
    
    # If not POST request, return 405 Method Not Allowed
    return HttpResponse(status=405, content="Method not allowed")

class TrainingView(View):
    template_name = 'training/training.html'

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id') 
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        raw_data = get_training_data(bot_id) if bot_id else ""
        context = {
            'botList': bots,
            'selectedBot': selected_bot,
            'rawData': raw_data
        }
        return render(request, self.template_name, context)
    

def get_training_data(bot_id):
    # replace with your actual logic for loading training data
    bot = Bot.objects.get(id=bot_id)
    # read file data/config.yml
    config_data = bot.bot_config
    raw_data = ""
    raw_data += config_data + "\n"

    intents = Intent.objects.filter(bot=bot)
    entities = Entity.objects.filter(bot=bot)
    actions = Action.objects.filter(bot=bot)
    regexes = Regex.objects.filter(bot=bot)
    synonyms = Synonym.objects.filter(bot=bot)
    lookup_tables = Lookup.objects.filter(bot=bot)
    stories = Story.objects.filter(bot=bot)
    rules = Rule.objects.filter(bot=bot)

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
        regex_variants = RegexVariant.objects.filter(regex=regex)
        for regex_variant in regex_variants:
            nlu_data_raw += "      - " + regex_variant.pattern + "\n"
        nlu_data_raw += "\n"
    nlu_data_raw += "\n"

    for synonym in synonyms:
        nlu_data_raw += "  - synonym: " + synonym.synonym_reference + "\n"
        nlu_data_raw += "    examples: |\n"
        synonym_variants = SynonymVariant.objects.filter(synonym=synonym)
        for synonym_variant in synonym_variants:
            nlu_data_raw += "      - " + synonym_variant.synonym_value + "\n"
        nlu_data_raw += "\n"
    nlu_data_raw += "\n"

    for lookup_table in lookup_tables:
        nlu_data_raw += "  - lookup: " + lookup_table.lookup_name + "\n"
        nlu_data_raw += "    examples: |\n"
        lookup_variants = LookupVariant.objects.filter(lookup=lookup_table)
        for lookup_variant in lookup_variants:
            nlu_data_raw += "      - " + lookup_variant.value + "\n"
        nlu_data_raw += "\n"
    nlu_data_raw += "\n"

    nlu_data += nlu_data_raw
    raw_data += nlu_data_raw

    stories_data = "version: '3.1'\n"
    stories_data_raw = "stories:\n"
    for story in stories:
        stories_data_raw += "  - story: " + story.story_name + "\n"
        stories_data_raw += "    steps:\n"
        steps = story.story.split("\n")
        for step in steps:
            stories_data_raw += "      " + step + "\n"
        stories_data_raw += "\n"
    stories_data_raw += "\n"

    stories_data += stories_data_raw
    raw_data += stories_data_raw

    rules_data = "version: '3.1'\n"
    rules_data_raw = "rules:\n"
    for rule in rules:
        rules_data_raw += "  - rule: " + rule.rule_name + "\n"
        rules_data_raw += "    steps:\n"
        steps = rule.rule_steps.split("\n")
        for step in steps:
            rules_data_raw += "    " + step + "\n"
        rules_data_raw += "\n"
    rules_data_raw += "\n"

    rules_data += rules_data_raw
    raw_data += rules_data_raw

    domain_data = "version: '3.1'\n"
    domain_data_raw = "intents:\n"
    for intent in intents:
        domain_data_raw += "  - " + intent.intent_name + "\n"
    domain_data_raw += "\n"

    domain_data_raw += "responses:\n"
    for action in actions:
        if action.action_type != 'utter':
            continue
        responses = Response.objects.filter(action=action)
        domain_data_raw += "  " + action.action_name + ":\n"
        for response in responses:
            response_texts = response.response_text.split("\n")
            if len(response_texts) >= 1:
                domain_data_raw += "    - text: |\n"
                for response_text in response_texts:
                    response_text = response_text.strip()
                    if response_text == "":
                        continue
                    domain_data_raw += "        " + response_text + "\n"
            
        domain_data_raw += "\n"
    domain_data_raw += "\n"

    domain_data_raw += "entities:\n"
    for entity in entities:
        domain_data_raw += "  - " + entity.entity_name + "\n"
    domain_data_raw += "\n"

    domain_data_raw += "actions:\n"
    for action in actions:
        if action.action_type == 'action':
            domain_data_raw += "  - " + action.action_name + "\n"
    domain_data_raw += "\n"

    domain_data_raw += "slots:\n"
    for action in actions:
        if action.action_type != 'slot_set':
            continue
        domain_data_raw += "  " + action.action_name + ":\n"
        config = action.action_config.split("\n")
        for conf in config:
            domain_data_raw += "    " + conf + "\n"
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
        'rules': rules_data,
        'stories': stories_data,
        'domain': domain_data
    }
    return data

def load_training_data(request, bot_id):
    return JsonResponse(get_training_data(bot_id), status=200)
    
def create_yml_files(data, folder_path):
    for file_name, file_content in data.items():
        path = os.path.join(folder_path, f"{file_name}.yml")
        with open(path, 'w', encoding='utf-8') as file:
            file.write(file_content)

def zip_files(folder_path, zip_name):
    zip_path = os.path.join(folder_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.yml'):
                    zipf.write(os.path.join(root, file), arcname=file)
    return zip_path

def download_zip(request, bot_id):
    yml_data = get_training_data(bot_id)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, 'rasadownload')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    create_yml_files(yml_data, folder_path)

    data_time = datetime.now().strftime('%Y%m%d%H%M%S')
    zip_name = 'rasa_files_' + data_time + '.zip'
    zip_path = zip_files(folder_path, zip_name)

    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(zip_path)
            return response
    return HttpResponse("Không tìm thấy file")

def train_model(request, bot_id):
    # replace with your actual logic for training a model
    bot = Bot.objects.get(id=bot_id)
    data = json.loads(request.body)
    raw_data = data.get('raw_data')
    force_training = data.get('force_training')

    model_name = f"{bot.bot_name}_model_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(current_dir, 'rasamodels')
    force_training = 'true' if force_training == 'true' else 'false'
    comment = data.get('comment')
    # generate model name
    
    headers = {'Content-Type': 'application/x-yaml', 'filename': model_name}
    url = RASA_TRAINING_URL 
    response = requests.post(url, data=raw_data, headers=headers)

    filename = response.headers.get('filename')
    file_path = os.path.join(local_path, filename)
    with open(file_path, 'wb') as f:
        f.write(response.content)
        
    if response.status_code == 200:
        newModel = ModelModel.objects.create(
            model_name=filename,
            server_path=url,
            local_path=local_path,
            comment=comment,
            server_response="available",
            timestamp=datetime.now(),
            bot=bot
        )
    
    messages.success(request, 'Model trained successfully.')
    return redirect('training', bot_id=bot_id)

    

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
        model_list = ModelModel.objects.filter(bot=bot_id) if bot_id else []
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        context = {
            'botList': bots,
            'selectedBot': selected_bot,
            "modelList": model_list
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

        paginator = Paginator(actions, 5)
        page = self.request.GET.get('page')
        
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
            'actionsList': paginator.get_page(page),
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
        bot = Bot.objects.get(id=bot_id)
        action = Action.objects.filter(bot=bot)
        return render(request, self.template_name, {'form': form, 'bot': bot})

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

class EditActionView(View):
    form_class = ActionForm
    template_name = 'responses/edit_action.html'

    def get(self, request, *args, **kwargs):
        action = get_object_or_404(Action, pk=kwargs.get('action_id'))
        form = self.form_class(instance=action)
        return render(request, self.template_name, {'form': form, 'action': action})

    def post(self, request, *args, **kwargs):
        action = get_object_or_404(Action, pk=kwargs.get('action_id'))
        form = self.form_class(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect('responses', bot_id=action.bot.id)
        return render(request, self.template_name, {'form': form, 'action': action})
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
    
def generate_charts(result_data):
        # Get the static directory path of the current app
        app_config = apps.get_app_config('chatbot_data')
        static_dir = os.path.join(app_config.path, 'static', app_config.label, 'images')

        # Ensure the directory exists
        os.makedirs(static_dir, exist_ok=True)

        # Generate the confidence chart
        predictions = result_data['intent_evaluation']['predictions']
        correct_confidences = [p['confidence'] for p in predictions if p['intent'] == p['predicted']]
        incorrect_confidences = [p['confidence'] for p in predictions if p['intent'] != p['predicted']]

        plt.figure(figsize=(10, 6))
        plt.hist([correct_confidences, incorrect_confidences], bins=np.linspace(0, 1, 20), stacked=True, label=['Câu dự đoán đúng', 'Câu dự đoán sai'], color=['#00bfff', '#8b0000'])
        plt.xlabel('Độ tin cậy (Confidence)')
        plt.ylabel('Số câu mẫu')
        plt.legend()
        datetime_name = datetime.now().strftime('%Y%m%d%H%M%S')
        chart1_path = os.path.join(static_dir, f'chart1_{datetime_name}.png')
        plt.savefig(chart1_path)
        plt.close()

        # Generate the confusion matrix
        report = result_data['intent_evaluation']['report']
        labels = [key for key in report.keys() if isinstance(report[key], dict)]  # Ensure only keys with dictionary values
        confusion_matrix = np.zeros((len(labels), len(labels)))

        for i, label in enumerate(labels):
            for j, predicted_label in enumerate(labels):
                confusion_matrix[i, j] = report[label].get('confused_with', {}).get(predicted_label, 0)

        plt.figure(figsize=(8, 8))
        sns.heatmap(confusion_matrix, annot=True, fmt='g', xticklabels=labels, yticklabels=labels, cmap='Blues')
        plt.xlabel('Nhận dự đoán')
        plt.ylabel('Nhận đúng')
        chart2_path = os.path.join(static_dir, f'chart2_{datetime_name}.png')
        plt.savefig(chart2_path)
        plt.close()

        # Return the relative paths for use in the template
        return (
            os.path.join(app_config.label, 'images', f'chart1_{datetime_name}.png'),
            os.path.join(app_config.label, 'images', f'chart2_{datetime_name}.png')
        )
class TestListView(View):
    template_name = 'test/test_list.html'

    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        return render(request, self.template_name, {'tests': tests})

    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = f.read()

            # Create a new Test instance
            test = Test(content=yaml_data)
            test.save()

            # Make a request to the Rasa server
            response = requests.post(RASA_TEST_INTENTS_ENDPOINT, data=yaml_data, headers={'Content-Type': 'application/x-yaml'})

            if response.status_code == 200:
                result_data = response.json()
                # Create a new TestResult instance
                test_result = TestResult(test=test, result=result_data)
                test_result.save()
                return JsonResponse({'test_id': test.id}, safe=False)
            else:
                return JsonResponse({'error': 'Failed to test intents'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

class TestView(View):
    template_name = 'test/test.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = f.read()

            # Create a new Test instance
            test = Test(content=yaml_data, type='intent')
            test.save()

            # Make a request to the Rasa server
            response = requests.post(RASA_TEST_INTENTS_ENDPOINT, data=yaml_data, headers={'Content-Type': 'application/x-yaml'})

            if response.status_code == 200:
                result_data = response.json()
                # Create a new TestResult instance
                chart1_path, chart2_path = generate_charts(result_data)
                test_result = TestResult(test=test, result=result_data, chart1_path=chart1_path, chart2_path=chart2_path)
                test_result.save()
                return JsonResponse(result_data, safe=False)
            else:
                return JsonResponse({'error': 'Failed to test intents'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)


class TestResultView(View):
    template_name = 'test/test_result.html'

    def get(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        try:
            test_result = TestResult.objects.get(test=test)
            result_data = test_result.result
        except TestResult.DoesNotExist:
            result_data = None
        if result_data:
            result_data['chart1_path'] = test_result.chart1_path
            result_data['chart2_path'] = test_result.chart2_path

        return render(request, self.template_name, {'test': test, 'test_result': result_data})

class RetestView(View):
    def post(self, request, test_id):
        test = get_object_or_404(Test, pk=test_id)
        response = requests.post(RASA_TEST_INTENTS_ENDPOINT, data=test.content, headers={'Content-Type': 'application/x-yaml'})

        if response.status_code == 200:
            result_data = response.json()
            
            chart1_path, chart2_path = generate_charts(result_data)
            test_result, created = TestResult.objects.update_or_create(
                test=test,
                defaults={'result': result_data, 'chart1_path': chart1_path, 'chart2_path': chart2_path}
            )
            return JsonResponse({'test_result': result_data}, safe=False)
        else:
            return JsonResponse({'error': 'Failed to re-test intents'}, status=response.status_code)

    

class RenameTestView(View):
    def post(self, request, test_id):
        test = get_object_or_404(Test, pk=test_id)
        new_name = request.POST.get('test_name')
        test.name = new_name
        test.save()
        return redirect('test_result', test_id=test_id)

class TestStoryView(View):
    template_name = 'test/test_list.html'

    def post(self, request, *args, **kwargs):
        if 'story_file' in request.FILES:
            file = request.FILES['story_file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = f.read()

            response = requests.post(RASA_TEST_STORIES_ENDPOINT, data=yaml_data, headers={'Content-Type': 'application/x-yaml'})

            if response.status_code == 200:
                test_name = f"Story Test {file.name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                test = Test.objects.create(name=test_name, content=yaml_data, type='story')
                result_data = response.json()
                # chart1_path, chart2_path = generate_charts(result_data)
                TestResult.objects.create(test=test, result=result_data, chart1_path="chart1_path", chart2_path="chart2_path")
                return redirect('test_result', test_id=test.id)
            else:
                return JsonResponse({'error': 'Failed to test stories'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)


class DeleteTestView(View):
    def post(self, request, test_id):
        test = get_object_or_404(Test, pk=test_id)
        test.delete()
        return JsonResponse({'success': True})

def generate_story_charts(result_data):
    app_config = apps.get_app_config('chatbot_data')
    static_dir = os.path.join(app_config.path, 'static', app_config.label, 'images')
    os.makedirs(static_dir, exist_ok=True)

    # Generate confidence chart
    actions = result_data['actions']
    correct_confidences = [a['confidence'] for a in actions if a['action'] == a['predicted']]
    incorrect_confidences = [a['confidence'] for a in actions if a['action'] != a['predicted']]

    plt.figure(figsize=(10, 6))
    plt.hist([correct_confidences, incorrect_confidences], bins=np.linspace(0, 1, 20), stacked=True, label=['Correct Predictions', 'Incorrect Predictions'], color=['#00bfff', '#8b0000'])
    plt.xlabel('Confidence')
    plt.ylabel('Number of Actions')
    plt.legend()
    datetime_name = datetime.now().strftime('%Y%m%d%H%M%S')
    chart1_path = os.path.join(static_dir, f'chart1_story_{datetime_name}.png')
    plt.savefig(chart1_path)
    plt.close()

    # Generate confusion matrix
    report = result_data['report']
    labels = [key for key in report.keys() if isinstance(report[key], dict)]
    confusion_matrix = np.zeros((len(labels), len(labels)))

    for i, label in enumerate(labels):
        for j, predicted_label in enumerate(labels):
            confusion_matrix[i, j] = report[label].get('confused_with', {}).get(predicted_label, 0)

    plt.figure(figsize=(8, 8))
    sns.heatmap(confusion_matrix, annot=True, fmt='g', xticklabels=labels, yticklabels=labels, cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    chart2_path = os.path.join(static_dir, f'chart2_story_{datetime_name}.png')
    plt.savefig(chart2_path)
    plt.close()

    return (
        os.path.join(app_config.label, 'images', f'chart1_story_{datetime_name}.png'),
        os.path.join(app_config.label, 'images', f'chart2_story_{datetime_name}.png')
    )
class TestStoryResultView(View):
    template_name = 'test/test_story_result.html'

    def get(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        try:
            test_result = TestResult.objects.get(test=test)
            result_data = test_result.result
        except TestResult.DoesNotExist:
            result_data = None
        
        if result_data:
            chart1_path, chart2_path = generate_story_charts(result_data)
        else:
            chart1_path, chart2_path = None, None
        
        return render(request, self.template_name, {
            'test': test,
            'test_result': result_data,
            'chart1_path': chart1_path,
            'chart2_path': chart2_path
        })
    
class RenameTestView(View):
    def post(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        new_name = request.POST.get('new_name')
        if new_name:
            test.name = new_name
            test.save()
        return redirect('test_story_result', test_id=test.id)

class RetestStoryView(View):
    def post(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        
        response = requests.post(RASA_TEST_STORIES_ENDPOINT, data=test.content, headers={'Content-Type': 'application/x-yaml'})
        
        if response.status_code == 200:
            result_data = response.json()
            chart1_path, chart2_path = generate_story_charts(result_data)
            test_result, created = TestResult.objects.update_or_create(
                test=test,
                defaults={'result': result_data, 'chart1_path': chart1_path, 'chart2_path': chart2_path}
            )
            return redirect('test_story_result', test_id=test.id)
        else:
            return JsonResponse({'error': 'Failed to re-test stories'}, status=response.status_code)