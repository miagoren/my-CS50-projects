from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import json

# Models for WebAid

class User(AbstractUser):

    skills = models.TextField()
    location = models.CharField(max_length=64)

    def get_latest_resolved(self):
        resolved = self.resolved.all().order_by('-id')[:5]
        return resolved

    def get_latest_created(self):
        opportunities = self.opportunities.all().filter(resolved=None).order_by('-id')

        for opportunity in opportunities:
            opportunity = opportunity.make_time_difference()
        return opportunities

class Opportunity(models.Model):
    """Opportunity"""

    title = models.CharField(max_length=64)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    location = models.CharField(max_length=64)
    categories = models.TextField() # Create categories
    creation_time = models.DateTimeField(auto_now_add=True)
    resolved = models.OneToOneField('Resolve', null=True, blank=True, on_delete=models.PROTECT, related_name='opportunity')

    def __str__(self):
        return f'Help {self.creator} ({self.title})'

    class Meta:
        verbose_name_plural = "Opportunities"

    def get_latest(num=None):
        if num:
            opportunities = Opportunity.objects.all().filter(resolved=None).order_by('-id')[: + num]
        else:
            opportunities = Opportunity.objects.all().filter(resolved=None).order_by('-id')

        for opportunity in opportunities:
            opportunity = opportunity.make_time_difference()
        return opportunities

    def make_time_difference(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        then = self.creation_time
        delta = now - then
        if delta < datetime.timedelta(minutes=1):
            # How many minutes ago
            self.creation_time = 'Posted just now'
        elif delta < datetime.timedelta(hours=1):
            # How many minutes ago
            minutes, rem = divmod(delta.seconds, 60)
            self.creation_time = f'{minutes} minutes ago'
        elif delta < datetime.timedelta(days=1):
            # How many hours ago
            hours, rem = divmod(delta.seconds, 3600)
            self.creation_time = f'{hours} hours ago'
        elif delta < datetime.timedelta(days=7):
            # How many days ago
            days = delta.days
            self.creation_time = f'{days} days ago'
        elif delta < datetime.timedelta(days=21):
            # How many weeks ago
            weeks, rem = divmod(delta.days, 7)
            self.creation_time = f'{weeks} weeks ago'
        else:
            self.creation_time = then.date
        return self

class Conversation(models.Model):
    """Conversation"""

    subject = models.CharField(max_length=64)
    users = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f'Conversation about {self.subject}'

class Message(models.Model):
    """Message"""

    body = models.TextField(max_length=1000)
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} says {self.body}'

class Resolve(models.Model):
    """Resolve"""

    resolvers = models.ManyToManyField(User, related_name='resolved')
    summary = models.TextField(max_length=1000)
