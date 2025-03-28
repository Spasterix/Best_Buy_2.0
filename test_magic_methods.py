#!/usr/bin/env python3
"""
Test module for magic methods and properties.
"""

import pytest
import products
import store


def test_product_magic_methods():
    """Test product magic methods and properties."""
    # Create test products
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)
    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = products.Product("Google Pixel 7", price=500, quantity=250)
    
    # Test string representation
    assert str(mac) == "MacBook Air M2, Price: $1450, Quantity: 100"
    
    # Test price comparison
    assert mac > bose  # 1450 > 250
    assert bose < mac  # 250 < 1450
    assert not (pixel > mac)  # 500 < 1450
    
    # Test price setter
    with pytest.raises(ValueError, match="Price cannot be negative"):
        mac.price = -100
        
    # Test invalid comparison
    assert mac.__gt__("invalid") == NotImplemented


def test_store_magic_methods():
    """Test store magic methods."""
    # Create test stores
    store1 = store.Store([
        products.Product("Product 1", price=100, quantity=10),
        products.Product("Product 2", price=200, quantity=20)
    ])
    
    store2 = store.Store([
        products.Product("Product 3", price=300, quantity=30),
        products.Product("Product 4", price=400, quantity=40)
    ])
    
    # Test product containment
    product1 = products.Product("Product 1", price=100, quantity=10)
    product3 = products.Product("Product 3", price=300, quantity=30)
    
    assert product1 in store1
    assert product3 not in store1
    assert product3 in store2
    
    # Test store combination
    combined_store = store1 + store2
    assert len(combined_store.products) == 4
    assert product1 in combined_store
    assert product3 in combined_store
    
    # Test invalid store combination
    assert combined_store.__add__("invalid") == NotImplemented


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 