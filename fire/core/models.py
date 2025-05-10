from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField()
    saved = models.DateTimeField()
    
    def __str__(self):
        return self.username
    
class Barber(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(unique=True)
    password = models.CharField()
    saved = models.DateTimeField()
    
    def __str__ (self):
        return self.email
    
class Admin(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(unique=True)
    password = models.CharField()
    saved = models.DateTimeField()
    
    def __str__(self):
        return self.email

