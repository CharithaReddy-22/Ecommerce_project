from flask import Blueprint, jsonify, request
from db import conn, cursor
from routes.auth import token_required
orders_bp = Blueprint("orders", __name__)
@orders_bp.route("/orders")
@token_required
def get_orders(current_user):

    cursor.execute("""
    SELECT
        orders.order_id,
        users.email,
        products.product_name,
        orders.quantity,
        orders.order_status,
        orders.created_at
    FROM orders
    JOIN users
        ON orders.user_id = users.user_id
    JOIN products
        ON orders.product_id = products.product_id
    WHERE orders.user_id = %s""",
    (current_user["user_id"],))
    rows = cursor.fetchall()

    orders = []

    for row in rows:

        order = {
            "order_id": row[0],
            "user_email": row[1],
            "product_name": row[2],
            "quantity": row[3],
            "status": row[4],
            "created_at": row[5]
        }

        orders.append(order)

    return jsonify(orders)
@orders_bp.route("/create-order", methods=["POST"])
@token_required
def create_order(current_user):
    data = request.json
    user_id = current_user["user_id"]
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
    (user_id, product_id, quantity, order_status)
    VALUES (%s, %s, %s, 'placed')
    """,
    (user_id, product_id, quantity)
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
@token_required
def update_order(current_user,order_id):

    data = request.json

    new_status = data["status"]
    cursor.execute(
    """
    SELECT *
    FROM orders
    WHERE order_id = %s
    AND user_id = %s
    """,
    (order_id, current_user["user_id"])
    )
    order = cursor.fetchone()

    if order is None:
        return {"error": "Unauthorized"}, 403
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
@token_required
def delete_order(current_user,order_id):
    cursor.execute(
    """
    SELECT *
    FROM orders
    WHERE order_id = %s
    AND user_id = %s
    """,
    (order_id, current_user["user_id"])
    )

    order = cursor.fetchone()

    if order is None:
        return {"error": "Unauthorized"}, 403
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
