from datetime import datetime
from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _

class Bot(models.Model):
    bot_name = models.TextField(_("Bot Name"))
    bot_config = models.TextField(_("Bot Config"))
    output_folder = models.TextField(_("Output Folder"))

    class Meta:
        verbose_name = _("Bot")
        verbose_name_plural = _("Bots")

class Intent(models.Model):
    intent_name = models.TextField(_("Intent Name"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='intents', verbose_name=_("Bot"))

    class Meta:
        verbose_name = _("Intent")
        verbose_name_plural = _("Intents")

class Synonym(models.Model):
    synonym_reference = models.TextField(_("Synonym Reference"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='synonyms', verbose_name=_("Bot"))

    class Meta:
        verbose_name = _("Synonym")
        verbose_name_plural = _("Synonyms")

class Entity(models.Model):
    entity_name = models.TextField(_("Entity Name"))
    slot_data_type = models.TextField(_("Slot Data Type"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='entities', verbose_name=_("Bot"))

    class Meta:
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")

class Expression(models.Model):
    expression_text = models.TextField(_("Expression Text"))
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='expressions', verbose_name=_("Intent"))
    is_train = models.BooleanField(default=True, verbose_name=_("Is Train"))

    class Meta:
        verbose_name = _("Expression")
        verbose_name_plural = _("Expressions")

class ExpressionParameter(models.Model):
    parameter_start = models.IntegerField(_("Parameter Start"))
    parameter_end = models.IntegerField(_("Parameter End"))
    parameter_value = models.TextField(_("Parameter Value"))
    expression = models.ForeignKey(Expression, on_delete=models.CASCADE, related_name='parameters', verbose_name=_("Expression"))
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='parameters', verbose_name=_("Intent"))
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='parameters', null=True, blank=True, verbose_name=_("Entity"))

    class Meta:
        verbose_name = _("Expression Parameter")
        verbose_name_plural = _("Expression Parameters")

class Regex(models.Model):
    regex_name = models.TextField(_("Regex Name"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='regexes', verbose_name=_("Bot"))

    def __str__(self):
        return self.regex_name

    class Meta:
        verbose_name = _("Regex")
        verbose_name_plural = _("Regexes")

class RegexVariant(models.Model):
    regex = models.ForeignKey(Regex, on_delete=models.CASCADE, related_name='variants', verbose_name=_("Regex"))
    pattern = models.TextField(_("Pattern"))

    def __str__(self):
        return f"{self.regex.regex_name}: {self.pattern}"

    class Meta:
        verbose_name = _("Regex Variant")
        verbose_name_plural = _("Regex Variants")

class Response(models.Model):
    response_text = models.TextField(_("Response Text"))
    response_type = models.TextField(_("Response Type"))
    action = models.ForeignKey('Action', on_delete=models.CASCADE, verbose_name=_("Action"))

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

class SynonymVariant(models.Model):
    synonym_value = models.TextField(_("Synonym Value"))
    synonym = models.ForeignKey(Synonym, on_delete=models.CASCADE, verbose_name=_("Synonym"))

    class Meta:
        verbose_name = _("Synonym Variant")
        verbose_name_plural = _("Synonym Variants")

class NluLog(models.Model):
    ip_address = models.TextField(_("IP Address"))
    query = models.TextField(_("Query"))
    event_type = models.TextField(_("Event Type"))
    event_data = models.TextField(_("Event Data"))
    timestamp = models.DateTimeField(_("Timestamp"))

    class Meta:
        verbose_name = _("NLU Log")
        verbose_name_plural = _("NLU Logs")

class ModelModel(models.Model):
    model_name = models.TextField(_("Model Name"))
    timestamp = models.DateTimeField(_("Timestamp"))
    comment = models.TextField(_("Comment"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name=_("Bot"))
    local_path = models.TextField(_("Local Path"))
    server_path = models.TextField(_("Server Path"))
    server_response = models.TextField(_("Server Response"))

    class Meta:
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

class ActionType(Enum):
    UTTER = "utter"
    ACTION = "action"
    FORM = "form"
    SLOT_SET = "slot_set"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Action(models.Model):
    action_name = models.TextField(_("Action Name"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name=_("Bot"))
    action_type = models.CharField(max_length=10, choices=ActionType.choices(), default=ActionType.UTTER.value, verbose_name=_("Action Type"))
    action_config = models.TextField(null=True, blank=True, verbose_name=_("Action Config"))

    def __str__(self):
        return self.action_name

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")

class Rule(models.Model):
    rule_name = models.TextField(_("Rule Name"))
    rule_steps = models.TextField(_("Rule Steps"))
    timestamp = models.DateTimeField(_("Timestamp"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='rules', verbose_name=_("Bot"))

    def __str__(self):
        return self.rule_name

    class Meta:
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")

class Lookup(models.Model):
    lookup_name = models.TextField(_("Lookup Name"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='lookups', verbose_name=_("Bot"))

    def __str__(self):
        return self.lookup_name

    class Meta:
        verbose_name = _("Lookup")
        verbose_name_plural = _("Lookups")

class LookupVariant(models.Model):
    lookup = models.ForeignKey(Lookup, on_delete=models.CASCADE, related_name='variants', verbose_name=_("Lookup"))
    value = models.TextField(_("Value"))

    def __str__(self):
        return f"{self.lookup.lookup_name}: {self.value}"

    class Meta:
        verbose_name = _("Lookup Variant")
        verbose_name_plural = _("Lookup Variants")

class Story(models.Model):
    story_name = models.TextField(_("Story Name"))
    story = models.TextField(_("Story"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name=_("Bot"))
    timestamp = models.DateTimeField(_("Timestamp"))

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")

class Conversation(models.Model):
    ip_address = models.TextField(blank=True, null=True, verbose_name=_("IP Address"))
    conversation = models.TextField(_("Conversation"))
    story = models.TextField(blank=True, null=True, verbose_name=_("Story"))
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name=_("Bot"))
    timestamp = models.DateTimeField(_("Timestamp"))

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

class Settings(models.Model):
    setting_name = models.TextField(unique=True, verbose_name=_("Setting Name"))
    setting_value = models.TextField(verbose_name=_("Setting Value"))

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

class History(models.Model):
    intent = models.CharField(max_length=255, default='', blank=True, verbose_name=_("Intent"))
    entities = models.TextField(default='[]', blank=True, verbose_name=_("Entities"))  # Assuming entities are stored as JSON strings
    user_say = models.TextField(default='', blank=True, verbose_name=_("User Say"))
    confidence = models.FloatField(default=0.0, blank=True, verbose_name=_("Confidence"))
    timestamp = models.DateTimeField(default=datetime.now, blank=True, verbose_name=_("Timestamp"))
    response = models.TextField(default='', blank=True, verbose_name=_("Response"))
    sender_id = models.CharField(max_length=255, default='', blank=True, verbose_name=_("Sender ID"))
    slot_values = models.TextField(default='{}', blank=True, verbose_name=_("Slot Values"))  # Assuming slot values are stored as JSON strings
    intent_ranking = models.TextField(default='[]', blank=True, verbose_name=_("Intent Ranking"))  # Assuming intent ranking is stored as JSON strings
    next_action = models.CharField(max_length=255, default='', blank=True, verbose_name=_("Next Action"))

    def __str__(self):
        return self.user_say

    class Meta:
        verbose_name = _("History")
        verbose_name_plural = _("Histories")

class ChatUser(models.Model):
    sender_id = models.TextField(_("Sender ID"))
    sender_name = models.TextField(_("Sender Name"))

    class Meta:
        verbose_name = _("Chat User")
        verbose_name_plural = _("Chat Users")

class Test(models.Model):
    TEST_TYPE_CHOICES = [
        ('intent', _("Intent Test")),
        ('story', _("Story Test")),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES, verbose_name=_("Test Type"))

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Test_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name=_("Test"))
    result = models.JSONField(_("Result"))
    chart1_path = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Chart 1 Path"))
    chart2_path = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Chart 2 Path"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"Result for {self.test.name}"

    class Meta:
        verbose_name = _("Test Result")
        verbose_name_plural = _("Test Results")
