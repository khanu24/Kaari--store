from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    """
    Display all available products or filter by selected category slug.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'current_category': category,
    })


def product_detail(request, slug):
    """
    Display a single product view with related category items.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    categories = Category.objects.all()

    # Fetch related products from the same category excluding the current product
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'categories': categories,
        'related_products': related_products,
    })