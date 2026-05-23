# restaurant/management/commands/seed.py

from django.core.management.base import BaseCommand
from restaurant.models import MenuItem, RestaurantTable


class Command(BaseCommand):
    help = 'Seed the database with sample menu items and tables'

    def handle(self, *args, **kwargs):

        # ── Clear existing data ──
        MenuItem.objects.all().delete()
        RestaurantTable.objects.all().delete()
        self.stdout.write("Existing data cleared.")

        # ── Seed menu items ──
        menu_items = [
            {"name": "Butter Chicken",    "description": "Tender chicken in a rich creamy tomato curry sauce.",          "category": "main",     "cuisine": "indian",   "price": 320.00},
            {"name": "Paneer Tikka",      "description": "Marinated cottage cheese cubes grilled in a tandoor oven.",    "category": "starter",  "cuisine": "indian",   "price": 240.00},
            {"name": "Dal Makhani",       "description": "Slow-cooked black lentils with butter and cream.",             "category": "main",     "cuisine": "indian",   "price": 220.00},
            {"name": "Gulab Jamun",       "description": "Soft milk dumplings soaked in rose-flavored sugar syrup.",     "category": "dessert",  "cuisine": "indian",   "price": 120.00},
            {"name": "Mango Lassi",       "description": "Chilled yogurt drink blended with fresh Alphonso mango.",      "category": "beverage", "cuisine": "indian",   "price": 100.00},
            {"name": "Margherita Pizza",  "description": "Classic pizza with tomato, fresh mozzarella and basil.",       "category": "main",     "cuisine": "italian",  "price": 380.00},
            {"name": "Fettuccine Alfredo","description": "Flat egg pasta in a silky Parmesan butter cream sauce.",       "category": "main",     "cuisine": "italian",  "price": 340.00},
            {"name": "Bruschetta",        "description": "Toasted sourdough with garlic, fresh tomato and basil.",       "category": "starter",  "cuisine": "italian",  "price": 180.00},
            {"name": "Tiramisu",          "description": "Espresso-soaked ladyfingers with mascarpone cream.",           "category": "dessert",  "cuisine": "italian",  "price": 220.00},
            {"name": "Grilled Salmon",    "description": "Atlantic salmon grilled with lemon butter and fresh dill.",    "category": "main",     "cuisine": "seafood",  "price": 520.00},
            {"name": "Fish and Chips",    "description": "Beer-battered cod fillet with thick-cut fries and tartar.",    "category": "main",     "cuisine": "seafood",  "price": 420.00},
            {"name": "Prawn Cocktail",    "description": "Chilled tiger prawns with lettuce and Marie Rose sauce.",      "category": "starter",  "cuisine": "seafood",  "price": 280.00},
        ]

        for item in menu_items:
            MenuItem.objects.create(**item)
        self.stdout.write(f"{len(menu_items)} menu items seeded.")

        # ── Seed tables ──
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

        for table in tables:
            RestaurantTable.objects.create(**table)
        self.stdout.write(f"{len(tables)} tables seeded.")

        self.stdout.write(self.style.SUCCESS("\nDatabase seeded successfully."))