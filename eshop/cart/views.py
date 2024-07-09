from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Item
from django.http import JsonResponse


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_items = cart.get_items
    quantities = cart.get_qty()
    return render( request, "cart_summary.html", {"cart_items": cart_items, "quantities": quantities})


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
        cart_quantity = cart.__len__()  # Adjust this based on your Cart implementation
        updated_stock = item.units_in_stock
        
        return JsonResponse({'qty': cart_quantity, 'updated_stock': updated_stock})
    
    return JsonResponse({'error': 'Invalid request'})


def cart_update(request):
    if request.method == 'POST' and request.POST.get('action') == 'post':
        cart = Cart(request)
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))

        # Fetch the item from the database
        item = get_object_or_404(Item, id=item_id)

        if item_qty > item.units_in_stock:
            return JsonResponse({'error': f'Only {item.units_in_stock} units available in stock.'}, status=400)

        # Check if the item exists in the cart
        if str(item_id) not in cart.get_qty():
            return JsonResponse({'error': f'Item with id {item_id} does not exist in the cart.'}, status=400)

        old_qty = cart.get_qty().get(str(item_id), 0)
        qty_diff = item_qty - old_qty

        if item_qty == 0:
            return JsonResponse({'delete_confirmation': True, 'item_id': item_id, 'item_name': item.name})

        # Update the cart
        cart.update(item_id=item_id, quantity=item_qty)
        item.units_in_stock -= qty_diff
        item.save()

        return JsonResponse({'units_in_stock': item.units_in_stock})

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