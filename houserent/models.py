from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FlatsAvailable(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200,)
    bedroom = models.PositiveIntegerField()
    livingroom = models.PositiveIntegerField()
    bathroom = models.PositiveIntegerField()
    kitchen = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    date_and_time=models.DateTimeField(default=timezone.now)
    # For multiple images, we can use Django's FileField with the 'upload_to' parameter to specify the upload directory.
    images = models.ImageField(upload_to='',null=True)
    slugs=models.SlugField(unique=True,null=True)

    def __str__(self):
        return self.title

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey('FlatsAvailable', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    persons = models.PositiveIntegerField()
    profession = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    date_and_time=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking for {self.user.username} - {self.flat.title}"
    

class Booked(models.Model):
    flat_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking {self.id} "