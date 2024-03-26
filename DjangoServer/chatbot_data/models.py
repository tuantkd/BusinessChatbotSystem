import json
from django.db import models
from enum import Enum
class Bot(models.Model):
    bot_name = models.TextField()
    bot_config = models.TextField()
    output_folder = models.TextField()

class Intent(models.Model):
    intent_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='intents')

class Synonym(models.Model):
    synonym_reference = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='synonyms')

class Entity(models.Model):
    entity_name = models.TextField()
    slot_data_type = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='entities')

class Expression(models.Model):
    expression_text = models.TextField()
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='expressions')

class ExpressionParameter(models.Model):
    parameter_start = models.IntegerField()
    parameter_end = models.IntegerField()
    parameter_value = models.TextField()
    expression = models.ForeignKey(Expression, on_delete=models.CASCADE, related_name='parameters')
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='parameters')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='parameters',null=True, blank=True)

class Regex(models.Model):
    regex_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='regexes')

    def __str__(self):
        return self.regex_name
    
class RegexVariant(models.Model):
    regex = models.ForeignKey(Regex, on_delete=models.CASCADE, related_name='variants')
    pattern = models.TextField()
    def __str__(self):
        return f"{self.regex.regex_name}: {self.pattern}"

class Response(models.Model):
    response_text = models.TextField()
    response_type = models.TextField()
    action = models.ForeignKey('Action', on_delete=models.CASCADE)
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

class ActionType(Enum):
    UTTER = "utter"
    ACTION = "action"
    FORM = "form"
    SLOT_SET = "slot_set"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Action(models.Model):
    action_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ActionType.choices(), default=ActionType.UTTER.value)
    action_config = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.action_name
    
class Rule(models.Model):
    rule_name = models.TextField()
    rule_steps = models.TextField()
    timestamp = models.DateTimeField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='rules')

    def __str__(self):
        return self.rule_name
class Lookup(models.Model):
    lookup_name = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='lookups')

    def __str__(self):
        return self.lookup_name
    
class LookupVariant(models.Model):
    lookup = models.ForeignKey(Lookup, on_delete=models.CASCADE, related_name='variants')
    value = models.TextField()

    def __str__(self):
        return f"{self.lookup.lookup_name}: {self.value}"


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