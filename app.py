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
    customer_id = data["customer_id"]
    product_id = data["product_id"]
    quantity = data["quantity"]

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