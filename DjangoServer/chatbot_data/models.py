import json
from django.db import models
from django.core.validators import RegexValidator
from enum import Enum
class Bot(models.Model):
    bot_name = models.TextField()
    bot_config = models.TextField()
    output_folder = models.TextField()

class Intent(models.Model):
    intent_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

class Synonym(models.Model):
    synonym_reference = models.TextField()
    regex_pattern = models.TextField(blank=True, null=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

class Entity(models.Model):
    entity_name = models.TextField()
    slot_data_type = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

class Expression(models.Model):
    expression_text = models.TextField()
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)

class ExpressionParameter(models.Model):
    parameter_start = models.IntegerField()
    parameter_end = models.IntegerField()
    parameter_value = models.TextField()
    expression = models.ForeignKey(Expression, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

class Regex(models.Model):
    regex_name = models.TextField()
    regex_pattern = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

class Response(models.Model):
    response_text = models.TextField()
    response_type = models.TextField()
    # Assuming Action model is defined elsewhere
    action = models.ForeignKey('Action', on_delete=models.CASCADE)
        

        # Add more response types as needed


class SynonymVariant(models.Model):
    synonym_value = models.TextField()
    synonym = models.ForeignKey(Synonym, on_delete=models.CASCADE)

class NluLog(models.Model):
    ip_address = models.TextField()
    query = models.TextField()
    event_type = models.TextField()
    event_data = models.TextField()
    timestamp = models.DateTimeField()

class ModelModel(models.Model):
    model_name = models.TextField()
    timestamp = models.DateTimeField()
    comment = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    local_path = models.TextField()
    server_path = models.TextField()
    server_response = models.TextField()

class Action(models.Model):
    action_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

class Story(models.Model):
    story_name = models.TextField()
    story = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Conversation(models.Model):
    ip_address = models.TextField(blank=True, null=True)
    conversation = models.TextField()
    story = models.TextField(blank=True, null=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Settings(models.Model):
    setting_name = models.TextField(unique=True)
    setting_value = models.TextField()