#!/usr/bin/env python3
"""
Test module for testing promotions implementation in main.py
"""

import pytest
import products
import promotions
import store


def reset_product_quantities(product_list: list) -> None:
    """
    Reset quantities of all products to their initial values.
    
    Args:
        product_list: List of products to reset
    """
    for product in product_list:
        if isinstance(product, products.Product):
            if isinstance(product, products.NonStockedProduct):
                continue  # Skip non-stocked products
            product.quantity = 100  # Reset to initial quantity


def test_promotions_implementation():
    """Test the implementation of promotions in the store system."""
    # Setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    
    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)
    
    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)
    
    # Test 1: Verify promotions are correctly set
    assert product_list[0].promotion == second_half_price
    assert product_list[1].promotion == third_one_free
    assert product_list[3].promotion == thirty_percent
    assert product_list[2].promotion is None
    assert product_list[4].promotion is None
    
    # Test 2: Verify promotion display in show()
    assert "[Second Half price!]" in product_list[0].show()
    assert "[Third One Free!]" in product_list[1].show()
    assert "[30% off!]" in product_list[3].show()
    
    # Test 3: Test price calculations with promotions
    # MacBook Air M2 with second half price
    assert product_list[0].buy(2) == 2175.0  # 1450 + 725
    reset_product_quantities(product_list)
    assert product_list[0].buy(3) == 3625.0  # 1450 + 725 + 1450
    reset_product_quantities(product_list)
    
    # Bose Earbuds with third one free
    assert product_list[1].buy(3) == 500.0  # 250 * 2
    reset_product_quantities(product_list)
    assert product_list[1].buy(6) == 1000.0  # 250 * 4
    reset_product_quantities(product_list)
    
    # Windows License with 30% off
    assert product_list[3].buy(2) == 175.0  # 125 * 2 * 0.7
    
    # Test 4: Test limited product with promotion
    shipping = product_list[4]
    shipping.set_promotion(thirty_percent)
    assert shipping.buy(1) == 7.0  # 10 * 0.7
    reset_product_quantities(product_list)
    
    # Test 5: Test removing promotions
    product_list[0].set_promotion(None)
    assert product_list[0].promotion is None
    assert "[Second Half price!]" not in product_list[0].show()
    
    # Test 6: Test store order with promotions
    best_buy = store.Store(product_list)
    order = [(product_list[0], 2), (product_list[1], 3)]
    total_price = best_buy.order(order)
    assert total_price == 3400.0  # (1450 * 2) + (250 * 2)  # MacBook ohne Promotion + Bose mit Third One Free
    reset_product_quantities(product_list)


def test_promotion_validation():
    """Test validation of promotions."""
    # Test invalid percentage discount
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
        promotions.PercentDiscount("Invalid", percent=150)
    
    # Test invalid product quantity
    product = products.Product("Test", price=100, quantity=5)
    product.set_promotion(promotions.SecondHalfPrice("Test"))
    
    with pytest.raises(ValueError, match="Not enough products available"):
        product.buy(10)
    
    # Test limited product with promotion
    limited = products.LimitedProduct("Limited", price=100, quantity=10, maximum=2)
    limited.set_promotion(promotions.ThirdOneFree("Test"))
    
    with pytest.raises(ValueError, match="Cannot purchase more than 2 units in one order"):
        limited.buy(3)


def test_non_stocked_product_with_promotion():
    """Test promotions with non-stocked products."""
    product = products.NonStockedProduct("Digital Product", price=100)
    product.set_promotion(promotions.PercentDiscount("20% off", percent=20))
    
    # Test price calculation
    assert product.buy(2) == 160.0  # 100 * 2 * 0.8
    
    # Test display
    assert "[20% off]" in product.show()
    
    # Test multiple quantities
    assert product.buy(5) == 400.0  # 100 * 5 * 0.8


if __name__ == "__main__":
    pytest.main([__file__]) 