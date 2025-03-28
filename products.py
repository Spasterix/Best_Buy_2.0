"""
Module for managing products in a store.
"""


class Product:
    """
    Represents a product in the store with name, price, and availability.

    Attributes:
        name (str): Name of the product
        price (float): Price of the product
        quantity (int): Available quantity
        active (bool): Availability status of the product
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

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        """Returns the current quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Sets the quantity of the product and updates the activity status.

        Args:
            quantity: New quantity of the product

        Raises:
            ValueError: If quantity is negative
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self) -> bool:
        """Returns whether the product is active."""
        return self.active

    def activate(self) -> None:
        """Activates the product."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivates the product."""
        self.active = False

    def show(self) -> str:
        """
        Creates a string representation of the product.

        Returns:
            Formatted product information as string
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

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
        if not self.is_active():
            raise RuntimeError("Product is not active")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if quantity > self.quantity:
            raise ValueError("Not enough products available")

        self.set_quantity(self.quantity - quantity)
        return quantity * self.price


def main():
    """Main function for testing the Product class."""
    # Test code
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))  # 12500.0
    print(mac.buy(100))  # 145000.0
    print(mac.is_active())  # False

    print(bose.show())  # Bose QuietComfort Earbuds, Price: 250, Quantity: 450
    print(mac.show())  # MacBook Air M2, Price: 1450, Quantity: 0

    bose.set_quantity(1000)
    print(bose.show())  # Bose QuietComfort Earbuds, Price: 250, Quantity: 1000


if __name__ == "__main__":
    main()
