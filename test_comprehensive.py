#!/usr/bin/env python3
"""
Comprehensive test module for testing all functionality of the store system.
"""

import pytest
import products
import promotions
import store


def test_product_creation():
    """Test basic product creation and properties."""
    # Test normal product
    product = products.Product("Test Product", price=100, quantity=10)
    assert product.name == "Test Product"
    assert product.price == 100
    assert product.quantity == 10
    assert product.active is True
    
    # Test invalid product creation
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        products.Product("", price=100, quantity=10)
    with pytest.raises(ValueError, match="Price cannot be negative"):
        products.Product("Test", price=-100, quantity=10)
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        products.Product("Test", price=100, quantity=-10)


def test_product_operations():
    """Test product operations like quantity changes and activation."""
    product = products.Product("Test", price=100, quantity=10)
    
    # Test quantity changes
    product.quantity = 5
    assert product.quantity == 5
    assert product.active is True
    
    product.quantity = 0
    assert product.quantity == 0
    assert product.active is False
    
    # Test manual activation/deactivation
    product.activate()
    assert product.active is True
    product.deactivate()
    assert product.active is False


def test_non_stocked_product():
    """Test non-stocked product functionality."""
    product = products.NonStockedProduct("Digital Product", price=100)
    
    # Test properties
    assert product.quantity == 0
    assert product.active is True
    
    # Test quantity changes (should be ignored)
    product.quantity = 10
    assert product.quantity == 0
    
    # Test purchases
    assert product.buy(2) == 200  # 2 * 100
    assert product.quantity == 0  # Should remain 0
    
    # Test display
    assert "(Digital)" in product.show()


def test_limited_product():
    """Test limited product functionality."""
    product = products.LimitedProduct("Limited", price=100, quantity=10, maximum=2)
    
    # Test properties
    assert product.maximum == 2
    assert product.quantity == 10
    
    # Test valid purchase
    assert product.buy(2) == 200  # 2 * 100
    
    # Test exceeding maximum
    with pytest.raises(ValueError, match="Cannot purchase more than 2 units in one order"):
        product.buy(3)
    
    # Test invalid maximum
    with pytest.raises(ValueError, match="Maximum purchase quantity must be positive"):
        products.LimitedProduct("Invalid", price=100, quantity=10, maximum=0)


def test_promotions():
    """Test all promotion types."""
    product = products.Product("Test", price=100, quantity=10)
    
    # Test percent discount
    percent_promo = promotions.PercentDiscount("20% off", percent=20)
    product.set_promotion(percent_promo)
    assert product.buy(2) == 160  # 200 * 0.8
    product.quantity = 10  # Reset quantity
    
    # Test second half price
    half_price_promo = promotions.SecondHalfPrice("Second Half Price!")
    product.set_promotion(half_price_promo)
    assert product.buy(2) == 150  # 100 + 50
    product.quantity = 10  # Reset quantity
    assert product.buy(3) == 250  # 100 + 50 + 100
    product.quantity = 10  # Reset quantity
    
    # Test third one free
    third_free_promo = promotions.ThirdOneFree("Third One Free!")
    product.set_promotion(third_free_promo)
    assert product.buy(3) == 200  # 100 * 2
    product.quantity = 10  # Reset quantity
    assert product.buy(6) == 400  # 100 * 4
    
    # Test invalid percent discount
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
        promotions.PercentDiscount("Invalid", percent=150)


def test_store_operations():
    """Test store operations."""
    # Create products
    product1 = products.Product("Product 1", price=100, quantity=10)
    product2 = products.NonStockedProduct("Product 2", price=200)
    product3 = products.LimitedProduct("Product 3", price=300, quantity=10, maximum=2)
    
    # Create store
    store_instance = store.Store([product1, product2, product3])
    
    # Test adding products
    new_product = products.Product("New Product", price=400, quantity=10)
    store_instance.add_product(new_product)
    assert new_product in store_instance.products
    
    # Test removing products
    store_instance.remove_product(new_product)
    assert new_product not in store_instance.products
    
    # Test getting total quantity
    assert store_instance.get_total_quantity() == 20  # 10 + 0 + 10
    
    # Test getting active products
    active_products = store_instance.get_all_products()
    assert len(active_products) == 3  # All products are active (including non-stocked)
    
    # Test ordering
    order = [(product1, 2), (product2, 2), (product3, 1)]
    total_price = store_instance.order(order)
    assert total_price == 900  # (100 * 2) + (200 * 2) + (300 * 1)
    
    # Reset quantities for next test
    product1.quantity = 10
    product3.quantity = 10


def test_store_with_promotions():
    """Test store operations with promotions."""
    # Create products with promotions
    product1 = products.Product("Product 1", price=100, quantity=10)
    product1.set_promotion(promotions.PercentDiscount("20% off", percent=20))
    
    product2 = products.Product("Product 2", price=200, quantity=10)
    product2.set_promotion(promotions.SecondHalfPrice("Second Half Price!"))
    
    product3 = products.Product("Product 3", price=300, quantity=10)
    product3.set_promotion(promotions.ThirdOneFree("Third One Free!"))
    
    # Create store
    store_instance = store.Store([product1, product2, product3])
    
    # Test order with promotions
    order = [(product1, 2), (product2, 2), (product3, 3)]
    total_price = store_instance.order(order)
    
    # Calculate expected price:
    # Product 1: 200 * 0.8 = 160
    # Product 2: 200 + 100 = 300
    # Product 3: 300 * 2 = 600
    assert total_price == 1060


def test_error_handling():
    """Test error handling in various scenarios."""
    # Test invalid product in store order
    store_instance = store.Store()
    invalid_product = products.Product("Invalid", price=100, quantity=10)
    order = [(invalid_product, 1)]
    with pytest.raises(ValueError, match="Product not available in this store"):
        store_instance.order(order)
    
    # Test inactive product purchase
    product = products.Product("Test", price=100, quantity=0)
    with pytest.raises(RuntimeError, match="Product is not active"):
        product.buy(1)
    
    # Test negative quantity purchase
    product = products.Product("Test", price=100, quantity=10)
    with pytest.raises(ValueError, match="Purchase quantity must be positive"):
        product.buy(-1)
    
    # Test exceeding available quantity
    with pytest.raises(ValueError, match="Not enough products available"):
        product.buy(20)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 