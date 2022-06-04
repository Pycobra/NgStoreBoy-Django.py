from django.urls import path
from . import views

app_name="payment_"
urlpatterns = [
    path('', views.payment, name="payment"),
    path('initiate_payment/', views.initiate_payment, name="initiate_payment"),
    path('<str:ref>/', views.verify_payment, name="verify_payment"),
    path('orderplaced/', views.order_placed, name="order_placed"),
    #path("paystack", include(('paystack.urls', 'paystack'),namespace='paystack'))
    #path('webhook/', views.stripe_webhook, name="webhook"),
]
