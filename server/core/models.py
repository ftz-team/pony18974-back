from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.fields import NullBooleanField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import tree
from random import randint
from .managers import UserManager
from .bot import send_message


@receiver(post_save, sender='core.Reservation')
def update_dataset_metadata(sender, instance=None, created=False, **kwargs):
    if created:
        instance.code = randint(1000, 9999)
        instance.save()
        user = instance.user
        user.current_reservation = instance
        user.save()

        #bot
        send_message(instance)

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=1000, default='', blank=True, null=True, unique=True)
    name = models.CharField(max_length=1000, default='', blank=True, null=True)
    city = models.CharField(max_length=1000, default='', blank=True, null=True)
    current_reservation = models.ForeignKey('core.Reservation', on_delete=models.CASCADE, related_name='user_current_reservation', blank=True, null=True)
    favourites = models.ManyToManyField('core.Wash', related_name='user_favourites', blank=True)

    # system
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.pk)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser


class Slot(models.Model):
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)

    @property
    def time_range(self):
        return str(self.time_start)[:-3] + ' - ' + str(self.time_end)[:-3]

class ServiceType(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True, null=True, unique=True)


class Service(models.Model):
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)

    @property
    def type_name(self):
        return self.type.name


class Wash(models.Model):
    name = models.CharField(max_length=1000, default='', blank=True, null=True, unique=True)
    address = models.CharField(max_length=1000, default='', blank=True, null=True, unique=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service, related_name='wash_services', blank=True)
    rating = models.FloatField(blank=True, null=True)
    price_level = models.PositiveIntegerField(blank=True, null=True)
    

    @property
    def reservations(self):
        return Reservation.objects.filter(wash=self)

    @property
    def available_slots(self):
        busy_slots = []
        for res in self.reservations:
            busy_slots.append(res.slot.pk)
        return Slot.objects.exclude(pk__in=busy_slots)

    @property
    def pk_available_slots(self):
        res = []
        for s in self.available_slots:
            res.append(s.pk)
        return res


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    wash = models.ForeignKey(Wash, on_delete=models.CASCADE, blank=True, null=True)
    code = models.PositiveIntegerField(blank=True, null=True)
    qr_image = models.ImageField(upload_to='media/', default='qr.png', blank=True, null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    wash = models.ForeignKey(Wash, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
