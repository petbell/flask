from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

db_params = {
    'dbname': 'product_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}


@app.route('/')
def index():
    return jsonify("Welcome to Products API!")

@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        return jsonify(products),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/products/<int:product_id>', methods=['GET'])
def get_a_product(product_id):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/products', methods=['POST'])
def add_product():
    try:
        new_product = request.get_json()
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        query = "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id"
        cursor.execute(query, (new_product['name'], new_product['price']))
        product_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return jsonify({"id": product_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')