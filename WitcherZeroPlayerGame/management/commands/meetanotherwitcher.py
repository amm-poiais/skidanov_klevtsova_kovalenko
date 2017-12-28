from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from WitcherZeroPlayerGame import models
from random import randint

def add_relation(witcher_to, witcher_with, relation):
    rel = models.WitchersRelationship.objects.create(first_witcher=witcher_to, second_witcher=witcher_with, relationship=relation)
    rel.save()
    message = 'В пути мне встретился ' + witcher_with.name + '. Теперь у нас с ним взаимная ' + rel.name + '.'
    witcher_event = models.WitcherEvent(witcher=witcher_to, event=message, date=datetime.now())
    witcher_event.save()



class Command(BaseCommand):
    @staticmethod
    def get_random_stranger(witcher):
        strangers = models.Witcher.objects.all().difference(models.Witcher.objects.filter(pk=witcher.pk))
        count = strangers.count()
        random_index = randint(0, count - 1)
        return strangers[random_index]

    @staticmethod
    def generate_meeting_event(user):
        witcher = user.profile.witcher
        stranger = Command.get_random_stranger(witcher)
        rel_count = models.Relation.objects.all().count()
        if (models.WitchersRelationship.objects.filter(first_witcher=witcher, second_witcher=stranger).count() == 0 &
                models.WitchersRelationship.objects.filter(first_witcher=stranger, second_witcher=witcher).count() == 0):
            rel_idx = randint(0, rel_count)
            rel = models.Relation.objects.all()[rel_idx]
            add_relation(witcher, stranger, rel)
            add_relation(stranger, witcher, rel)

    def handle(self, *args, **options):
        for user in User.objects.filter(
                profile__last_seen__gte=datetime.now() - timedelta(minutes=30),
                profile__witcher__isnull=False,
                profile__witcher__status="Жив"
        ):
            self.generate_meeting_event(user)
        self.stdout.write('Finished')
