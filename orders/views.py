# orders/views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReceiptUploadForm
from .models import Order, OrderItem
from cart.cart import Cart
import urllib.parse


# SUCCESS PAGE
@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})



# ORDER HISTORY
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders/history.html', {'orders': orders})



# ORDER LIST
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

# ORDER DETAIL
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# UPLOAD RECEIPT
@login_required
def upload_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order.payment_status = 'PENDING'
            form.save()
            return redirect('orders:success', order_id=order.id)
    else:
        form = ReceiptUploadForm(instance=order)

    return render(request, 'orders/upload_receipt.html', {'form': form, 'order': order})

# PAYMENT PAGE
# orders/views.py
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    message = f"Order #{order.id}\n"
    for item in order.items.all():
        message += f"{item.product.name} x{item.quantity} = {item.get_cost()} TZS\n"
    message += f"\nTotal: {order.get_total_cost()} TZS"

    whatsapp_message = urllib.parse.quote(message)

    return render(request, 'orders/payment.html', {
        'order': order,
        'whatsapp_message': whatsapp_message
    })


@login_required
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.payment_status = "PAID"
    order.save()
    messages.success(request, "Payment confirmed! Thank you.")
    return redirect('orders:success', order_id=order.id)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Order


def order_invoice_pdf(request, order_id):
    order = Order.objects.get(id=order_id)

    template = get_template('orders/invoice.html')
    html = template.render({'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response






# CREATE ORDER (SAFE VERSION)
@login_required
@transaction.atomic
def create(request):
    cart = Cart(request)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('cart:cart_detail')

        # Create the order
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Clear cart
        cart.clear()

        # Redirect to payment page
        return redirect('orders:payment', order_id=order.id)

