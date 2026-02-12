from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Order, OrderItem
from django.db.models import Sum


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'payment_method',
        'total_amount',
        'colored_payment_status',
        'created_at',
    )

    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('id', 'user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_amount')
    inlines = [OrderItemInline]

    def colored_payment_status(self, obj):
        colors = {
            'PAID': 'green',
            'PENDING': 'orange',
            'FAILED': 'red',
        }
        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(obj.payment_status, 'gray'),
            obj.payment_status
        )

    colored_payment_status.short_description = "Payment Status"

    # 🔥 ADMIN DASHBOARD STATS
    def changelist_view(self, request, extra_context=None):
        stats = Order.objects.aggregate(
            total_orders=models.Count('id'),
            paid_orders=models.Count('id', filter=models.Q(payment_status='PAID')),
            pending_orders=models.Count('id', filter=models.Q(payment_status='PENDING')),
        )

        revenue = 0
        for order in Order.objects.filter(payment_status='PAID'):
            revenue += order.get_total_cost()

        extra_context = extra_context or {}
        extra_context['stats'] = {
            'total_orders': stats['total_orders'],
            'paid_orders': stats['paid_orders'],
            'pending_orders': stats['pending_orders'],
            'revenue': revenue,
        }

        return super().changelist_view(request, extra_context=extra_context)
