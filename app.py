from flask import Flask, jsonify, request
from db import conn, cursor

app = Flask(__name__)

@app.route("/")
def home():
    return "Ecommerce API Running"

@app.route("/products")
def get_products():
    cursor.execute("SELECT * FROM products")
    
    columns = [desc[0] for desc in cursor.description]
    products = []

    for row in cursor.fetchall():
        products.append(dict(zip(columns, row)))

    return jsonify(products)
@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.json

    if not data:
        return {"error": "No data provided"}, 400

    customer_id = data.get("customer_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not customer_id or not product_id or not quantity:
        return {"error": "Missing required fields"}, 400

    cursor.execute(
        """
        INSERT INTO orders (customer_id, product_id, quantity, order_status)
        VALUES (%s,%s,%s,'placed')
        """,
        (customer_id, product_id, quantity)
    )

    conn.commit()

    return {"message": "Order created successfully"}
if __name__ == "__main__":
    app.run(debug=True)