import requests

BASE_URL = "http://127.0.0.1:5000"

# Helper function to create a product for testing
def create_test_product():
    response = requests.post(f"{BASE_URL}/products", json={
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99
    })
    return response.json()["id"]

# Helper function to delete a product after testing
def delete_test_product(product_id):
    requests.delete(f"{BASE_URL}/products/{product_id}")

def test_add_product():
    """Test adding a new product."""
    product_id = create_test_product()
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    delete_test_product(product_id)

def test_get_products():
    """Test retrieving all products."""
    product_id = create_test_product()
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    delete_test_product(product_id)

def test_get_product_by_id():
    """Test retrieving a product by ID."""
    product_id = create_test_product()
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "price" in data
    delete_test_product(product_id)

def test_update_product():
    """Test updating an existing product."""
    product_id = create_test_product()
    response = requests.put(f"{BASE_URL}/products/{product_id}", json={
        "name": "Updated Product",
        "price": 120.00
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 120.00
    delete_test_product(product_id)

def test_delete_product():
    """Test deleting a product."""
    product_id = create_test_product()
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 204
