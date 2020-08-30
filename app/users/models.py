import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from PIL import Image
from virtual_tutoring.storage_backends import PublicMediaStorage


class Profile(models.Model):
    AS   = 'AS'
    AAP  = 'AAP'
    COE  = 'COE'
    ILR  = 'ILR'
    CALS = 'CALS'
    HUMEC = 'HUMEC'
    SCJCB = 'SCJCB'

    SCHOOL_CHOICES = [(CALS, 'Agriculture and Life Sciences'), (AAP, 'Architecture, Art, and Planning'), (AS, 'Arts and Sciences'), (
        COE, 'Engineering'), (HUMEC, 'Human Ecology'), (ILR, 'Industrial and Labor Relations'), (SCJCB, 'SC Johnson College of Business')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grad_year = models.IntegerField(default=2024, validators=[MaxValueValidator(
        datetime.datetime.now().year + 4), MinValueValidator(1990)])
    image = models.ImageField(default='default.jpg',
                              storage=PublicMediaStorage())
    college = models.CharField(max_length=5, choices=SCHOOL_CHOICES, default=AS)

    def __str__(self):
        return f'{self.user.username} Profile'
