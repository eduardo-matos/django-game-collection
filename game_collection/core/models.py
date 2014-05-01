from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    title = models.CharField('title', max_length=100)
    publisher = models.CharField('publisher', max_length=100)
    completed = models.BooleanField('completed', default=False)
    created_at = models.DateField('created_at', auto_now_add=True)
    updated_at = models.DateField('updated_at', auto_now=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.title
