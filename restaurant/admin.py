# restaurant/admin.py

from django.contrib import admin
from .models import MenuItem, RestaurantTable, Order, OrderItem


# ──────────────────────────────────────────
# ORDERITEM INLINE
# Shows order items directly inside the Order page
# ──────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model          = OrderItem
    extra          = 0
    readonly_fields = ['unit_price']
    fields         = ['menu_item', 'quantity', 'unit_price']


# ──────────────────────────────────────────
# MENUITEM ADMIN
# ──────────────────────────────────────────
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display   = ['name', 'category', 'cuisine', 'price', 'is_available', 'updated_at']
    list_filter    = ['category', 'cuisine', 'is_available']
    search_fields  = ['name', 'description']
    list_editable  = ['price', 'is_available']
    ordering       = ['category', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Classification', {
            'fields': ('category', 'cuisine')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


# ──────────────────────────────────────────
# RESTAURANTTABLE ADMIN
# ──────────────────────────────────────────
@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):

    list_display  = ['table_number', 'capacity', 'is_occupied']
    list_filter   = ['is_occupied', 'capacity']
    ordering      = ['table_number']


# ──────────────────────────────────────────
# ORDER ADMIN
# ──────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display   = ['id', 'table', 'status', 'total_price', 'created_at']
    list_filter    = ['status', 'created_at']
    search_fields  = ['id', 'table__table_number']
    ordering       = ['-created_at']
    readonly_fields = ['total_price', 'created_at', 'updated_at']

    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('table', 'status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ──────────────────────────────────────────
# ORDERITEM ADMIN
# ──────────────────────────────────────────
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display  = ['id', 'order', 'menu_item', 'quantity', 'unit_price']
    search_fields = ['order__id', 'menu_item__name']
    ordering      = ['order']