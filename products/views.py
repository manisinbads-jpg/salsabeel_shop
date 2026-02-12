from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from cart.cart import Cart


# Home page / shop listing
def product_list(request):
    """
    Display all products and categories.
    Home page can also reuse this view.
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })


# Products filtered by category
def product_list_by_category(request, slug):
    """
    Show products for a specific category (using slug).
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })


# Product detail page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    variants = product.variants.all()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
    })

# Cart pages
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'products/cart_detail.html', {'cart': cart})


def add_to_cart(request, product_id):
    """
    Add a product to cart.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect('products:cart_detail')


def remove_from_cart(request, product_id):
    """
    Remove a product from cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('products:cart_detail')


# Optional: simple home page (hero + video + categories)
from products.models import Product



def home(request):
    categories = Category.objects.all()

    # Get new products (latest 8 for example)
    new_products = Product.objects.filter(is_new=True)[:8]

    # Get promo products (latest 8 for example)
    promo_products = Product.objects.filter(is_promo=True)[:8]

    context = {
        "categories": categories,
        "new_products": new_products,
        "promo_products": promo_products,
    }

    return render(request, "products/home.html", context)




def about(request):
    return render(request, 'products/about.html')


def contact(request):
    return render(request, 'products/contact.html')


def new_arrivals(request):
    products = Product.objects.filter(is_new=True)
    return render(request, 'products/new_arrivals.html', {'products': products})


def promotions(request):
    products = Product.objects.filter(is_promo=True)
    return render(request, 'products/promotions.html', {'products': products})
