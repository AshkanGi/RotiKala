from product.models import Product


CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['color'], item['size'])
            yield item

    def unique_id_generator(self, id, color, size):
        result = f'{id}-{color}-{size}'
        return result

    def add(self, product, quantity, color, size):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = {
                'quantity': 0,
                'price': str(product.price),
                'color': color,
                'size': size,
                'id': product.id
            }
        self.cart[unique]['quantity'] += int(quantity)
        self.session.modified = True

    def remove(self, id):
        if id in self.cart:
            del self.cart[id]
            self.session.modified = True

    def clear(self):
        self.session.pop(CART_SESSION_ID, None)
        self.session.modified = True

    def total_products(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def total_price(self):
        return sum(int(item['quantity']) * int(item['price']) for item in self.cart.values())