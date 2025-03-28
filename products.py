#!/usr/bin/env python3
"""
Module for managing products in a store.
"""

import logging
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    """
    Represents a product in the store with name, price, and availability.
    
    Attributes:
        name (str): Name of the product
        price (float): Price of the product
        quantity (int): Available quantity
        active (bool): Availability status of the product
        promotion (Optional[Promotion]): Current promotion on the product
    """
    
    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Initializes a new product.
        
        Args:
            name: Name of the product
            price: Price of the product
            quantity: Available quantity
            
        Raises:
            ValueError: If name is empty or price/quantity is negative
        """
        if not name:
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
            
        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = quantity > 0
        self._promotion = None
        
        logging.info(f"Created new product: {self.show()}")
        
    @property
    def name(self) -> str:
        """Returns the name of the product."""
        return self._name
        
    @property
    def price(self) -> float:
        """Returns the price of the product."""
        return self._price
        
    @property
    def quantity(self) -> int:
        """Returns the current quantity of the product."""
        return self._quantity
        
    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Sets the quantity of the product and updates the activity status.
        
        Args:
            value: New quantity of the product
            
        Raises:
            ValueError: If quantity is negative
        """
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        
        old_quantity = self._quantity
        self._quantity = value
        self._active = value > 0
        
        if old_quantity != value:
            logging.info(f"Quantity changed for {self.name}: {old_quantity} -> {value}")
        
    @property
    def active(self) -> bool:
        """Returns whether the product is active."""
        return self._active
        
    @property
    def promotion(self) -> Optional['Promotion']:
        """Returns the current promotion on the product."""
        return self._promotion
        
    def set_promotion(self, promotion: Optional['Promotion']) -> None:
        """
        Sets a promotion on the product.
        
        Args:
            promotion: Promotion to apply, or None to remove promotion
        """
        self._promotion = promotion
        if promotion:
            logging.info(f"Added promotion '{promotion.name}' to {self.name}")
        else:
            logging.info(f"Removed promotion from {self.name}")
        
    def activate(self) -> None:
        """
        Manually activates the product.
        Note: This will not change the quantity.
        """
        if not self._active:
            self._active = True
            logging.info(f"Product activated: {self.name}")
        
    def deactivate(self) -> None:
        """
        Manually deactivates the product.
        Note: This will not change the quantity.
        """
        if self._active:
            self._active = False
            logging.info(f"Product deactivated: {self.name}")
        
    def show(self) -> str:
        """
        Creates a string representation of the product.
        
        Returns:
            Formatted product information as string
        """
        result = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            result += f" [{self.promotion.name}]"
        return result
        
    def buy(self, quantity: int) -> float:
        """
        Purchases a specific quantity of the product.
        
        Args:
            quantity: Quantity to purchase
            
        Returns:
            Total price of the purchase
            
        Raises:
            ValueError: If quantity is negative or greater than available
            RuntimeError: If product is not active
        """
        if not self.active:
            raise RuntimeError("Product is not active")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if quantity > self.quantity:
            raise ValueError("Not enough products available")
            
        # Calculate price with promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price
            
        self.quantity -= quantity
        logging.info(f"Purchase made: {quantity}x {self.name} for ${total_price}")
        return total_price


class NonStockedProduct(Product):
    """
    Represents a product that doesn't need quantity tracking.
    Example: Software licenses
    """
    
    def __init__(self, name: str, price: float) -> None:
        """
        Initializes a new non-stocked product.
        
        Args:
            name: Name of the product
            price: Price of the product
            
        Raises:
            ValueError: If name is empty or price is negative
        """
        super().__init__(name, price, quantity=0)
        self._active = True  # Non-stocked products are always active
        
    @property
    def quantity(self) -> int:
        """Always returns 0 for non-stocked products."""
        return 0
        
    @quantity.setter
    def quantity(self, value: int) -> None:
        """Ignores quantity changes for non-stocked products."""
        pass
        
    def show(self) -> str:
        """
        Creates a string representation of the non-stocked product.
        
        Returns:
            Formatted product information as string
        """
        result = f"{self.name} (Digital), Price: {self.price}"
        if self.promotion:
            result += f" [{self.promotion.name}]"
        return result
        
    def buy(self, quantity: int) -> float:
        """
        Purchases a specific quantity of the non-stocked product.
        
        Args:
            quantity: Quantity to purchase
            
        Returns:
            Total price of the purchase
            
        Raises:
            ValueError: If quantity is not positive
        """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
            
        # Calculate price with promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price
            
        logging.info(f"Purchase made: {quantity}x {self.name} for ${total_price}")
        return total_price


class LimitedProduct(Product):
    """
    Represents a product with a maximum purchase quantity per order.
    Example: Shipping fees
    """
    
    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        """
        Initializes a new limited product.
        
        Args:
            name: Name of the product
            price: Price of the product
            quantity: Available quantity
            maximum: Maximum quantity that can be purchased in one order
            
        Raises:
            ValueError: If name is empty, price/quantity is negative, or maximum is not positive
        """
        if maximum <= 0:
            raise ValueError("Maximum purchase quantity must be positive")
            
        self._maximum = maximum
        super().__init__(name, price, quantity)
        
    @property
    def maximum(self) -> int:
        """Returns the maximum purchase quantity per order."""
        return self._maximum
        
    def show(self) -> str:
        """
        Creates a string representation of the limited product.
        
        Returns:
            Formatted product information as string
        """
        result = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per order: {self.maximum}"
        if self.promotion:
            result += f" [{self.promotion.name}]"
        return result
        
    def buy(self, quantity: int) -> float:
        """
        Purchases a specific quantity of the limited product.
        
        Args:
            quantity: Quantity to purchase
            
        Returns:
            Total price of the purchase
            
        Raises:
            ValueError: If quantity is negative, greater than available, or exceeds maximum
            RuntimeError: If product is not active
        """
        if not self.active:
            raise RuntimeError("Product is not active")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if quantity > self.quantity:
            raise ValueError("Not enough products available")
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} units in one order")
            
        self.quantity -= quantity
        
        # Calculate price with promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price
            
        logging.info(f"Purchase made: {quantity}x {self.name} for ${total_price}")
        return total_price


def main():
    """Main function for testing the Product class."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Test code
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    windows = NonStockedProduct("Windows License", price=125)
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    print(bose.buy(50))  # 12500.0
    print(mac.buy(100))  # 145000.0
    print(mac.active)  # False

    print(bose.show())  # Bose QuietComfort Earbuds, Price: 250, Quantity: 450
    print(mac.show())   # MacBook Air M2, Price: 1450, Quantity: 0
    print(windows.show())  # Windows License (Digital), Price: 125
    print(shipping.show())  # Shipping, Price: 10, Quantity: 250, Max per order: 1

    bose.quantity = 1000
    print(bose.show())  # Bose QuietComfort Earbuds, Price: 250, Quantity: 1000


if __name__ == "__main__":
    main()
