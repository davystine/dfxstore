from .cart import Cart

#context processor so cart can work on all pages
def cart(request):
    #return the default data from our cart
    return{'cart': Cart(request)}