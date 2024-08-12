from django.db import models
from django.contrib import admin
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    profile_img = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email

class package(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    days = models.IntegerField()
    image = models.ImageField(upload_to='static/images/packages/')
    available = models.BooleanField()
    description = models.TextField()
    rating = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
class contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.subject} from {self.email}"
    
class signup(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    OTP = models.CharField(max_length=6)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

class otp(models.Model):
    email = models.CharField(max_length=255)
    OTP = models.CharField(max_length=6)

class booking(models.Model):
    package = models.BigIntegerField()
    user = models.BigIntegerField()
    arrival = models.DateField()
    members = models.IntegerField()
    payment = models.ImageField()
    verify = models.BooleanField()
    # recipt = 

    def __str__(self) -> str:
        Package = package.objects.get(id=self.package)
        return f"Package: {Package.name} | Verify: {self.verify} | Status: {self.status}"
    
    @property
    def end_date(self):
        Package = package.objects.filter(id=self.package).first()
        return self.arrival + timedelta(days=Package.days)
    
    @property
    def reviewed(self) -> bool:
        Review = review.objects.filter(booking=self.id)
        return Review.exists()
    
    @property
    def status(self) -> str:
        date = timezone.now().date()
        if date < self.arrival and self.payment == "/static/images/receipts/no_receipt.html" and not self.verify:
            return "Un-Paid"
        elif date < self.arrival and self.payment != "/static/images/receipts/no_receipt.html" and not self.verify:
            return "Un-Verified"
        elif date < self.arrival and self.verify:
            return "Coming Soon"
        elif date >= self.arrival and date <= self.end_date and self.verify:
            return "Active"
        elif date > self.end_date and not self.reviewed:
            return "Un-Reviewed"
        else:
            return "Expire"

class review(models.Model):
    rating = models.IntegerField()
    booking = models.BigIntegerField()
    comment = models.TextField(max_length=500)

    def __str__(self) -> str:
        booked = booking.objects.get(id=self.booking)
        Package = package.objects.get(id=booked.package)
        User = user.objects.get(id=booked.user)
        return f"User:{User.name} | package: {Package.name}"
    
    @property
    def booked(self):
        book = booking.objects.get(id=self.booking)
        return book

    @property
    def Package(self) -> package:
        booked = self.booked
        Package = package.objects.get(id=booked.package)
        return Package
    
    @property
    def User(self) -> user:
        booked = self.booked
        result = user.objects.get(id=booked.user)
        return result

admin.site.register(user)
admin.site.register(package)
admin.site.register(contact)
admin.site.register(booking)
admin.site.register(review)