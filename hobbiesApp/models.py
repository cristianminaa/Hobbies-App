from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class MyUser(AbstractUser):
    image = models.ImageField(
        null=True, blank=False, default='default.png')
    city = models.CharField(max_length=200, null=False, blank=True)
    dob = models.DateField(max_length=8, null=True)
    hobbies = models.ManyToManyField('Hobby', blank=True)
    friends = models.ManyToManyField("MyUser", blank=True)
    objects = UserManager()

    def to_dict(self):
        '''Returns the Doctor object in the form of a dictionary'''
        return {
            'username': self.username,
            'id': self.id,
            'image': str(self.image),
            'city': self.city,
            'dob': self.dob,
            'email': self.email,
            'age': (datetime.date.today().year - self.dob.year -
                    ((datetime.date.today().month, datetime.date.today().day)
                     < (self.dob.month, self.dob.day))),
            'hobbies': [hobby.name for hobby in self.hobbies.all()],
            'friends': [friend.username for friend in self.friends.all()],
            'url': reverse('profilePage', kwargs={'id': self.id}),
            'api': reverse('user api', kwargs={'id': self.id}),
            'editing': False,
        }


class Hobby(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def to_dict(self):
        return{
            'name': self.name,
            'id': self.id,
        }


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        MyUser, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        MyUser, related_name="to_user", on_delete=models.CASCADE
    )

    def to_dict(self):
        return {
            'from_user': (self.from_user).to_dict(),
            'to_user': (self.to_user).to_dict(),
        }


class PageView(models.Model):
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
