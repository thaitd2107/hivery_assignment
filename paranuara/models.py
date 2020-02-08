from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.

class Company(models.Model):
    index = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False,
                                        verbose_name=_("Company Index"))
    company = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Company Name"))


class People(models.Model):
    _id = models.CharField(max_length=128, unique=True, blank=False, verbose_name=_("People ID"))
    index = models.IntegerField(primary_key=True, unique=True, blank=False, null=False, verbose_name=_("People Index"))
    guid = models.CharField(max_length=128, unique=True, blank=False, verbose_name=_("GUID"))
    has_died = models.BooleanField(default=False, verbose_name="Died")
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=32, verbose_name=_("Balance"))
    picture = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Picture"))
    age = models.IntegerField(default=0, blank=True, null=True, verbose_name=_("Age"))
    eye_color = models.CharField(max_length=32, blank=True, null=True, verbose_name=_("Eye Color"))
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Name"))
    gender = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("Gender"))
    company = models.ForeignKey('Company', related_name="employees", blank=True, null=True,
                                verbose_name=_("Company ID"), on_delete=models.CASCADE)
    email = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Phone"))
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Address"))
    about = models.TextField(blank=True, null=True, verbose_name=_("About"))
    registered = models.DateTimeField(blank=True, null=True, verbose_name=_('Registered'))
    tags = models.TextField(blank=True, null=True, verbose_name=_("Tags"))
    favourite_food = models.TextField(blank=True, null=True, verbose_name=_("Favourite Food"))
    fruits = models.TextField(blank=True, null=True, verbose_name=_("Favourite Fruit"))
    vegetables = models.TextField(blank=True, null=True, verbose_name=_("Favourite Vegetable"))
    greeting = models.TextField(blank=True, null=True, verbose_name=_("Greeting"))

    # add a list of new tags to people
    def add_tags(self, new_tags=None):
        if new_tags:
            self.tags = ','.join(new_tags)
            self.save()

    # return a list of tags
    def get_tags(self):
        if self.tags:
            return self.tags.split(',')
        else:
            return []

    # add a list of new favourite food to people
    def add_favourite_food(self, favourite_foods=None):
        if favourite_foods:
            self.favourite_food = ','.join(favourite_foods)
            self.save()

    # return a list of favourite_food
    def get_favourite_food(self):
        if self.favourite_food:
            return self.favourite_food.split(',')
        else:
            return []

    # return a list of favourite fruits
    def get_fruits(self):
        if self.fruits:
            return self.fruits.split(',')
        else:
            return []

    # return a list of favourite vegetables
    def get_vegetables(self):
        if self.vegetables:
            return self.vegetables.split(',')
        else:
            return []

    # add a friend
    def add_friend(self, other_people_index):
        new_friend = Friend()
        new_friend.people_index = self
        new_friend.friend_index = other_people_index
        new_friend.save()

    # add a list of friends
    def add_friends(self, friend_list):
        if friend_list:
            for friend in friend_list:
                self.add_friend(People.objects.filter(index=friend['index']).first())

    # return a friend list
    def get_all_friends(self):
        return self.friends.all()


class Friend(models.Model):
    people_index = models.ForeignKey('People', related_name='friends', verbose_name=_('People'),
                                     on_delete=models.CASCADE)
    friend_index = models.ForeignKey('People', verbose_name=_('Friend'), on_delete=models.CASCADE)
