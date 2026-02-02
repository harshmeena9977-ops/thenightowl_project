from django.shortcuts import render

# Create your views here.
import razorpay
from django.conf import settings
from wallets.models import Wallet, Transaction

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def add_money(request):
    amount = int(request.POST.get('amount'))
    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })
    return render(request, 'payments/pay.html', {'order': order})