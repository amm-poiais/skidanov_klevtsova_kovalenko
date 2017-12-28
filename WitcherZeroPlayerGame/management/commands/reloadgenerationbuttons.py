from django.core.management.base import BaseCommand
from WitcherZeroPlayerGame.management.commands import generateevent
from WitcherZeroPlayerGame.models import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


def reload(user):
    user.profile.possible_negative_events = 5
    user.profile.possible_positive_events = 5
    user.profile.possible_neutral_events = 10
    user.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(profile__last_seen__gte=datetime.now() - timedelta(hours=1)):
            reload(user)
