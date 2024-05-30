from django.db import models
from accounts.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country_map = models.ImageField(upload_to='map_images', blank=True, null=True) 
    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='destination_images')
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activity_images', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title
    
class DayDescription(models.Model):
    day = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Day {self.day}"    
    
class Package(models.Model):
    name = models.CharField(max_length=100)
    activities = models.ForeignKey(Activity, on_delete=models.CASCADE)
    total_days = models.PositiveIntegerField(default=1) 
    difficulty_level = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    day_descriptions = models.ManyToManyField(DayDescription)  # New field for descriptions of each day
    requirements = models.TextField(default='')  # New field for requirements with default value ''
    services = models.TextField(default='')  # New field for services with default value ''
    total_participants = models.PositiveIntegerField(default=1) # New field for total participants
    booking_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='package_images', blank=True, null=True)
    map_image = models.ImageField(upload_to='map_images', blank=True, null=True)  # New field for map image
    best_season = models.CharField(max_length=50, default='Spring')
    safety_tips = models.TextField(default='')  # New field for safety tips with default value ''

    def __str__(self):
        return self.name



    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE) 
    date_booked = models.DateField(auto_now_add=True,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    participants = models.IntegerField(default=1, validators=[MinValueValidator(1)],null=True,blank=True)  # Field for the number of participants
    special_requirements = models.TextField(blank=True, null=True)  # Field for special requirements
    payment_gateway = models.BooleanField(default=False)  # Field to indicate if booking is through payment gateway
    pidx =models.CharField(max_length=50,null=True,blank=True)
    status=models.CharField(max_length=50,null=True,blank=True)
    transection_id=models.CharField(max_length=50,null=True,blank=True)
    fee=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    refunded=models.BooleanField(null=True,blank=True,default=False)
    price=models.IntegerField( null=True,blank=True)

    def __str__(self):
        return f"{self.activity.title} - {self.user.username}"
  