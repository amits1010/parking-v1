from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate

from django.db import transaction


# from .models import user
from django.contrib.auth.models import User
from .serializer import userSerializers,garageSerializers,spotsSerializers,revervationSerializer,transactionSerializer#,updateRevervationSerializer,updateTransactionSerializer

from .models import Garage,spots,Reservations,transactions

from django.utils.timezone import now


# Create your views here.
# @APIView('GET','POST')
# class user_CRUD(ListCreateAPIView):
#     queryset = user.objects.all()
#     serializer_class = userSerializers



class user_CRUD(APIView):
    def get(self,request):
        qs = User.objects.all()
        serializer_obj = userSerializers(qs,many=True)
        return Response(serializer_obj.data)
    def post(self,request):
        password = request.data.get('password')
        serializer = userSerializers(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            # user_data = user.objects.get(user_obj.id)
            # user_data.set_password(password=password)
            refresh = RefreshToken.for_user(user_obj)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token_data,status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class userLoginApi(APIView):
    def post(self,request):
        user_email = request.data.get('email')
        password = request.data.get('password')
      
        #==============================================================================
        # try:
        #     user_auth =authenticate(username=user_email,password=password)
        # except User.DoesNotExist:
        #     return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # if user_auth:
        #     refresh = RefreshToken.for_user(user_auth)
        #     token_data = {
        #         'refresh': str(refresh),
        #         'access': str(refresh.access_token),
        #     }
        #     return Response(token_data, status=status.HTTP_200_OK)
        #===================================================================
        try:
            user_auth = User.objects.get(email=user_email)#authenticate(username=username,password=password)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password,user_auth.password):
            refresh = RefreshToken.for_user(user_auth)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token_data, status=status.HTTP_200_OK)

        else:
            # User credentials are invalid, return an unauthorized response
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)



from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class alluser(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_data = User.objects.all()
        serializer = userSerializers(user_data,many=True)
        return Response(serializer.data)
    


class list_all_available_garage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        print(id,type(id))
        all_garage = spots.objects.filter(garage_id__zipcode= id,status=True)
        print(all_garage)
        serializer = spotsSerializers(all_garage,many=True)

        return Response(serializer.data)
    
class reserve_spot(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,spot_id):
        try:

            get_spot = spots.objects.get(id=spot_id)
        except spots.DoesNotExist:
             return Response({"error": "Spot not found"}, status=status.HTTP_404_NOT_FOUND)
        
        reservation_data = {
            'garage_id':get_spot.garage_id_id,
            'spot_id':get_spot.id,
            'payment':1
        }
        serializer_reservation = revervationSerializer(data=reservation_data)
        if serializer_reservation.is_valid():
            reservation = serializer_reservation.save()
            get_spot.status=False
            get_spot.save()

            transaction_data = {
                'reservation_id':reservation.id,
                'total_time':0,
                'payment_amount':0
            }
            serializer_transaction = transactionSerializer(data=transaction_data)
            if serializer_transaction.is_valid():
                serializer_transaction.save()
                return Response({"success": "Reservation and transaction created successfully"}, status=status.HTTP_201_CREATED)
            else:
                Reservations.delete()
                get_spot.status=True
                get_spot.save()
                return Response(serializer_transaction.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_reservation.errors, status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime
import math

def calculate_time_diff(start_datetime,end_datetie,rate_of_vicle):
    #convert datetime format to str format stat time and end time
    str_start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    str_end_time = end_datetie.strftime("%Y-%m-%d %H:%M:%S")

    start_time = datetime.strptime(str_start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(str_end_time, "%Y-%m-%d %H:%M:%S")
    time_difference_minutes = (end_time - start_time).total_seconds() / 60

    #calculate rate per minutes
    rate_per_min = rate_of_vicle / 60

    total_amount = round(rate_per_min * time_difference_minutes,2)

    #if total time difference is more than 60 min..convet it inhours and mintes

    hours = time_difference_minutes // 60
    remaining_minutes = time_difference_minutes % 60

    if hours > 0:
        if remaining_minutes > 0:
            total_time = f"{hours} hours {math.ceil(remaining_minutes)} minutes"
        else:
            total_time = f"{hours} hours"
    else:
        total_time = f"{math.ceil(remaining_minutes)} minutes"
    return total_time,total_amount




class reservation_close(APIView):
    def patch(self,request,reserve_id):
        print(reserve_id)
        try:
            reserve = Reservations.objects.get(id=reserve_id,payment=1)
        except Reservations.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        reserev_data_update = {
            'end_time':datetime.now(),
            'payment':2
        }
        # update_reserve_serializer = updateRevervationSerializer(reserve,data=request.data,partial=True)
        update_reserve_serializer = revervationSerializer(reserve,data=reserev_data_update,partial=True)
        with transaction.atomic():
            if update_reserve_serializer.is_valid():
                update_reserve_serializer.save() #not update reservation here becouse if transaction or spot 
                #update failed then reservatin stataus will update so we will added this line before transaction update

                try:
                    transcation = transactions.objects.get(reservation_id_id=reserve_id)
                except transactions.DoesNotExist:
                    return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
                total_time , payment_amount = calculate_time_diff(reserve.start_time,reserve.end_time,30)
                transaction_data_update = {
                    'total_time':total_time,
                    'payment_amount':payment_amount
                }
                # update_transaction_serializer = updateTransactionSerializer(transcation,data=request.data,partial=True)
                update_transaction_serializer = transactionSerializer(transcation,data=transaction_data_update,partial=True)
                if update_transaction_serializer.is_valid():
                   
                    update_transaction_serializer.save()
                    spot_data = spots.objects.get(id = reserve.spot_id.id)
                    spot_data.status = True
                    spot_data.save()
                    return Response({"success": "Reservation closed and data updated successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(update_transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(update_reserve_serializer.errors, status=status.HTTP_400_BAD_REQUEST)