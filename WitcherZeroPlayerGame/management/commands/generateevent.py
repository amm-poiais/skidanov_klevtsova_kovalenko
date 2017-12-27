from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from WitcherZeroPlayerGame import models
from django.db.models.aggregates import Count
from random import randint
from django.db.models import Max


class Command(BaseCommand):
    @staticmethod
    def generate_neutral_event(user):
        events = models.Event.objects.all()
        count = events.count()        random_index = randint(0, count - 1)
        event = events[random_index]
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
    def get_random_armor(witcher):
        possible_armor = models.Armor.objects.filter(owned_by_school=False).union(
            models.Armor.objects.filter(owned_by_school=True, school=witcher.school))
        count = possible_armor.count()
        random_index = randint(0, count - 1)
        return possible_armor[random_index]

    @staticmethod
    def get_random_alchemy():
        possible_alchemy = models.Alchemy.objects.all()
        count = possible_alchemy.count()
        random_index = randint(0, count - 1)
        return possible_alchemy[random_index]

    @staticmethod
    def get_random_monster():
        possible_monster = models.Monster.objects.all()
        count = possible_monster.count()
        random_index = randint(0, count - 1)
        return possible_monster[random_index]

    @staticmethod
    def get_random_stranger(witcher):
        strangers = models.Witcher.objects.all().difference(models.Witcher.objects.filter(pk=witcher.pk))
        count = strangers.count()
        random_index = randint(0, count - 1)
        return strangers[random_index]

    @staticmethod
    def generate_positive_event(user):
        # TODO: изменить диапазон типов после добавления в базу брони и предметов
        positive_event_type = randint(0, 0)
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
        elif positive_event_type == 1:
            armor = Command.get_random_armor(user.profile.witcher)
            having_armor = models.HavingArmor.objects.filter(witcher=user.profile.witcher, armor=armor)
            if having_armor.count() != 0:
                having_armor.first().count += 1
                having_armor.first().save()
            else:
                having_armor = models.HavingArmor.objects.create(witcher=user.profile.witcher, armor=armor, count=1)
                having_armor.save()
            message = "Нашел труп, а на нем - " + armor.name + ". Пахнет не очень, но зато бесплатно!"
        elif positive_event_type == 2:
            alchemy = Command.get_random_alchemy()
            having_alchemy = models.HavingAlchemy.objects.filter(witcher=user.profile.witcher, alchemy=alchemy)
            if having_alchemy.count() != 0:
                having_alchemy.first().count += 1
                having_alchemy.first().save()
            else:
                having_alchemy = models.HavingAlchemy.objects.create(witcher=user.profile.witcher, alchemy=alchemy, count=1)
                having_alchemy.save()
            message = "Что-то больно ударило по голове. Оказалось - " + alchemy.name \
                      + ". Пожалуй, оставлю себе, пригодится."
        else:
            message = "Какое-то хорошее событие!"
        witcher_event = models.WitcherEvent(witcher=user.profile.witcher, event=message, date=datetime.now())
        witcher_event.save()

    @staticmethod
    def generate_negative_event(user):
        wither = user.profile.witcher
        monster = Command.get_random_monster()
        monster_chance = monster.strength
        max_dam_per = models.DamagePerc.objects.order_by('-value').first()
        monster_weap_rel = models.MonsterWeaponTypeRelation.objects.filter(monster=monster, damage_perc=max_dam_per)
        monster_dam_rel = models.MonsterDamageTypePerc.objects \
            .filter(monster=monster, damage_perc=max_dam_per)
        witcher_chance = 100
        possible_armor = models.HavingArmor.objects.filter(witcher=wither).select_related('armor')
        if possible_armor.count() != 0:
            witcher_chance += possible_armor.aggregate(Max('protection'))
        possible_weapon = models.HavingWeapon.objects.filter(witcher=wither).select_related('weapon')
        if possible_weapon.count() != 0 & monster_weap_rel.count() != 0:
            possible_weapon = possible_weapon.filter(weapon__weapon_type_in=monster_weap_rel.all().weapon_type)
            if possible_weapon.count() != 0:
                witcher_chance += possible_weapon.aggregate(Max('damage'))
        possible_alchemy = models.HavingAlchemy.objects.filter(witcher=wither).select_related('alchemy')
        if possible_alchemy.count() != 0 & monster_dam_rel.count() != 0:
            possible_alchemy = possible_alchemy.filter(alchemy__damage_type_in=monster_dam_rel.all().damage_type)
        for al in possible_alchemy:
            witcher_chance += 5
        if monster_chance/witcher_chance >= 1:
            message = monster.name + ' напал со спины и откусил ползадницы. Отполз в кусты зализывать раны.'
        else:
            random = randint(0, 100)
            if random/100 < monster_chance/witcher_chance:
                message = monster.name + ' победил меня, хоть и в не очень честном бою. В следующий раз я ему задам!'
            else:
                message = monster.name + ' напал и думал, что будет легко. Но я показал ему, где утопцы зимуют!'
        #message = 'Случилось что-то плохое. Очень плохое.'
        witcher_event = models.WitcherEvent(witcher=user.profile.witcher, event=message, date=datetime.now())
        witcher_event.save()

    @staticmethod
    def generate_meeting_event(user):
        witcher = user.profile.witcher
        stranger = Command.get_random_stranger(witcher)
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
                profile__last_seen__gte=datetime.now() - timedelta(minutes=10),
                profile__witcher__isnull=False,
                profile__witcher__status="Жив"
        ):
            event_type = randint(0, 2)
            if event_type == 0:
                self.generate_neutral_event(user)
            elif event_type == 1:
                self.generate_positive_event(user)
            else:
                self.generate_negative_event(user)
        self.stdout.write('Finished')
