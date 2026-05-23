# restaurant/urls.py

from django.urls import path
from .views import (
    MenuListView,
    MenuDetailView,
    TableListView,
    OrderListView,
    OrderDetailView,
)

urlpatterns = [
    # ── Menu endpoints ──────────────────────────
    path('menu/',        MenuListView.as_view(),   name='menu-list'),
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),

    # ── Table endpoints ──────────────────────────
    path('tables/',      TableListView.as_view(),  name='table-list'),

    # ── Order endpoints ──────────────────────────
    path('orders/',          OrderListView.as_view(),  name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]