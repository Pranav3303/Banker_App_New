from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from math import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
import paypalrestsdk
from django.conf import settings
from django.urls import reverse

# Create your views here.

def Home(request):
    df = employee.objects.all()
    df_pagenator = Paginator(df,9)
    pagenum = request.GET.get('page')
    page = df_pagenator.get_page(pagenum)
    # context = {'page':page,
    # 'total_no_page' : ceil(df_pagenator.count/3),
    # 'total_no_data' : df_pagenator.count
    # }

    df1 = service.objects.all()
    df1_pagenator = Paginator(df1,6)
    pagenum1 = request.GET.get('page1')
    page1 = df1_pagenator.get_page(pagenum1)


    return render(request, "index.html", {'page':page, 'page1':page1})


def signup(request):
    if request.method == 'POST':
        first = request.POST['fn']
        last = request.POST['ln']
        email = request.POST['eid']
        username = request.POST['username']
        pw1 = request.POST['pw1']
        pw2 = request.POST['pw2']

        if pw1 == pw2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email is already taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username,password=pw1,email=email,first_name=first,last_name=last)
                user.save()
                return redirect("signin")
        else:
            messages.info(request,"Password Mismatch, Try Again")
            return redirect("signup")
        
    return render(request,'signup.html')


def signout(request):
    logout(request)
    return redirect('/')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pw']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credential, Please Try Again")
            return redirect('signin')

    return render(request, 'signin.html')

def profile_detail(request):
    return redirect(request, 'profile_detail')


def contact1(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        categeory = request.POST['categeory']
        decribe = request.POST['decribe']
                
        df2=contact.objects.create(name=name, email=email, phone=phone, categeory=categeory, decribe=decribe)
        df2.save()
        return redirect("/")
    else:
        messages.info(request, "Please fill out all fields.")
        return render(request , 'contact.html')
    
    # return render(request, 'contact.html')



def getInTouch(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        categeory = request.POST['categeory']
        decribe = request.POST['decribe']
                
        df3=contact.objects.create(name=name, email=email, phone=phone, categeory=categeory, decribe=decribe)
        df3.save()
        return redirect('/')
    else:
        messages.info(request, "Please fill out all fields.")
        return render(request,'getInTouch.html')   
    
    # return render(request, 'getInTouch.html')


def contactform(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        df4 = contactForm.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        df4.save()
        return redirect('/')
    
    else:
        messages.info(request, "Please fill out all fields.")
        return redirect('contactForm')


def payment(request):
    """View to display the payment plans."""
    return render(request, 'payment.html')

def create_payment(request, plan):
    """View to create a PayPal payment based on the selected plan."""
    # Determine pricing and plan based on the `plan` argument
    if plan == 'basic':
        amount = 47.00
        item_name = 'Basic Plan'
    elif plan == 'premium':
        amount = 200.00
        item_name = 'Premium Plan'
    elif plan == 'professional':
        amount = 750.00
        item_name = 'Professional Plan'
    else:
        return HttpResponse("Invalid plan selected", status=400)

    # Create PayPal payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "USD"
            },
            "description": item_name
        }],
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
        }
    })

    # Create the payment and redirect to PayPal for approval
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        return HttpResponse("Error creating PayPal payment: " + str(payment.error), status=400)


def execute_payment(request):
    """View to execute PayPal payment after user approval."""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Fetch the payment from PayPal
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html', {'payment':payment})
    else:
        return HttpResponse("Error executing payment: " + str(payment.error), status=400)



def payment_cancel(request):
    """View to show payment cancellation."""
    return render(request, 'payment_cancel.html')