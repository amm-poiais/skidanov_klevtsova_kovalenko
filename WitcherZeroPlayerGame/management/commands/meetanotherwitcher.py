from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from WitcherZeroPlayerGame import models
from random import randint


class MeetAnotherWitcher(BaseCommand):
    @staticmethod
    def get_random_stranger(witcher):
        strangers = models.Witcher.objects.all().difference(models.Witcher.objects.filter(pk=witcher.pk))
        count = strangers.count()
        random_index = randint(0, count - 1)
        return strangers[random_index]

    @staticmethod
    def generate_meeting_event(user):
        witcher = user.profile.witcher
        stranger = MeetAnotherWitcher.get_random_stranger(witcher)
        rel_count = models.Relation.objects.all().count()
        if (models.WitchersRelationship.objects.filter(first_witcher=witcher, second_witcher=stranger).count() == 0 &
                models.WitchersRelationship.objects.filter(first_witcher=stranger, second_witcher=witcher).count() == 0):
            rel_idx = randint(0, rel_count)
            rel = models.Relation.objects.all()[rel_idx]
            rel1 = models.WitchersRelationship.objects.create(first_witcher=witcher, second_witcher=stranger, relationship=rel)
            rel2 = models.WitchersRelationship.objects.create(first_witcher=stranger, second_witcher=witcher, relationship=rel)
            rel1.save()
            rel2.save()
            message1 = 'В пути мне встретился ' + stranger.name + '. Теперь у нас с ним взаимная ' + rel.name + '.'
            message2 = 'В пути мне встретился ' + witcher.name + '. Теперь у нас с ним взаимная ' + rel.name + '.'
            witcher_event_1 = models.WitcherEvent(witcher=witcher, event=message1, date=datetime.now())
            witcher_event_2 = models.WitcherEvent(witcher=stranger, event=message2, date=datetime.now())
            witcher_event_1.save()
            witcher_event_2.save()

    def handle(self, *args, **options):
        for user in User.objects.filter(
                profile__last_seen__gte=datetime.now() - timedelta(minutes=30),
                profile__witcher__isnull=False,
                profile__witcher__status="Жив"
        ):
            self.generate_meeting_event(user)
        self.stdout.write('Finished')