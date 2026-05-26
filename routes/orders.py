from flask import Blueprint, jsonify, request
from db import conn, cursor

orders_bp = Blueprint("orders", __name__)
@orders_bp.route("/orders")
def get_orders():

    cursor.execute("""
        SELECT
            orders.order_id,
            customers.email,
            products.product_name,
            orders.quantity,
            orders.order_status,
            orders.created_at
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.customer_id
        JOIN products
            ON orders.product_id = products.product_id
    """)
    rows = cursor.fetchall()

    orders = []

    for row in rows:

        order = {
            "order_id": row[0],
            "customer_email": row[1],
            "product_name": row[2],
            "quantity": row[3],
            "status": row[4],
            "created_at": row[5]
        }

        orders.append(order)

    return jsonify(orders)
@orders_bp.route("/create-order", methods=["POST"])
def create_order():
    data = request.json
    customer_id = data["customer_id"]
    product_id = data["product_id"]
    quantity = data["quantity"]
    cursor.execute(
        "SELECT stock_quantity FROM products WHERE product_id = %s",
        (product_id,)
    )
    stock = cursor.fetchone()
    if stock is None:
        return {"error": "Product not found"}, 404
    current_stock = stock[0]
    if current_stock < quantity:
        return {"error": "Insufficient stock"}, 400
    cursor.execute(
        """
        INSERT INTO orders
        (customer_id, product_id, quantity, order_status)
        VALUES (%s, %s, %s, 'placed')
        """,
        (customer_id, product_id, quantity)
    )
    cursor.execute(
        """
        UPDATE products
        SET stock_quantity = stock_quantity - %s
        WHERE product_id = %s
        """,
        (quantity, product_id)
    )
    conn.commit()
    return {"message": "Order created successfully"}
@orders_bp.route("/update-order/<int:order_id>", methods=["PUT"])
def update_order(order_id):

    data = request.json

    new_status = data["status"]

    cursor.execute(
        """
        UPDATE orders
        SET order_status = %s
        WHERE order_id = %s
        """,
        (new_status, order_id)
    )

    conn.commit()

    return {
        "message": "Order updated successfully"
    }
@orders_bp.route("/delete-order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):

    # Delete payments
    cursor.execute(
        """
        DELETE FROM payments
        WHERE order_id = %s
        """,
        (order_id,)
    )

    # Delete shipping
    cursor.execute(
        """
        DELETE FROM shipping
        WHERE order_id = %s
        """,
        (order_id,)
    )

    # Delete order
    cursor.execute(
        """
        DELETE FROM orders
        WHERE order_id = %s
        """,
        (order_id,)
    )

    conn.commit()

    return {
        "message": "Order deleted successfully"
    }