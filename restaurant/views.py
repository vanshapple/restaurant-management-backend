# restaurant/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import MenuItem, RestaurantTable, Order, OrderItem
from .serializers import (
    MenuItemSerializer,
    RestaurantTableSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
    OrderStatusSerializer,
)


# ──────────────────────────────────────────
# MENU VIEWS
# ──────────────────────────────────────────

class MenuListView(APIView):
    """
    GET  /api/menu/  → list all available menu items
    POST /api/menu/  → create a new menu item
    """

    def get(self, request):
        items = MenuItem.objects.filter(is_available=True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailView(APIView):
    """
    PUT    /api/menu/<id>/  → update a menu item
    DELETE /api/menu/<id>/  → delete a menu item
    """

    def get_object(self, pk):
        return get_object_or_404(MenuItem, pk=pk)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(
            {"message": "Menu item deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


# ──────────────────────────────────────────
# TABLE VIEWS
# ──────────────────────────────────────────

class TableListView(APIView):
    """
    GET /api/tables/          → list all tables
    GET /api/tables/?available=true  → list only available tables
    """

    def get(self, request):
        available = request.query_params.get('available')

        if available == 'true':
            tables = RestaurantTable.objects.filter(is_occupied=False)
        else:
            tables = RestaurantTable.objects.all()

        serializer = RestaurantTableSerializer(tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ──────────────────────────────────────────
# ORDER VIEWS
# ──────────────────────────────────────────

class OrderListView(APIView):
    """
    GET  /api/orders/          → list all orders
    GET  /api/orders/?status=pending  → filter by status
    POST /api/orders/          → create a new order
    """

    def get(self, request):
        order_status = request.query_params.get('status')

        if order_status:
            orders = Order.objects.filter(status=order_status)
        else:
            orders = Order.objects.all()

        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        table     = validated['table']
        items     = validated['items']

        # ── Create the Order ──
        order = Order.objects.create(table=table)

        # ── Create each OrderItem and calculate total ──
        total = 0
        for item_data in items:
            menu_item = item_data['menu_item']
            quantity  = item_data['quantity']
            unit_price = menu_item.price

            OrderItem.objects.create(
                order      = order,
                menu_item  = menu_item,
                quantity   = quantity,
                unit_price = unit_price,
            )
            total += unit_price * quantity

        # ── Save total and mark table occupied ──
        order.total_price = total
        order.save()

        table.is_occupied = True
        table.save()

        response_serializer = OrderReadSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """
    GET /api/orders/<id>/  → retrieve one order
    PUT /api/orders/<id>/  → update order status
    """

    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderReadSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderStatusSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_status = serializer.validated_data['status']
        order.status = new_status
        order.save()

        # ── Free the table when order is paid ──
        if new_status == 'paid':
            order.table.is_occupied = False
            order.table.save()

        response_serializer = OrderReadSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_200_OK)