""" App Models are listed here """
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Pet(models.Model):
    """ Pet Model for adding New Pet """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(help_text="Age of pet in years.")
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

# HealthLog model
class HealthLog(models.Model):
    """ HealthLog Model for adding health records """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    record_date = models.DateField()
    weight = models.FloatField()
    rabies = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    deworming = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no','No')], default='no')

    def __str__(self):
        return f"Health Log for {self.pet.name} on {self.record_date}"

# ActivityLog model
ACTIVITY_CHOICES = [
    ('walk', 'Walk'),
    ('play', 'Play'),
    ('groom', 'Grooming'),
]

class ActivityLog(models.Model):
    """ ActivityLog Model for adding activity records """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes.")

    def __str__(self):
        return f"{self.pet.name} - {self.activity_type}"

class Product(models.Model):
    """ Product model for storing accessories of pets """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpeg')

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    """ Contact Model for storing mails """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(validators=[MaxLengthValidator(1000)])
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
