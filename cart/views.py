from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .models import Order, OrderItem


def cart_detail(request):
    cart = Cart(request)
    template = 'cart/partials/cart_drawer.html' if request.headers.get('HX-Request') else 'cart/cart_detail.html'
    return render(request, template, {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Extract quantity and override parameters safely
    try:
        quantity = max(1, int(request.POST.get('quantity', 1)))
    except (ValueError, TypeError):
        quantity = 1

    override = str(request.POST.get('override', '')).lower() in ['true', '1']

    cart.add(product_id=product.id, quantity=quantity, override_quantity=override)

    # Return partial drawer for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'cart/partials/cart_drawer.html', {'cart': cart})

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    # Return partial drawer for HTMX requests, redirect for standard requests
    if request.headers.get('HX-Request'):
        return render(request, 'cart/partials/cart_drawer.html', {'cart': cart})

    return redirect('cart:cart_detail')


def checkout(request):
    cart = Cart(request)

    # Redirect to product catalog if cart is empty
    if len(cart) == 0:
        return redirect('store:product_list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()

        if full_name and email and phone and address and city:
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                total_amount=cart.get_final_total(),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'cart/order_success.html', {'order': order})

    return render(request, 'cart/checkout.html', {'cart': cart})