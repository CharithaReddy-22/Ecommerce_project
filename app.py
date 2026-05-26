from flask import Flask, jsonify, request
from db import cursor
from routes.orders import orders_bp
from routes.products import products_bp
app = Flask(__name__)
app.register_blueprint(orders_bp)
app.register_blueprint(products_bp)
@app.route("/")
def home():
    return "Ecommerce API Running"
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)