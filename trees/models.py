from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Account(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    accounts = models.ManyToManyField(Account, related_name="users")

    def plant_tree(self, plant, latitude, longitude):
        return PlantedTree.objects.create(
            user=self, plant=plant, latitude=latitude, longitude=longitude
        )

    def plant_trees(self, tree_data):
        planted = []
        for plant, (latitude, longitude) in tree_data:
            tree = self.plant_tree(plant, latitude, longitude)
            planted.append(tree)
        return planted


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Plant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="planted_trees"
    )
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="instances")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    planted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plant.name} by {self.user.username}"
