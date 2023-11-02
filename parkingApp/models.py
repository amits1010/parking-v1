from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password


# Create your models here.
# class user(models.Model):
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)


    

    # def __str__(self) -> str:
    #     return self.first_name



class vehicies(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    license = models.CharField(max_length=50)
    vehicle_CHOICES =( 
    ("1", "Two wheeler"), 
    ("2", "Four Wheeler"), 
    
    ) 
    vehicle_type = models.CharField(max_length=30,choices=vehicle_CHOICES,default='1')
class rate(models.Model):
    wheeler = models.CharField(max_length=50)
    rate = models.IntegerField()
    def __str__(self) -> str:
        return str(self.rate)

class Garage(models.Model):
    zipcode = models.CharField(max_length=100)
    rate_two_wheeler = models.ForeignKey(rate,on_delete=models.CASCADE,related_name='two_wheeler')
    rate_four_wheeler = models.ForeignKey(rate,on_delete=models.CASCADE,related_name='four_wheeler')

    def __str__(self) -> str:
        return self.zipcode


class spots(models.Model):
    garage_id = models.ForeignKey(Garage,on_delete=models.CASCADE)
    vehicle_CHOICES =( 
    ("1", "Two wheeler"), 
    ("2", "Four Wheeler"), 
    
    ) 
    vehicle_type = models.CharField(max_length=30,choices=vehicle_CHOICES,default='1')
    
    # STATUS_CHOICES = (
    #     ('1', 'Available'),
    #     ('2', 'Booked'),
    # )
    # status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='1')
    
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)




class Reservations(models.Model):
    garage_id = models.ForeignKey(Garage,on_delete=models.CASCADE)
    spot_id = models.ForeignKey(spots,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now)
    STATUS_CHOICES = (
        ('1', 'pending'),
        ('2', 'paid'),
    )
    payment = models.CharField(max_length=10,choices=STATUS_CHOICES,default='1')

    def __str__(self) -> str:
        return str(self.id) 
class transactions(models.Model):
    reservation_id = models.ForeignKey(Reservations,on_delete=models.CASCADE)
    total_time = models.CharField(max_length=200)
    payment_amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self) -> str:
        return str(self.id)