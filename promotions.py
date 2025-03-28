#!/usr/bin/env python3
"""
Module for managing product promotions.
"""

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    """
    Abstract base class for all promotions.
    
    Attributes:
        name (str): Name of the promotion
    """
    
    def __init__(self, name: str) -> None:
        """
        Initializes a new promotion.
        
        Args:
            name: Name of the promotion
        """
        self._name = name
        
    @property
    def name(self) -> str:
        """Returns the name of the promotion."""
        return self._name
        
    @abstractmethod
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Applies the promotion to a product and returns the discounted price.
        
        Args:
            product: Product to apply promotion to
            quantity: Quantity to purchase
            
        Returns:
            Total price after promotion
        """
        pass


class PercentDiscount(Promotion):
    """
    Represents a percentage discount promotion.
    Example: 20% off
    """
    
    def __init__(self, name: str, percent: float) -> None:
        """
        Initializes a new percentage discount promotion.
        
        Args:
            name: Name of the promotion
            percent: Discount percentage (0-100)
            
        Raises:
            ValueError: If percent is not between 0 and 100
        """
        if not 0 <= percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
            
        super().__init__(name)
        self._percent = percent
        
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Applies percentage discount to the total price.
        
        Args:
            product: Product to apply discount to
            quantity: Quantity to purchase
            
        Returns:
            Total price after discount
        """
        base_price = product.price * quantity
        discount = base_price * (self._percent / 100)
        return base_price - discount


class SecondHalfPrice(Promotion):
    """
    Represents a promotion where the second item is half price.
    Example: Buy 2 items, second one is 50% off
    """
    
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Applies second item half price promotion.
        
        Args:
            product: Product to apply promotion to
            quantity: Quantity to purchase
            
        Returns:
            Total price after promotion
        """
        if quantity < 2:
            return product.price * quantity
            
        # Calculate number of pairs and remaining items
        pairs = quantity // 2
        remaining = quantity % 2
        
        # Price for pairs (first item full price, second half price)
        pair_price = product.price * 1.5
        # Price for remaining items (full price)
        remaining_price = product.price * remaining
        
        return (pair_price * pairs) + remaining_price


class ThirdOneFree(Promotion):
    """
    Represents a promotion where every third item is free.
    Example: Buy 3 items, get 1 free
    """
    
    def apply_promotion(self, product: 'Product', quantity: int) -> float:
        """
        Applies buy 2 get 1 free promotion.
        
        Args:
            product: Product to apply promotion to
            quantity: Quantity to purchase
            
        Returns:
            Total price after promotion
        """
        if quantity < 3:
            return product.price * quantity
            
        # Calculate number of groups of 3 and remaining items
        groups = quantity // 3
        remaining = quantity % 3
        
        # Price for groups (2 items at full price, 1 free)
        group_price = product.price * 2
        # Price for remaining items (full price)
        remaining_price = product.price * remaining
        
        return (group_price * groups) + remaining_price 