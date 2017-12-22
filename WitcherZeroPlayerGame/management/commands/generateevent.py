from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from WitcherZeroPlayerGame import models
from django.db.models.aggregates import Count
from random import randint


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(
                profile__last_seen__gte=datetime.now() - timedelta(minutes=10),
                profile__witcher__age__isnull=False
        ):
            count = models.Event.objects.aggregate(count=Count('id'))['count']
            random_index = randint(0, count - 1)
            event = models.Event.objects.all()[random_index]
            witcher_event = models.WitcherEvent(witcher=user.profile.witcher, witcher_event=event, date=datetime.now())
            witcher_event.save()
        self.stdout.write('Finished')