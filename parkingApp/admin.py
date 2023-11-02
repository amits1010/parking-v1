from django.contrib import admin
from .models import Garage,spots,rate,Reservations,transactions

# from django.contrib.auth.models import User

# from django.contrib.auth.models import User
# Register your models here.
# class useradmin(admin.ModelAdmin):
#     model=User
#     fields = ['email','first_name','last_name','password']
# admin.site.register(User,useradmin)

class garagedmin(admin.ModelAdmin):
    model = Garage
    list_display = ['id','zipcode','rate_two_wheeler','rate_four_wheeler']

admin.site.register(Garage,garagedmin)

class spotAdmin(admin.ModelAdmin):
    model = spots
    list_display = ['id','garage_id','vehicle_type','status']
admin.site.register(spots,spotAdmin)

class rateAdmin(admin.ModelAdmin):
    model = rate
    list_display = ['id','wheeler','rate']
admin.site.register(rate,rateAdmin)


class reservationAdmin(admin.ModelAdmin):
    model = Reservations
    list_display = ['id','garage_id','spot_id','start_time','end_time','payment']
admin.site.register(Reservations,reservationAdmin)


class transactionAdmin(admin.ModelAdmin):
    model = transactions
    list_display = ['id','reservation_id','total_time','payment_amount']
admin.site.register(transactions,transactionAdmin)