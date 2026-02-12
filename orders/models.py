from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('MOBILE', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('COD', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    receipt = models.ImageField(
        upload_to='receipts/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    # ✅ total order cost
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # ✅ admin display helper
    def total_amount(self):
        return self.get_total_cost()

    total_amount.short_description = "Total Amount"

    def invoice_number(self):
        return f"INV-{self.id:06d}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(default=1)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def get_cost(self):
        return self.price * self.quantity
