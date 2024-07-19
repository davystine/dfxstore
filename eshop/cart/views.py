from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Item
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_items = cart.get_items
    quantities = cart.get_qty()
    totals = cart.cart_total()
    return render( request, "cart/cart_summary.html", {"cart_items": cart_items, "quantities": quantities, "totals": totals})

def cart_add(request):
    cart = Cart(request)  # Assuming you have a Cart class or module
    
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
        
        item = get_object_or_404(Item, id=item_id)
        
        # Check if there's enough stock
        if item_qty > item.units_in_stock:
            return JsonResponse({'error': 'Not enough stock available'})
        
        # Add item to cart
        cart.add(item=item, quantity=item_qty)
        
        # Reduce stock quantity
        item.units_in_stock -= item_qty
        item.save()
        
        # Return JSON response with updated cart quantity and remaining stock
        cart_quantity = len(cart) # Adjust this based on your Cart implementation
        updated_stock = item.units_in_stock
        
        return JsonResponse({'qty': cart_quantity, 'updated_stock': updated_stock})
    
    return JsonResponse({'error': 'Invalid request'})

def cart_update(request):
    if request.method == 'POST' and request.POST.get('action') == 'post':
        print("Entered cart_update function")  # Debug line

        cart = Cart(request)
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))

        item = get_object_or_404(Item, id=item_id)

        print(f"Updating item_id={item_id} with item_qty={item_qty}")  # Debug line

        if item_qty > item.units_in_stock:
            print("Not enough stock available")  # Debug line
            return JsonResponse({'error': f'Only {item.units_in_stock} units available in stock.'}, status=400)

        if str(item_id) not in cart.get_qty():
            print(f"Item with id {item_id} does not exist in the cart.")  # Debug line
            return JsonResponse({'error': f'Item with id {item_id} does not exist in the cart.'}, status=400)

        old_qty = cart.get_qty().get(str(item_id), 0)
        qty_diff = item_qty - old_qty
        print(f"Old quantity: {old_qty}, New quantity: {item_qty}, Quantity difference: {qty_diff}")  # Debug line

        if item_qty == 0:
            print(f"Deleting item {item_id}")  # Debug line
            return JsonResponse({'delete_confirmation': True, 'item_id': item_id, 'item_name': item.name})

        cart.update(item_id=item_id, quantity=item_qty)
        item.units_in_stock -= qty_diff
        item.save()

        cart_quantity = len(cart)
        updated_total = cart.cart_total()

        print(f"Cart updated. New quantity: {cart_quantity}, New total: {updated_total}")  # Debug line

        return JsonResponse({
            'qty': cart_quantity,
            'units_in_stock': item.units_in_stock,
            'updated_total': updated_total
        })

    print("Invalid request method or action.")  # Debug line
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        item_id = int(request.POST.get('item_id'))
        cart = Cart(request)
        
        # Get current cart quantity of the item
        current_qty = cart.get_qty().get(str(item_id), 0)
        
        # Remove the item from the cart
        cart.delete(item_id=item_id)
        
        # Reload the item object to get the latest stock
        item = get_object_or_404(Item, id=item_id)
        
        # Restore the stock to reflect the removed item
        item.units_in_stock += current_qty
        item.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

