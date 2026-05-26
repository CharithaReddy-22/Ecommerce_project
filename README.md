# Ecommerce Backend API

A backend ecommerce API project built using Flask and PostgreSQL.

## Features

- Product APIs
- Order Management
- CRUD Operations
- PostgreSQL Database Integration
- REST APIs
- Inventory Management
- Modular Flask Blueprint Structure

## Technologies Used

- Python
- Flask
- PostgreSQL
- Supabase
- psycopg2
- Git & GitHub

## API Endpoints

### Products
GET /products

### Orders
GET /orders

POST /create-order

PUT /update-order/<order_id>

DELETE /delete-order/<order_id>

## Project Structure

Ecommerce Project/
│
├── app.py
├── db.py
├── routes/
│ ├── orders.py
│ └── products.py
│
├── requirements.txt
└── README.md

## Run Project

pip install -r requirements.txt

python app.py