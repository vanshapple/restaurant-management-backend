# restaurant/serializers.py

from rest_framework import serializers
from .models import MenuItem, RestaurantTable, Order, OrderItem


# ──────────────────────────────────────────
# SERIALIZER 1: MenuItem
# ──────────────────────────────────────────
class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model  = MenuItem
        fields = [
            'id', 'name', 'description', 'category',
            'cuisine', 'price', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# ──────────────────────────────────────────
# SERIALIZER 2: RestaurantTable
# ──────────────────────────────────────────
class RestaurantTableSerializer(serializers.ModelSerializer):

    class Meta:
        model  = RestaurantTable
        fields = ['id', 'table_number', 'capacity', 'is_occupied']
        read_only_fields = ['id', 'is_occupied']


# ──────────────────────────────────────────
# SERIALIZER 3: OrderItem — for reading (nested inside Order response)
# ──────────────────────────────────────────
class OrderItemReadSerializer(serializers.ModelSerializer):

    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model  = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'unit_price']
        read_only_fields = ['id', 'unit_price', 'menu_item_name']


# ──────────────────────────────────────────
# SERIALIZER 4: OrderItem — for writing (accepts input when creating order)
# ──────────────────────────────────────────
class OrderItemWriteSerializer(serializers.Serializer):

    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.filter(is_available=True)
    )
    quantity = serializers.IntegerField(min_value=1)


# ──────────────────────────────────────────
# SERIALIZER 5: Order — for reading (full detail response)
# ──────────────────────────────────────────
class OrderReadSerializer(serializers.ModelSerializer):

    items       = OrderItemReadSerializer(many=True, read_only=True)
    table_number = serializers.IntegerField(source='table.table_number', read_only=True)

    class Meta:
        model  = Order
        fields = [
            'id', 'table', 'table_number', 'status',
            'total_price', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


# ──────────────────────────────────────────
# SERIALIZER 6: Order — for writing (accepts input when creating order)
# ──────────────────────────────────────────
class OrderWriteSerializer(serializers.Serializer):

    table = serializers.PrimaryKeyRelatedField(
        queryset=RestaurantTable.objects.all()
    )
    items = OrderItemWriteSerializer(many=True)

    def validate_table(self, value):
        if value.is_occupied:
            raise serializers.ValidationError(
                f"Table {value.table_number} is already occupied."
            )
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("An order must have at least one item.")
        return value


# ──────────────────────────────────────────
# SERIALIZER 7: Order status update only
# ──────────────────────────────────────────
class OrderStatusSerializer(serializers.Serializer):

    STATUS_CHOICES = ['pending', 'preparing', 'served', 'paid']

    status = serializers.ChoiceField(choices=STATUS_CHOICES)