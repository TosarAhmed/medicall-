from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.models import UserOTP
from item.models import Category, Item
from .forms import SignupForm
import requests
import random
import uuid
from django.conf import settings
import re

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

    elif not request.session.get('user_id'):
        return redirect('core:login')
    else:
        return render(request, 'core/otp.html')

def userlogin(request):
    if request.method == 'POST':
        
        phone = request.POST.get('phone')
        if not validate_bangladeshi_mobile_number(phone):
            return render(request, 'core/login.html', {"error": "Invalid Phone number"})
        
        phone = validate_bangladeshi_mobile_number(phone)

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
            return redirect('core:verify-otp')
        else:
            return render(request, 'core/login.html', {"error": "User with this phone number does not exists!"})
    return render(request, 'core/login.html')

def signup(request):

    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        mobile_number = request.POST.get('mobile')
        
        if not validate_bangladeshi_mobile_number(mobile_number):
            return render(request, 'core/signup.html', {"error": "Invalid mobile number!"})
        
        # Conver into valid mobile number if string exists it can detect it
        mobile_number = validate_bangladeshi_mobile_number(mobile_number)

        username = generate_unique_username()

        if mobile_number and full_name:
            if UserOTP.objects.filter(mobile=mobile_number).exists():
                return render(request, 'core/signup.html', {"error": "An account with this phone number already exists!"})
            else:
                new_user = User.objects.create_user(
                    username=username,
                    first_name=full_name,
                    password='@Xuser123$'
                )
                if new_user:
                    otp_code = str(random.randint(100000, 999999))
                    new_otp_model = UserOTP.objects.create(user=new_user, mobile=mobile_number, otp_code=otp_code)
                    send_otp(new_otp_model)
                    request.session['user_id'] = new_user.id
                    return redirect('core:verify-otp')
                else:
                    return render(request, 'core/signup.html', {"error": "New user creation failed! try again later."})
        else:
            return render(request, 'core/signup.html', {"error": "Full name and Mobile number is required!"})
     
    return render(request, 'core/signup.html')
 

def send_otp(userOtpModel):

    message = f"""
    Hi {userOtpModel.user.first_name},
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
    

def generate_unique_username(base_name="user"):
    while True:
        unique_username = f"{base_name}_{uuid.uuid4().hex[:8]}"
        if not User.objects.filter(username=unique_username).exists():
            return unique_username
        
def validate_bangladeshi_mobile_number(number_str):
    pattern = r'^01[3-9]\d{8}$'
    if re.match(pattern, number_str):
        # Convert the valid string to an integer
        return int(number_str)
    else:
        # Return an error message if the number is invalid
        return False