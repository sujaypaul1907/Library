from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    fees = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name) + " ["+str(self.fees)+']'

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.phone)+']' 


def expiry():
    return datetime.today() + timedelta(days=14)
    
class IssuedBook(models.Model):
    member_id = models.CharField(max_length=100, blank=True) 
    fees = models.CharField(max_length=10)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
