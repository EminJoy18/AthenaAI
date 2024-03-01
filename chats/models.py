from django.db import models

# Create your models here.
class Chat(models.Model):
    user_prompt = models.CharField(max_length = 5000)
    bot_response = models.CharField(max_length = 5000)