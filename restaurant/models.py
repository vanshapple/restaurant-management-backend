# restaurant/models.py

from django.db import models


# ──────────────────────────────────────────
# MODEL 1: MenuItem
# ──────────────────────────────────────────
class MenuItem(models.Model):

    CATEGORY_CHOICES = [
        ('starter',   'Starter'),
        ('main',      'Main Course'),
        ('dessert',   'Dessert'),
        ('beverage',  'Beverage'),
    ]

    CUISINE_CHOICES = [
        ('indian',    'Indian'),
        ('italian',   'Italian'),
        ('seafood',   'Seafood'),
        ('continental', 'Continental'),
    ]

    name          = models.CharField(max_length=100)
    description   = models.TextField(blank=True)
    category      = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    cuisine       = models.CharField(max_length=20, choices=CUISINE_CHOICES)
    price         = models.DecimalField(max_digits=8, decimal_places=2)
    is_available  = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']


# ──────────────────────────────────────────
# MODEL 2: RestaurantTable
# ──────────────────────────────────────────
class RestaurantTable(models.Model):

    table_number  = models.PositiveIntegerField(unique=True)
    capacity      = models.PositiveIntegerField(default=4)
    is_occupied   = models.BooleanField(default=False)

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Table {self.table_number} ({status})"

    class Meta:
        ordering = ['table_number']


# ──────────────────────────────────────────
# MODEL 3: Order
# ──────────────────────────────────────────
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('preparing',  'Preparing'),
        ('served',     'Served'),
        ('paid',       'Paid'),
    ]

    table         = models.ForeignKey(
                        RestaurantTable,
                        on_delete=models.PROTECT,
                        related_name='orders'
                    )
    status        = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='pending'
                    )
    total_price   = models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        default=0.00
                    )
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} | Table {self.table.table_number} | {self.status}"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# MODEL 4: OrderItem
# ──────────────────────────────────────────
class OrderItem(models.Model):

    order         = models.ForeignKey(
                        Order,
                        on_delete=models.CASCADE,
                        related_name='items'
                    )
    menu_item     = models.ForeignKey(
                        MenuItem,
                        on_delete=models.PROTECT,
                        related_name='order_items'
                    )
    quantity      = models.PositiveIntegerField(default=1)
    unit_price    = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"

    class Meta:
        ordering = ['id']