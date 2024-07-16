from store.models import Item

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})
        
    def add(self, item, quantity):
        item_id = str(item.id)
        item_qty = int(quantity)
        
        if item_id in self.cart:
            self.cart[item_id] += item_qty
        else:
            self.cart[item_id] = item_qty
        
        self.save()
    
    def __len__(self):
        return sum(item_qty for item_qty in self.cart.values())
    
    def get_items(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        return items
    
    def get_qty(self):
        return self.cart
    
    def update(self, item_id, quantity):
        item_id_str = str(item_id)
        item_qty = int(quantity)
        
        if item_qty == 0:
            self.delete(item_id)
        else:
            if item_id_str in self.cart:
                self.cart[item_id_str] = item_qty
                self.save()
            else:
                raise ValueError(f"Item with id {item_id} does not exist in the cart.")
    
    def delete(self, item_id):
        item_id_str = str(item_id)
        
        if item_id_str in self.cart:
            del self.cart[item_id_str]
            self.save()
            
    def cart_total(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for item in items:
                if item.id == key:
                    if item.on_sale:
                        total = total + (item.sale_price * value)
                    else:
                        total = total + (item.price * value)         
        return total
        
    
    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
