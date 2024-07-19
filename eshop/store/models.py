from django.db import models
from django.contrib.auth.models import User
import uuid, datetime
from django.db.models.signals import post_save
from django.db.models import Avg



class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

def generate_sku():
    return uuid.uuid4().hex[:6].upper()

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True, default=generate_sku)  # Use callable function
    units_in_stock = models.PositiveIntegerField(default=0)  # New field for stock quantity

    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        avg_rating = self.rating_set.aggregate(Avg('rating'))['rating__avg'] or 0
        return round(avg_rating, 1)

class UserProfile(models.Model):
    GENDER_CHOICES = [('', ''), ('M', 'Male'), ('F', 'Female'),('O', 'Other'),]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    cart = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    
# create a user profile by default whenever a user registers
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile(user=instance)
        userprofile.save() 
        
# Automate the profile
post_save.connect(create_userprofile, sender=User)

class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {self.rating}"
