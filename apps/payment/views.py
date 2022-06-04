import json

from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from decimal  import Decimal
from django.http import HttpResponse
from django.http.request import HttpRequest

from apps.cart.cart import Cart
from apps.cart.forms import CheckoutForm
from apps.order.utilities import checkout, email_notify_vendor, email_notify_customer, payment_confirmation
from apps.vendor.models import Vendor
from apps.product.models import Product
#import stripe

from .forms import PaymentForm
from .models import Payment

@login_required
def CartView(request):
    #(id__in=id, category__slug=slug)
    newest_products = Product.objects.filter(is_active=True, in_stock=True).order_by('-date_added')[:3]
    #newest_products = Product.product_manager.all().order_by('-date_added')[:3]
    return render(request, 'payment/payment.html', {'newest_products': newest_products})

@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        """if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            try:
                charge = stripe.Charge.create(
                    amount=int(account.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from eCommerce',
                    source=stripe_token
                )
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                orderReciept = checkout(request, first_name, last_name, email, address, zipcode, place, phone, account.get_total_cost())
                account.clear()

                email_notify_vendor(orderReciept)
                email_notify_customer(orderReciept)

                return redirect('cart_:success_')

            except Exception:
                messages.error(request, 'There was something wrong with the payment')"""
    else:
        form = CheckoutForm()
    return render(request, 'payment/payment.html')  #, {'form': form})  # , 'stripe_pub_key':settings.STRIPE_PUB_KEY})


@login_required
def payment(request):
    cart = Cart(request)
    """
    try:
        total = str(chats.get_total_price())
        total = total.replace('.','')
        #total = int(total)
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gpb',
            metadata={'userid': request.user.id}
        )
        return render(request, 'payment/payment.html', {'client_secret': intent.client_secret})
    
    except Exception:
        #messages.error(request, 'There was something wrong with the payment')
    """

"""
#
@csrf_exempt
def stripe_webhook(request):
    payload=request.body
    event=None
    try:
        event=stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    if event.type== 'payment_intent_succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)"""

def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')

@login_required
def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment =payment_form.save()
            return render(request, 'payment/make_payment.html', {'payment':payment,
                                                                 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form=PaymentForm()
    return render(request, 'payment/initiate_payment.html', {'payment': payment_form})

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Veriication Successful")
    if verified:
        messages.error(request, "Veriication Failed")
    return redirect('payment_:initiate_payment')



"""
PAYSTACK_SECRET_KEY=os.environ.get(PAYSTACK_SECRET_KEY)
CRISPY_TEMPLATE_PACK="bootstrap4"
"""