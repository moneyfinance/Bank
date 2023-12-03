from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Bank.settings import api_key
import requests, random
from .serializer import Otp_serializer,UserSerializer
from .models import Otp,User
import json




@api_view(['POST'])
def check(request):
    print(request.data['phone_number'])
    return Response({"message":"done"},status=status.HTTP_200_OK)

@api_view(['GET'])
def login_page(request):
    return render(request,'login.html')

@api_view(['POST'])
def user_info(request):
    return render(request,'user_data.html')

@api_view(['GET','POST'])
def registration_verification(request):
    data = request.data
    print(data)
    phone_number = data.get('phone_number')
    otp = data.get('otp')
    user = Otp.objects.filter(phone_number = phone_number , otp = otp).first()
    if user is None:
        return Response({"message : Wrong otp. Please enter correct otp"},status=status.HTTP_404_NOT_FOUND)
    
    user = User.objects.filter(phone_number = phone_number).first()
    if user is None:
        user_data = {
            'phone_number' : phone_number,
            'is_phone_verified' : True,
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
        }
        serializer = UserSerializer(data = user_data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        s = serializer.save()
        data = {
            'id' : s.id,
        }
        return Response(data , status=status.HTTP_200_OK)
    else:
        data = {
            'id' : user.id,
        }
        return Response(data , status=status.HTTP_200_OK)
    return Response({"message : Registration successfull"} , status=status.HTTP_200_OK)


@api_view(['GET'])
def user_page(request,id):
    return render(request,'user_data.html')


@api_view(['POST'])
def send_otp(request):
    data = request.data
    if data.get('phone_number') is None:
        return Response({
            'message': 'phone_number is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    phone_number = "+91" + data['phone_number']
    
    try:
        otp = random.randint(1000, 9999)
        user = Otp.objects.filter(phone_number=data['phone_number']).first()
        if user is None:
            n_data = {
                'phone_number': data['phone_number'],
                'otp': otp
            }
            serializer = Otp_serializer(data=n_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.otp = otp
            user.save()

        url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/OTP1"
        response = requests.get(url)

        if response.status_code == 200:
            return Response({"message": "Otp sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "something wrong with api"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

