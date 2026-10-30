# KAARI STORE ™ — Signature Streetwear & Embroidered Caps

An e-commerce storefront built with **Django**, **HTMX**, **Tailwind CSS (CDN)**, and **Swiper.js** for the KAARI streetwear brand. Features product catalog, category filtering, an HTMX-powered slide-over cart drawer, full checkout with Cash-on-Delivery ordering, and a responsive mobile-first design with a brutalist aesthetic.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.1 (Python 3.12+) |
| Frontend | Tailwind CSS v3 (CDN), HTMX 1.9, Swiper.js 11 |
| Database | SQLite (development) |
| Image Processing | Pillow |
| Fonts | Google Fonts (Inter, Syne) |

---

## Project Structure

```
Kaari--store/
├── kaari_store/          # Django project settings & root URL config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                # Product catalog app
│   ├── models.py         # Category, Product, ProductImage
│   ├── views.py          # product_list, product_detail
│   ├── urls.py
│   ├── admin.py
│   └── context_processors.py  # Global categories context
│
├── cart/                 # Cart & checkout app
│   ├── cart.py           # Session-based Cart class (shipping logic)
│   ├── models.py         # Order, OrderItem
│   ├── views.py          # cart_detail, cart_add, cart_remove, checkout
│   ├── urls.py
│   ├── admin.py          # Order admin with inline items
│   ├── context_processors.py  # Global cart context
│   └── tests.py          # Automated test suite
│
├── templates/
│   ├── base.html                       # Base layout (nav, footer, mobile drawer)
│   ├── store/
│   │   ├── product_list.html           # Home / product grid with Swiper hero
│   │   └── product_detail.html         # Product page with gallery & thumbnails
│   └── cart/
│       ├── cart_detail.html            # Full cart page
│       ├── checkout.html               # Checkout form (COD)
│       ├── order_success.html          # Order confirmation
│       └── partials/
│           └── cart_drawer.html        # HTMX slide-over cart drawer
│
├── static/
│   └── images/
│       ├── logo.png                    # Brand logo
│       └── banners/                    # Hero slider banners
│
├── media/                # User-uploaded product images (gitignored)
├── requirements.txt
├── manage.py
└── README.md
```

---

## Features

- **Product Catalog** — Browse all products or filter by category
- **Product Detail** — Image gallery with thumbnail switcher, related products
- **Hero Slider** — Swiper.js banner carousel with auto-play
- **HTMX Cart Drawer** — Slide-over cart from any page, live quantity +/− controls, no full reload
- **Session Cart** — Server-side cart stored in Django sessions
- **Checkout (COD)** — Shipping form with order saved to database
- **Order Management** — Django admin panel with Order + OrderItem inline
- **Standard Shipping** — Flat PKR 250 shipping added to every order
- **Responsive Design** — Mobile hamburger menu drawer, touch-friendly cart, fluid grid
- **Brutalist Aesthetic** — Bold borders, sharp shadows, uppercase typography

---

## Setup & Installation

### Prerequisites

- **Python 3.12+** installed
- **pip** package manager
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/khanu24/Kaari--store.git
cd Kaari--store
```

### 2. Create & Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set your username, email, and password.

### 6. Run Development Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## URLs Reference

| URL | Description |
|---|---|
| `/` | Home — product listing with hero slider |
| `/category/<slug>/` | Products filtered by category |
| `/product/<slug>/` | Product detail page |
| `/cart/` | Full cart page |
| `/cart/add/<id>/` | Add product to cart (POST) |
| `/cart/remove/<id>/` | Remove product from cart (POST) |
| `/cart/checkout/` | Checkout form & order placement |
| `/admin/` | Django admin panel |

---

## Adding Products

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Create a **Category** first (e.g., "Caps", "Accessories")
4. Then add **Products** — fill in name, slug, price, description, main image
5. Use the **Product Image inline** to add multiple gallery angles per product

---

## Running Tests

```bash
python manage.py test
```

This runs the automated test suite covering:
- Cart add/remove via HTMX
- Categories context processor on all pages
- Checkout order creation with shipping calculation
- Cart clearing after successful order

---

## Environment Notes

- **SECRET_KEY**: Currently hardcoded for development. For production, move it to an environment variable.
- **DEBUG**: Set to `True`. Set to `False` for production and configure `ALLOWED_HOSTS`.
- **Database**: Uses SQLite by default. Switch to PostgreSQL for production.
- **Static/Media**: Served by Django in development. Use a CDN or web server (Nginx) in production.
- **Tailwind/HTMX/Swiper**: Loaded via CDN — no build step required.

---

## License

This project is proprietary to KAARI STORE. All rights reserved.
