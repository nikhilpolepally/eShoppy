

from math import ceil
from urllib.request import HTTPBasicAuthHandler

import requests
from app.models import Category, Contact, Order, Product
from eShoppy import settings
from django.shortcuts import redirect, render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#Initate RazorPay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def Index(request):
    allProds = []
    catprods = Product.objects.values('deals', 'id')
    cats = {item['deals'] for item in catprods}
    for cat in cats:
        print(cat)
        if cat == "Best Offers" or cat == "Most Popular" or cat=="Fruits and Vegetables" or cat=="Snacks Store":
            prod = Product.objects.filter(deals=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "index.html", params)

def BySearch(request, name):
    catprods = Product.objects.filter(product_name__icontains=name)
    params = {'allProds': catprods}
    return render(request, "search.html", params)

def ByCategory(request, slug):
    allProds = []
    catprods = Category.objects.get(slug=slug)
    prodlist = Product.objects.filter(category=catprods)
    params = {'allProds': prodlist}
    return render(request, "products.html", params)


def AbouUs(request):
    return render(request, "about.html")

def Team(request):
    return render(request, "team.html")

def HandleContact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Contacts=Contact(name=name,email=email,subject=subject,message=message)
        Contacts.save()
        messages.info(request, "We received you request and we will get back to you soon..")
        return render(request, "contact.html")
    if request.method == "GET":
        return render(request, "contact.html")

def Cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/account/login')
    return render(request, "cart.html")


def Checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/account/login')
    if request.method == "POST":
        order_items = request.POST.get('order_items', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Orders = Order(order_items=order_items,amount=amount, name=name, delivery_email=email, user_email=request.user.email,address=address,city=city, state=state,zip_code=zip_code,phone=phone)
        Orders.save()

# # RAZOR PAY INTEGRATION
        order_id = Orders.order_id
        print(order_id)
        order_amount = int(amount)*100  # 9900
        new_order_response = razorpay_client.order.create({
            "amount": order_amount,
            "currency": "INR",
                        "payment_capture": "1"
        })
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(
            request,
            "checkout.html",
            {
                "callback_url": settings.DOMAIN + "/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": new_order_response,
                "order_id": order_id
            },
        )

    return render(request, 'checkout.html')


@csrf_exempt
def Callback(request):
    data = {}
    try:
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        orderid = request.POST.get('order_id', '')
        callUrl = "https://api.razorpay.com/v1/payments/"+razorpay_payment_id
        response = requests.get(callUrl, auth=HTTPBasicAuthHandler(
            settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print(response)
        if response.status_code == 200:
            Order = Order.objects.get(orderid=orderid)
            Order.payment_id = razorpay_payment_id
            Order.save()
            data = response.json()

        else:
            print('Error:', response.status_code)

        # verify the payment signature.

        return render(request, "payment.html", {'response': data})
    except:
        return render(request, "payment.html", {'response': data})
    
