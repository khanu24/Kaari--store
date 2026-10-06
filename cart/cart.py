from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart_session_key')
        if not cart:
            cart = self.session['cart_session_key'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, override_quantity=False):
        product_id = str(product_id)
        product = Product.objects.get(id=product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        else:
            self.cart[product_id]['price'] = str(product.price)

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for p_id, item_data in self.cart.items():
            if p_id in product_map:

                item = {
                    'quantity': item_data['quantity'],
                    'price': Decimal(item_data['price']),
                    'product': product_map[p_id],
                }
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if 'cart_session_key' in self.session:
            del self.session['cart_session_key']
            self.save()