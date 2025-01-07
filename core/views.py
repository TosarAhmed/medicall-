from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.models import UserOTP
from item.models import Category, Item
from .forms import SignupForm
import requests
import random
from django.conf import settings

def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    # return render(request, 'core/index.html', {
    #     'categories': categories,
    #     'items': items,
    # })
    return redirect('item:items')

def contact(request):
    return render(request, 'core/contact.html')

def verify_otp(request):
    if request.method == 'POST':
        userid = request.session.get('user_id')

        
        otp = request.POST.get('otp')

        if User.objects.filter(id=userid).exists():
            user = User.objects.get(id=userid)
            
            check = UserOTP.objects.filter(user=user, otp_code=otp).first()
             
            if check:
                login(request, user)
                return redirect('/')
            else:
                user_id = request.session.get('user_id')
                return render(request, 'core/otp.html', {"userid": user_id, 'error': 'Wrong OTP Code'})

        return redirect('core:login')

    else:
        return redirect('core:login')

def userlogin(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if UserOTP.objects.filter(mobile=phone).exists():
            # random 6 digit otp code 
            otp_code = str(random.randint(100000, 999999))
            # Otp model
            otpModel = UserOTP.objects.get(mobile=phone)
            # Save randomly generated otp into otp model
            otpModel.otp_code = otp_code
            otpModel.save()
            # Send top to user phone number
            send_otp(otpModel)
            request.session['user_id'] = otpModel.user.id
            return render(request, 'core/otp.html', {"userid": otpModel.user.id})
        else:
            return render(request, 'core/login.html', {"error": "User with this phone number does not exists!"})
    return render(request, 'core/login.html')

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect ('/login/')

    else:

        form = SignupForm()
    return render(request, 'core/signup.html',  {"form": form})
 

def send_otp(userOtpModel):

    message = f"""
    Hi {userOtpModel.user.username},
    Your OTP code for Medicall+ is: {userOtpModel.otp_code}
    """
    url = "http://bulksmsbd.net/api/smsapi"
    params = {
        "api_key": settings.BULK_SMS_API_KEY,
        "type": "text",
        "number": userOtpModel.mobile,
        "senderid": settings.BULK_SMS_SENDER_ID,
        "message": message,
    }

    try:
        response = requests.get(url, params=params)
        # print("Bulk sms response", response)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        res = response.json()
        return res  # Parse and return the JSON response
    except requests.RequestException as e:
        return {"error": str(e)}