from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress



def payment_success(request):
     # Clear the cart
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Payment successful. Your order is on the way!")
    return redirect('store:home')
    


def checkout(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    quantities = cart.get_qty()
    totals = cart.cart_total()

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Checkout as registered user
            shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
            shipping_form = ShippingForm(request.POST, instance=shipping_user)
        else:
            # Checkout as guest
            shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            shipping_form.save()  # Save the shipping address
            # Redirect to the payment page
            return redirect('payment:checkout')
        else:
            # If form is invalid, add errors to messages and re-render the form
            for field in shipping_form.errors:
                for error in shipping_form.errors[field]:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        if request.user.is_authenticated:
            # Checkout as registered user
            shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
            shipping_form = ShippingForm(instance=shipping_user)
        else:
            # Checkout as guest
            shipping_form = ShippingForm()

    return render(request, "payment/checkout.html", {
        "cart_items": cart_items,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })
