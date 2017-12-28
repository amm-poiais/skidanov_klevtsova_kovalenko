from django.core.management.base import BaseCommand
from WitcherZeroPlayerGame.management.commands import generateevent
from WitcherZeroPlayerGame.models import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(profile__last_seen__gte=datetime.now() - timedelta(hours=1)):
            user.profile.possible_bad_events = 5
            user.profile.possible_good_events = 5
            user.profile.possible_neutral_events = 10
            user.save()
