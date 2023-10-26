from django.db import models

class UserInput(models.Model):
    topic = models.CharField(max_length=100)