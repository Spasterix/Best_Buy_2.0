#!/usr/bin/env python3
"""
Module for managing a store with multiple products.
"""

from typing import List, Tuple
from products import Product


class Store:
    """
    Represents a store that manages multiple products.
    
    The Store class implements a composition pattern where it maintains
    a collection of Product instances.
    
    Attributes:
        products (List[Product]): List of products available in the store
    """
    
    def __init__(self, products: List[Product] = None) -> None:
        """
        Initializes a new store with an optional list of products.
        
        Args:
            products: Initial list of products (optional)
        """
        self.products = products if products is not None else []
        
    def add_product(self, product: Product) -> None:
        """
        Adds a new product to the store.
        
        Args:
            product: Product instance to add
        """
        if product not in self.products:
            self.products.append(product)
            
    def remove_product(self, product: Product) -> None:
        """
        Removes a product from the store.
        
        Args:
            product: Product instance to remove
        """
        if product in self.products:
            self.products.remove(product)
            
    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.
        
        Returns:
            Total number of items across all products
        """
        return sum(product.quantity for product in self.products)
        
    def get_all_products(self) -> List[Product]:
        """
        Returns all active products in the store.
        
        Returns:
            List of active products
        """
        return [product for product in self.products if product.active]
        
    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Processes an order of multiple products.
        
        Args:
            shopping_list: List of tuples containing (Product, quantity)
            
        Returns:
            Total price of the order
            
        Raises:
            ValueError: If product is not in store or other validation fails
        """
        total_price = 0.0
        
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Product not available in this store")
            total_price += product.buy(quantity)
            
        return total_price


def main():
    """Main function for testing the Store class."""
    # Create products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    
    # Create store with initial products
    best_buy = Store([bose, mac])
    
    # Add new product
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    best_buy.add_product(pixel)
    
    # Test ordering
    price = best_buy.order([(bose, 5), (mac, 30), (bose, 10)])
    print(f"Order cost: {price} dollars.")
    
    # Test other methods
    print(f"Total quantity in store: {best_buy.get_total_quantity()}")
    print("Active products:")
    for product in best_buy.get_all_products():
        print(product.show())


if __name__ == "__main__":
    main()
