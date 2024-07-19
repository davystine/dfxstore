from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress




def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_items = cart.get_items
    quantities = cart.get_qty()
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        #checkout as registered user
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
    return render( request, "payment/checkout.html", 
                  {"cart_items": cart_items, 
                   "quantities": quantities, 
                   "totals": totals, 
                   "shipping_form": shipping_form})