#!/usr/bin/env python3
"""
Test module for product promotions.
"""

import pytest
from products import Product, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


def test_percent_discount():
    """Test percentage discount promotion."""
    product = Product("Test Product", price=100, quantity=10)
    promotion = PercentDiscount("20% off", percent=20)
    product.set_promotion(promotion)
    
    # Test single item
    assert product.buy(1) == 80.0  # 100 - 20%
    
    # Test multiple items
    assert product.buy(3) == 240.0  # (100 * 3) - 20%
    
    # Test invalid percentage
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
        PercentDiscount("Invalid", percent=150)


def test_second_half_price():
    """Test second item half price promotion."""
    product = Product("Test Product", price=100, quantity=10)
    promotion = SecondHalfPrice("Second Half Price!")
    product.set_promotion(promotion)
    
    # Test single item
    assert product.buy(1) == 100.0  # Full price
    
    # Test pair of items
    assert product.buy(2) == 150.0  # 100 + 50
    
    # Test multiple pairs
    assert product.buy(4) == 300.0  # (100 + 50) * 2
    
    # Test with remaining item
    assert product.buy(3) == 250.0  # (100 + 50) + 100


def test_third_one_free():
    """Test buy 2 get 1 free promotion."""
    product = Product("Test Product", price=100, quantity=20)
    promotion = ThirdOneFree("Third One Free!")
    product.set_promotion(promotion)
    
    # Test single item
    assert product.buy(1) == 100.0  # Full price
    
    # Test two items
    assert product.buy(2) == 200.0  # Full price for both
    
    # Test three items
    assert product.buy(3) == 200.0  # Pay for 2, get 1 free
    
    # Test multiple groups
    assert product.buy(6) == 400.0  # Pay for 4, get 2 free
    
    # Test with remaining items
    assert product.buy(4) == 300.0  # Pay for 3, get 1 free, plus 1 full price


def test_promotion_on_non_stocked_product():
    """Test promotions on non-stocked products."""
    product = NonStockedProduct("Digital Product", price=100)
    promotion = PercentDiscount("30% off", percent=30)
    product.set_promotion(promotion)
    
    assert product.buy(1) == 70.0  # 100 - 30%
    assert product.buy(3) == 210.0  # (100 * 3) - 30%


def test_promotion_on_limited_product():
    """Test promotions on limited products."""
    product = LimitedProduct("Limited Product", price=100, quantity=10, maximum=5)
    promotion = SecondHalfPrice("Second Half Price!")
    product.set_promotion(promotion)
    
    # Test within limit
    assert product.buy(2) == 150.0  # 100 + 50
    
    # Test exceeding limit
    with pytest.raises(ValueError, match="Cannot purchase more than 5 units in one order"):
        product.buy(6)


def test_promotion_removal():
    """Test removing promotions from products."""
    product = Product("Test Product", price=100, quantity=10)
    promotion = PercentDiscount("20% off", percent=20)
    
    # Add promotion
    product.set_promotion(promotion)
    assert product.promotion == promotion
    assert product.buy(1) == 80.0
    
    # Remove promotion
    product.set_promotion(None)
    assert product.promotion is None
    assert product.buy(1) == 100.0


def test_promotion_display():
    """Test promotion display in product string representation."""
    product = Product("Test Product", price=100, quantity=10)
    promotion = PercentDiscount("20% off", percent=20)
    
    # Test without promotion
    assert "Promotion" not in product.show()
    
    # Test with promotion
    product.set_promotion(promotion)
    assert "Promotion: 20% off" in product.show()


def main():
    """Main function to run tests directly."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    main() 