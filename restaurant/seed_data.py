# restaurant/seed_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_backend.settings')
django.setup()

from restaurant.models import MenuItem, RestaurantTable


# ──────────────────────────────────────────
# CLEAR EXISTING DATA
# ──────────────────────────────────────────
def clear_data():
    MenuItem.objects.all().delete()
    RestaurantTable.objects.all().delete()
    print("Existing data cleared.")


# ──────────────────────────────────────────
# SEED MENU ITEMS
# ──────────────────────────────────────────
def seed_menu_items():
    menu_items = [

        # ── Indian ──────────────────────────────
        {
            "name":        "Butter Chicken",
            "description": "Tender chicken in a rich, creamy tomato-based curry sauce.",
            "category":    "main",
            "cuisine":     "indian",
            "price":       320.00,
            "is_available": True,
        },
        {
            "name":        "Paneer Tikka",
            "description": "Marinated cottage cheese cubes grilled in a tandoor oven.",
            "category":    "starter",
            "cuisine":     "indian",
            "price":       240.00,
            "is_available": True,
        },
        {
            "name":        "Dal Makhani",
            "description": "Slow-cooked black lentils simmered overnight with butter and cream.",
            "category":    "main",
            "cuisine":     "indian",
            "price":       220.00,
            "is_available": True,
        },
        {
            "name":        "Gulab Jamun",
            "description": "Soft milk-solid dumplings soaked in rose-flavored sugar syrup.",
            "category":    "dessert",
            "cuisine":     "indian",
            "price":       120.00,
            "is_available": True,
        },
        {
            "name":        "Mango Lassi",
            "description": "Chilled yogurt-based drink blended with fresh Alphonso mango.",
            "category":    "beverage",
            "cuisine":     "indian",
            "price":       100.00,
            "is_available": True,
        },

        # ── Italian ─────────────────────────────
        {
            "name":        "Margherita Pizza",
            "description": "Classic Neapolitan pizza with San Marzano tomato, fresh mozzarella and basil.",
            "category":    "main",
            "cuisine":     "italian",
            "price":       380.00,
            "is_available": True,
        },
        {
            "name":        "Fettuccine Alfredo",
            "description": "Flat egg pasta tossed in a silky Parmesan and butter cream sauce.",
            "category":    "main",
            "cuisine":     "italian",
            "price":       340.00,
            "is_available": True,
        },
        {
            "name":        "Bruschetta",
            "description": "Toasted sourdough rubbed with garlic, topped with fresh tomato and basil.",
            "category":    "starter",
            "cuisine":     "italian",
            "price":       180.00,
            "is_available": True,
        },
        {
            "name":        "Tiramisu",
            "description": "Classic Italian dessert with espresso-soaked ladyfingers and mascarpone cream.",
            "category":    "dessert",
            "cuisine":     "italian",
            "price":       220.00,
            "is_available": True,
        },

        # ── Seafood ─────────────────────────────
        {
            "name":        "Grilled Salmon",
            "description": "Atlantic salmon fillet grilled with lemon butter, capers and fresh dill.",
            "category":    "main",
            "cuisine":     "seafood",
            "price":       520.00,
            "is_available": True,
        },
        {
            "name":        "Fish and Chips",
            "description": "Beer-battered cod fillet served with thick-cut fries and tartar sauce.",
            "category":    "main",
            "cuisine":     "seafood",
            "price":       420.00,
            "is_available": True,
        },
        {
            "name":        "Prawn Cocktail",
            "description": "Chilled tiger prawns on a bed of lettuce with Marie Rose sauce.",
            "category":    "starter",
            "cuisine":     "seafood",
            "price":       280.00,
            "is_available": True,
        },
    ]

    for item_data in menu_items:
        MenuItem.objects.create(**item_data)

    print(f"{len(menu_items)} menu items seeded successfully.")


# ──────────────────────────────────────────
# SEED RESTAURANT TABLES
# ──────────────────────────────────────────
def seed_tables():
    tables = [
        {"table_number": 1, "capacity": 2},
        {"table_number": 2, "capacity": 2},
        {"table_number": 3, "capacity": 4},
        {"table_number": 4, "capacity": 4},
        {"table_number": 5, "capacity": 4},
        {"table_number": 6, "capacity": 6},
        {"table_number": 7, "capacity": 6},
        {"table_number": 8, "capacity": 8},
    ]

    for table_data in tables:
        RestaurantTable.objects.create(**table_data)

    print(f"{len(tables)} tables seeded successfully.")


# ──────────────────────────────────────────
# RUN
# ──────────────────────────────────────────
if __name__ == '__main__':
    print("Seeding database...")
    clear_data()
    seed_menu_items()
    seed_tables()
    print("\nDone. Database is ready.")