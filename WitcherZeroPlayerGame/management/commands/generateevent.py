from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from WitcherZeroPlayerGame import models
from django.db.models.aggregates import Count
from random import randint


class Command(BaseCommand):
    @staticmethod
    def generate_neutral_event(user):
        count = models.Event.objects.count()
        random_index = randint(0, count - 1)
        event = models.Event.objects.all()[random_index]
        witcher_event = models.WitcherEvent(witcher=user.profile.witcher, event=event.event, date=datetime.now())
        witcher_event.save()

    @staticmethod
    def get_random_weapon(witcher):
        possible_weapon = models.Weapon.objects.filter(owned_by_school=False).union(
            models.Weapon.objects.filter(owned_by_school=True, school=witcher.school))
        count = possible_weapon.count()
        random_index = randint(0, count - 1)
        return possible_weapon[random_index]

    @staticmethod
    def generate_positive_event(user):
        positive_event_type = randint(0, 1)
        message = ""
        if positive_event_type == 0:
            weapon = Command.get_random_weapon(user.profile.witcher)
            having_weapon = models.HavingWeapon.objects.filter(witcher=user.profile.witcher, weapon=weapon)
            if having_weapon.count() != 0:
                having_weapon.first().count += 1
                having_weapon.first().save()
            else:
                having_weapon = models.HavingWeapon.objects.create(witcher=user.profile.witcher, weapon=weapon, count=1)
                having_weapon.save()
            message = "Нашел " + weapon.name + " в кустах... Может, все же есть бог на свете?"
        else:
            message = "Какое-то хорошее событие!"
        witcher_event = models.WitcherEvent(witcher=user.profile.witcher, event=message, date=datetime.now())
        witcher_event.save()

    @staticmethod
    def generate_negative_event(user):
        message = 'Какое-то плохое событие!'
        witcher_event = models.WitcherEvent(witcher=user.profile.witcher, event=message, date=datetime.now())
        witcher_event.save()

    def handle(self, *args, **options):
        for user in User.objects.filter(
                profile__last_seen__gte=datetime.now() - timedelta(minutes=10),
                profile__witcher__age__isnull=False
        ):
            event_type = randint(0, 2)
            if event_type == 0:
                self.generate_neutral_event(user)
            elif event_type == 1:
                self.generate_positive_event(user)
            else:
                self.generate_negative_event(user)
        self.stdout.write('Finished')
