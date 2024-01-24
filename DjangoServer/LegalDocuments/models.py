from django.db import models

class Laws(models.Model):
    LawId = models.IntegerField(primary_key=True)
    LawNumber = models.CharField(max_length=255)
    IssuedDate = models.DateField()
    LawName = models.TextField()
    LawLink = models.CharField(max_length=255)

class Decrees(models.Model):
    DecreeId = models.IntegerField(primary_key=True)
    DecreeNumber = models.CharField(max_length=255)
    IssuedDate = models.DateField()
    DecreeName = models.TextField()
    DecreeLink = models.CharField(max_length=255)

class Circulars(models.Model):
    CircularId = models.IntegerField(primary_key=True)
    CircularNumber = models.CharField(max_length=255)
    IssuedDate = models.DateField()
    CircularName = models.TextField()
    CircularLink = models.CharField(max_length=255)

class Decisions(models.Model):
    DecisionId = models.IntegerField(primary_key=True)
    DecisionNumber = models.CharField(max_length=255)
    IssuedDate = models.DateField()
    DecisionName = models.TextField()
    DecisionLink = models.CharField(max_length=255)
