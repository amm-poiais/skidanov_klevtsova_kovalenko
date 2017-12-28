from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.


class MonsterType(models.Model):
    name = models.CharField(max_length=20)


class MonsterClass(models.Model):
    name = models.CharField(max_length=20)


class Monster(models.Model):
    name = models.CharField(max_length=40)
    monster_type = models.ForeignKey(MonsterType, models.PROTECT)
    monster_class = models.ForeignKey(MonsterClass, models.PROTECT)
    strength = models.IntegerField()



class DamagePerc(models.Model):
    name = models.CharField(max_length=50)


class WeaponType(models.Model):
    name = models.CharField(max_length=30)


class MonsterWeaponTypeRelation(models.Model):
    monster = models.ForeignKey(Monster, models.PROTECT)
    weapon_type = models.ForeignKey(WeaponType, models.PROTECT)
    damage_perc = models.ForeignKey(DamagePerc, models.PROTECT)

    class Meta:
        unique_together = (("monster", "weapon_type"),)


class WitcherSchool(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Weapon(models.Model):
    name = models.CharField(max_length=40)
    owned_by_school = models.BooleanField()
    school = models.ForeignKey(WitcherSchool, models.PROTECT, null=True)
    weapon_type = models.ForeignKey(WeaponType, models.PROTECT)
    price = models.IntegerField()
    damage = models.IntegerField()


class Armor(models.Model):
    name = models.CharField(max_length=40)
    owned_by_school = models.BooleanField()
    school = models.ForeignKey(WitcherSchool, models.PROTECT, null=True)
    price = models.IntegerField()
    protection = models.IntegerField()


class Witcher(models.Model):
    name = models.CharField(max_length=40, unique=True)
    age = models.IntegerField()
    school = models.ForeignKey(WitcherSchool, models.PROTECT, null=True)
    status = models.CharField(max_length=30)


class HavingArmor(models.Model):
    witcher = models.ForeignKey(Witcher, models.PROTECT)
    armor = models.ForeignKey(Armor, models.PROTECT)
    count = models.IntegerField()

    class Meta:
        unique_together = (("witcher", "armor"),)


class HavingWeapon(models.Model):
    witcher = models.ForeignKey(Witcher, models.PROTECT)
    weapon = models.ForeignKey(Weapon, models.PROTECT)
    count = models.IntegerField()

    class Meta:
        unique_together = (("witcher", "weapon"),)


class Relation(models.Model):
    name = models.CharField(max_length=40)


class WitchersRelationship(models.Model):
    first_witcher = models.ForeignKey(Witcher, models.PROTECT, related_name='first')
    second_witcher = models.ForeignKey(Witcher, models.PROTECT, related_name='second')
    relationship = models.ForeignKey(Relation, models.PROTECT)

    class Meta:
        unique_together = (("first_witcher", "second_witcher"),)


class Ingridient(models.Model):
    name = models.CharField(max_length=40)


class LootFromMonster(models.Model):
    monster = models.ForeignKey(Monster, models.PROTECT)
    ingridient = models.ForeignKey(Ingridient, models.PROTECT)
    probability = models.FloatField()

    class Meta:
        unique_together = (("monster", "ingridient"),)


class DamageType(models.Model):
    name = models.CharField(max_length=20)


class MonsterDamageTypePerc(models.Model):
    monster = models.ForeignKey(Monster, models.PROTECT)
    damage_type = models.ForeignKey(DamageType, models.PROTECT)
    damage_perc = models.ForeignKey(DamagePerc, models.PROTECT)

    class Meta:
        unique_together = (("monster", "damage_type"),)


class AlchemyType(models.Model):
    name = models.CharField(max_length=40)


class Alchemy(models.Model):
    name = models.CharField(max_length=40)
    action_time = models.IntegerField()
    alchemy_type = models.ForeignKey(AlchemyType, models.PROTECT)
    damage_type = models.ForeignKey(DamageType, models.PROTECT)
    toxicity = models.IntegerField()


class Formula(models.Model):
    ingridient = models.ForeignKey(Ingridient, models.PROTECT)
    alchemy = models.ForeignKey(Alchemy, models.PROTECT)
    count = models.IntegerField()

    class Meta:
        unique_together = (("ingridient", "alchemy"),)


class HavingAlchemy(models.Model):
    alchemy = models.ForeignKey(Alchemy, models.PROTECT)
    witcher = models.ForeignKey(Witcher, models.PROTECT)
    count = models.IntegerField()

    class Meta:
        unique_together = (("alchemy", "witcher"),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile", blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    witcher = models.OneToOneField(Witcher, on_delete=models.SET_NULL, null=True, blank=True)
    possible_positive_events = models.IntegerField(default=5)
    possible_negative_events = models.IntegerField(default=5)
    possible_neutral_events = models.IntegerField(default=10)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            profile.last_seen = datetime.today()
            sender.profile = profile

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Event(models.Model):
    event = models.CharField(max_length=200)


class WitcherEvent(models.Model):
    event = models.CharField(max_length=200)
    witcher = models.ForeignKey(Witcher, models.PROTECT, related_name='witcher')
    date = models.DateTimeField()
