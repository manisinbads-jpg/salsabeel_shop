from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductVariant


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for key, item in cart.items():
        product = get_object_or_404(Product, id=item['product_id'])
        variant = get_object_or_404(ProductVariant, id=item['variant_id'])

        quantity = item['quantity']
        price = float(variant.price)
        subtotal = price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'variant': variant,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart/detail.html', {
        'cart_items': cart_items,
        'total': total,
    })



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    size = request.POST.get('size')
    color = request.POST.get('color')
    quantity = int(request.POST.get('quantity', 1))

    variant = get_object_or_404(
        ProductVariant,
        product=product,
        size=size,
        color=color
    )

    cart = request.session.get('cart', {})

    key = f"{product_id}-{variant.id}"

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'product_id': product_id,
            'variant_id': variant.id,
            'size': size,
            'color': color,
            'price': float(variant.price),
            'quantity': quantity,
        }

    request.session['cart'] = cart

    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

    return redirect('cart:cart_detail')
