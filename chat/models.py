from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Message(models.Model):
    text = models.CharField(max_length=500)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
