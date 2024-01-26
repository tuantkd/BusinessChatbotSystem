import json
from django.db import models
from django.core.validators import RegexValidator

class Menu(models.Model):
    index = models.CharField(max_length=255,validators=[
        RegexValidator(
            regex=r'^(\d+\.)*\d+$',
            message='Index must be a number or a series of numbers separated by dots',
            code='invalid_index'
        )
    ])
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    
class NLU(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    content = models.TextField()

# FILEPATH: /D:/Projects/EnterpriseRegistrationSystem/DjangoServer/chatbot_data/models.py
class Rule(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    content = models.TextField()

# FILEPATH: /D:/Projects/EnterpriseRegistrationSystem/DjangoServer/chatbot_data/models.py
class Stories(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    content = models.TextField()

# FILEPATH: /D:/Projects/EnterpriseRegistrationSystem/DjangoServer/chatbot_data/models.py
class Domain(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    content = models.TextField()

class History(models.Model):
    user_id = models.CharField(max_length=50, null=False)
    session_id = models.CharField(max_length=50, null=False)
    intent = models.CharField(max_length=50, null=False)
    text = models.CharField(max_length=500, null=False)
    entities = models.JSONField(null=True)
    confidence = models.FloatField(null=True)
