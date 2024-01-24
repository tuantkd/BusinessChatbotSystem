import json
from django.db import models

class Intents(models.Model):
    Name = models.CharField(max_length=255)
    Examples = models.TextField()

class Entities(models.Model):
    Name = models.CharField(max_length=255)
    Value = models.CharField(max_length=255)

class Actions(models.Model):
    Name = models.CharField(max_length=255)

class Stories(models.Model):
    Name = models.CharField(max_length=255)
    Steps = models.TextField()

class Rules(models.Model):
    Conditions = models.TextField()
    ActionId = models.ForeignKey(Actions, on_delete=models.CASCADE)

class Responses(models.Model):
    Name = models.CharField(max_length=200)
    Texts = models.TextField()

    def set_texts(self, texts_list):
        self.Texts = json.dumps(texts_list)

    def get_texts(self):
        return json.loads(self.Texts)

class History(models.Model):
    UserId = models.CharField(max_length=50, null=False)
    SessionId = models.CharField(max_length=50, null=False)
    Intent = models.CharField(max_length=50, null=False)
    Text = models.CharField(max_length=500, null=False)
    Entities = models.JSONField(null=True)
    Confidence = models.FloatField(null=True)
