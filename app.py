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
if __name__ == "__main__":
    app.run(debug=True)