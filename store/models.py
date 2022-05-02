from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Bihar', 'Bihar'),
    ('Assam', 'Assam'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=40)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name