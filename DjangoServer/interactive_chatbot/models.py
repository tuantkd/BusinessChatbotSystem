from django.db import models

class Bot(models.Model):
    bot_name = models.CharField(max_length=200)
    bot_config = models.TextField()
    output_folder = models.CharField(max_length=200)

    def __str__(self):
        return self.bot_name