from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'city', 'total_amount', 'status', 'paid', 'created_at']
    list_filter = ['status', 'paid', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'address']
    inlines = [OrderItemInline]
