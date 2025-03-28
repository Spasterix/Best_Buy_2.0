
"""
Test module for the Product class.
"""

import pytest
from products import Product


def test_create_valid_product():
    """Test creating a product with valid parameters."""
    product = Product("Test Product", price=100, quantity=10)
    assert product.name == "Test Product"
    assert product.price == 100
    assert product.quantity == 10
    assert product.active is True


def test_create_product_empty_name():
    """Test creating a product with empty name raises ValueError."""
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("", price=100, quantity=10)


def test_create_product_negative_price():
    """Test creating a product with negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("Test Product", price=-100, quantity=10)


def test_create_product_negative_quantity():
    """Test creating a product with negative quantity raises ValueError."""
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("Test Product", price=100, quantity=-10)


def test_product_becomes_inactive_at_zero_quantity():
    """Test that product becomes inactive when quantity reaches zero."""
    product = Product("Test Product", price=100, quantity=5)
    product.quantity = 0
    assert product.active is False
    assert product.quantity == 0


def test_product_reactivates_when_quantity_increases():
    """Test that product becomes active again when quantity increases."""
    product = Product("Test Product", price=100, quantity=0)
    assert product.active is False
    product.quantity = 5
    assert product.quantity == 5
    assert product.active is True


def test_product_purchase_modifies_quantity():
    """Test that product purchase correctly modifies quantity and returns price."""
    product = Product("Test Product", price=100, quantity=5)
    total_price = product.buy(2)
    assert product.quantity == 3
    assert total_price == 200
    assert product.active is True


def test_product_purchase_exceeds_quantity():
    """Test that buying more than available quantity raises ValueError."""
    product = Product("Test Product", price=100, quantity=5)
    with pytest.raises(ValueError, match="Not enough products available"):
        product.buy(6)
    assert product.quantity == 5  # Verify quantity remains unchanged


def test_product_purchase_inactive_product():
    """Test that buying from inactive product raises RuntimeError."""
    product = Product("Test Product", price=100, quantity=0)
    # Stelle sicher, dass das Produkt wirklich inaktiv ist
    product.deactivate()
    with pytest.raises(RuntimeError, match="Product is not active"):
        product.buy(1)
    assert product.quantity == 0  # Verify quantity remains unchanged


def test_product_purchase_negative_quantity():
    """Test that buying negative quantity raises ValueError."""
    product = Product("Test Product", price=100, quantity=5)
    with pytest.raises(ValueError, match="Purchase quantity must be positive"):
        product.buy(-1)
    assert product.quantity == 5  # Verify quantity remains unchanged


def test_product_show_method():
    """Test the string representation of a product."""
    product = Product("Test Product", price=100, quantity=5)
    expected = "Test Product, Price: 100, Quantity: 5"
    assert product.show() == expected


def test_product_set_quantity_validation():
    """Test that setting quantity validates input."""
    product = Product("Test Product", price=100, quantity=5)
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        product.quantity = -1
    assert product.quantity == 5  # Verify quantity remains unchanged


def test_product_manual_activation():
    """Test manual activation and deactivation of products."""
    product = Product("Test Product", price=100, quantity=5)
    assert product.active is True

    product.deactivate()
    assert product.active is False

    product.activate()
    assert product.active is True


def main():
    """Main function to run tests directly."""
    pytest.main([__file__, "-v"])  # Added verbose flag for better output


if __name__ == "__main__":
    main() 