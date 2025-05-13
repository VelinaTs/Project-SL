from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
    
class User(AbstractUser):
    ROLE_CHOISE = (
        ('admin', 'Admin'),
        ('barber', 'Barber'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOISE, default='user')
    
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    saved = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username
    
class SaveChas(models.Model):
    phone = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    barber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='barber')
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.date} {self.time} with {self.barber.firstname} {self.barber.lastname}, phone: {self.phone}"
