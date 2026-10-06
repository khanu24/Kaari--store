from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    template = 'cart/partials/cart_drawer.html' if request.headers.get('HX-Request') else 'cart/cart_detail.html'
    return render(request, template, {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Extract quantity and override parameters from POST request
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', False)

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
        # Process order submission (Database saving logic will go here)
        cart.clear()
        return render(request, 'cart/order_success.html')

    return render(request, 'cart/checkout.html', {'cart': cart})