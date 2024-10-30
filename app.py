from flask import Flask, request, jsonify
from models import db, Product
from config import config_by_name

app = Flask(__name__)

# Configuring database
app.config.from_object(config_by_name['development'])  # Use 'development', 'testing', or 'production' as needed
db.init_app(app)

# Initialize the database
def setup_database():
    db.create_all()

# Routes
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the API! Use /products to interact with the Product endpoints."
    }), 200

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify(product.to_dict()), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204

if __name__ == '__main__':
    with app.app_context():  # Use application context
        setup_database()     # Initialize the database
    app.run(debug=True)