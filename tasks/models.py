from django.db import models
from django.contrib.auth.models import User

class Task(models.Model): 
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    completed_at = models.DateTimeField(null = True)
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self): 
        return f'{self.title} - {self.user.username}'