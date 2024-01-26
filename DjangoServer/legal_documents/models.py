from django.db import models

class Laws(models.Model):
    law_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    law_name = models.TextField()
    law_link = models.CharField(max_length=255)

class Decrees(models.Model):
    decree_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    decree_name = models.TextField()
    decree_link = models.CharField(max_length=255)

class Circulars(models.Model):
    circular_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    circular_name = models.TextField()
    circular_link = models.CharField(max_length=255)

class Decisions(models.Model):
    decision_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    decision_name = models.TextField()
    decision_link = models.CharField(max_length=255)
