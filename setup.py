from products.models import Product

product_list = [
    {"name": "Keyboard", "price": 500, "available_quantity": 100},
    {"name": "Mouse", "price": 250, "available_quantity": 200},
    {"name": "Speaker", "price": 6000, "available_quantity": 8},
    {"name": "Filter", "price": 3200, "available_quantity": 7},
    {"name": "Cycle", "price": 5500, "available_quantity": 22},
    {"name": "Bed", "price": 15000, "available_quantity": 13},
    {"name": "Table", "price": 2000, "available_quantity": 12},
    {"name": "Mobile Phone", "price": 12000, "available_quantity": 100},
    {"name": "Laptop", "price": 60000, "available_quantity": 30},
    {"name": "AC", "price": 25000, "available_quantity": 5},
    {"name": "TV", "price": 10000, "available_quantity": 15},
    {"name": "Refrigerator", "price": 20000, "available_quantity": 10}
]


def populate_products():
    for product in product_list:
        Product.objects.create(
            name=product.get('name'),
            price=product.get('price'),
            available_quantity=product.get('available_quantity')
        )
