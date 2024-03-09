from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # DELIVERY_METHOD_CHOICES = [
    #     ("email", 'Email'),
    #     ("push", 'Push Notification'),
    # ]
    # delivery_method = models.CharField(choices=DELIVERY_METHOD_CHOICES, max_length=20, default=DELIVERY_METHOD_CHOICES[0][0])
    tasks = models.ForeignKey(PeriodicTask, blank=True,on_delete=models.CASCADE)
