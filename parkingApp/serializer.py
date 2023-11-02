from rest_framework import serializers

# from .models import user
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Garage,spots,Reservations,transactions

class userSerializers(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields=['username','email','first_name','last_name','password']
        #fields = '__all__'
       

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(userSerializers, self).create(validated_data)
    
class garageSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Garage
        fields = '__all__'

class spotsSerializers(serializers.ModelSerializer):
    garage_id = serializers.StringRelatedField()
    vehicle_type  = serializers.CharField(source ='get_vehicle_type_display')
    class Meta:
        model = spots
        # fields = '__all__'
        fields = ['id','garage_id','vehicle_type','status']

class revervationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'

# class updateRevervationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservations
#         fields = ['end_time','payment']

class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = '__all__'
# class updateTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = transactions
#         fields = ['total_time','payment_amount']