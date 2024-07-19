from store.models import Item, UserProfile
import json

class Cart():
    def __init__(self, request):
        # Initialize the cart with session and request
        self.session = request.session
        self.request = request
        self.cart = self.session.get('cart', {})
        
    def add(self, item, quantity):
        # Add an item to the cart
        item_id = str(item.id)
        item_qty = int(quantity)
        
        # If item already in cart, increase its quantity, otherwise add it
        if item_id in self.cart:
            self.cart[item_id] += item_qty
        else:
            self.cart[item_id] = item_qty
             
        self.save()
        
        # If user is authenticated, update the cart in the user profile
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user)
            cart_str = json.dumps(self.cart)
            user_profile.update(cart=cart_str)
    
    def database_add(self, item, quantity):
        # Similar to add method but with item passed as an ID
        item_id = str(item)
        item_qty = int(quantity)
        
        if item_id in self.cart:
            self.cart[item_id] += item_qty
        else:
            self.cart[item_id] = item_qty
             
        self.save()
        
        # If user is authenticated, update the cart in the user profile
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user)
            cart_str = json.dumps(self.cart)
            user_profile.update(cart=cart_str)
    
    def __len__(self):
        # Return the total number of items in the cart
        return sum(item_qty for item_qty in self.cart.values())
    
    def get_items(self):
        # Retrieve all items in the cart from the database
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        return items
    
    def get_qty(self):
        # Return the quantities of items in the cart
        return self.cart
    
    def update(self, item_id, quantity):
        # Update the quantity of a specific item in the cart
        item_id_str = str(item_id)
        item_qty = int(quantity)
        
        # If quantity is 0, remove the item from the cart
        if item_qty == 0:
            self.delete(item_id)
        else:
            if item_id_str in self.cart:
                self.cart[item_id_str] = item_qty
                self.save()
                
                # If user is authenticated, update the cart in the user profile
                if self.request.user.is_authenticated:
                    user_profile = UserProfile.objects.filter(user=self.request.user)
                    cart_str = json.dumps(self.cart)
                    user_profile.update(cart=cart_str)
            else:
                raise ValueError(f"Item with id {item_id} does not exist in the cart.")
    
    def delete(self, item_id):
        # Remove an item from the cart
        item_id_str = str(item_id)
        
        if item_id_str in self.cart:
            del self.cart[item_id_str]
            self.save()
              
            # If user is authenticated, update the cart in the user profile
            if self.request.user.is_authenticated:
                user_profile = UserProfile.objects.filter(user=self.request.user)
                cart_str = json.dumps(self.cart)
                user_profile.update(cart=cart_str)
    
    def cart_total(self):
        # Calculate the total cost of all items in the cart
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        quantities = self.cart
        total = 0
        
        # Iterate through each item in the cart to calculate the total
        for key, value in quantities.items():
            key = int(key)
            for item in items:
                if item.id == key:
                    if item.on_sale:
                        total += item.sale_price * value
                    else:
                        total += item.price * value         
        return total
        
    def save(self):
        # Save the cart back into the session and mark it as modified
        self.session['cart'] = self.cart
        self.session.modified = True
        
    def clear(self):
        # Clear the cart
        self.cart = {}
        self.session['cart'] = self.cart
        self.session.modified = True
