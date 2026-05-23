# 🍽️ Restaurant Management System — Backend API

A production-style REST API backend built with **Django** and **Django REST Framework** for managing restaurant operations including menu items, tables, and orders.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5 |
| API Layer | Django REST Framework |
| Database | SQLite |
| Testing | Postman |

---

## 📁 Project Structure

```
restaurant-management-backend/
├── restaurant_backend/        ← Project config (settings, root URLs)
├── restaurant/                ← Main app
│   ├── management/commands/   ← Custom management commands
│   │   └── seed.py            ← Database seeder
│   ├── migrations/            ← Database migrations
│   ├── models.py              ← Database models
│   ├── serializers.py         ← Request/response serializers
│   ├── views.py               ← API views
│   ├── urls.py                ← App-level URL routing
│   └── admin.py               ← Admin panel config
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/vanshapple/restaurant-management-backend.git
cd restaurant-management-backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed sample data
```bash
python manage.py seed
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```

API is now live at `http://127.0.0.1:8000/`

---

## 📌 API Endpoints

### Menu

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/menu/` | List all available menu items |
| POST | `/api/menu/` | Create a new menu item |
| PUT | `/api/menu/<id>/` | Update a menu item |
| DELETE | `/api/menu/<id>/` | Delete a menu item |

### Tables

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tables/` | List all tables |
| GET | `/api/tables/?available=true` | List available tables only |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/orders/` | Create a new order |
| GET | `/api/orders/` | List all orders |
| GET | `/api/orders/?status=pending` | Filter orders by status |
| GET | `/api/orders/<id>/` | Retrieve a single order |
| PUT | `/api/orders/<id>/` | Update order status |

---

## 📦 Example Requests

### Create Order
```json
POST /api/orders/
{
    "table": 1,
    "items": [
        {"menu_item": 1, "quantity": 2},
        {"menu_item": 6, "quantity": 1}
    ]
}
```

### Update Order Status
```json
PUT /api/orders/1/
{
    "status": "preparing"
}
```

Valid status values: `pending` → `preparing` → `served` → `paid`

---

## 🗄️ Database Models

```
MenuItem
  id, name, description, category, cuisine,
  price, is_available, created_at, updated_at

RestaurantTable
  id, table_number, capacity, is_occupied

Order
  id, table (FK), status, total_price,
  created_at, updated_at

OrderItem
  id, order (FK), menu_item (FK),
  quantity, unit_price
```

---

## ✅ Business Logic

- Total order price is **automatically calculated** from item quantities and prices
- Table is marked **occupied** when an order is created
- Table is marked **available** when order status is set to `paid`
- Menu item price is **snapshotted** at time of ordering — future price changes don't affect past orders
- Unavailable menu items **cannot be ordered**
- An occupied table **cannot receive a new order**

---

## 🌱 Sample Data

Run `python manage.py seed` to load:

- **12 menu items** across Indian, Italian, and Seafood cuisines
- **8 restaurant tables** with varying capacities (2 to 8 seats)

---

## 👤 Admin Panel

Visit `http://127.0.0.1:8000/admin/` after creating a superuser.

Features:
- Manage menu items with inline price editing
- View all orders with nested order items
- Monitor table availability
- Filter and search across all models

---

## 👨‍💻 Author

**Vansh K Bhanushali**
Backend Developer Intern Candidate
[GitHub](https://github.com/vanshapple) 
[LinkedIn](https://linkedin.com/in/vanshbhanushali)
