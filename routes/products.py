
from flask import Blueprint, jsonify
from db import cursor

products_bp = Blueprint("products", __name__)
@products_bp.route("/products")
def get_products():
    cursor.execute("SELECT * FROM products")
    
    columns = [desc[0] for desc in cursor.description]
    products = []

    for row in cursor.fetchall():
        products.append(dict(zip(columns, row)))

    return jsonify(products)