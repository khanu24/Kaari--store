from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product
from cart.models import Order, OrderItem


class CartAndCheckoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Caps', slug='caps')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Cap',
            slug='test-cap',
            price=2500.00,
            is_available=True
        )

    def test_categories_context_processor_on_cart_page(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        self.assertEqual(list(response.context['categories']), [self.category])

    def test_cart_add_and_drawer_htmx(self):
        # Test HTMX POST to add product
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 2},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart (2)')
        self.assertContains(response, 'Test Cap')

    def test_cart_remove_htmx(self):
        # Add first
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        # Remove via POST with HTMX
        response = self.client.post(
            reverse('cart:cart_remove', args=[self.product.id]),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart is Empty')

    def test_checkout_creates_order_and_clears_cart(self):
        # Add product to cart
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 2})

        # Submit checkout POST
        checkout_data = {
            'full_name': 'Ali Khan',
            'email': 'ali@example.com',
            'phone': '03001234567',
            'address': 'House 123, Street 4',
            'city': 'Lahore',
            'postal_code': '54000',
            'payment_method': 'cod',
        }
        response = self.client.post(reverse('cart:checkout'), checkout_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Confirmed!')
        self.assertContains(response, 'Ali Khan')

        # Check DB
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.full_name, 'Ali Khan')
        self.assertEqual(order.total_amount, 5250.00)
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)

        # Check cart is cleared
        session_cart = self.client.session.get('cart_session_key')
        self.assertTrue(session_cart is None or len(session_cart) == 0)
