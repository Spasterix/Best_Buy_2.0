#!/usr/bin/env python3
"""
Main module providing a user interface for the store management system.
"""

from typing import List
import products
import store
import promotions


def display_menu() -> None:
    """Displays the main menu options."""
    print("\n=== Store Management System ===")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")
    print("============================")


def list_products(store_instance: store.Store) -> None:
    """
    Lists all active products in the store.
    
    Args:
        store_instance: Store instance to display products from
    """
    print("\nAvailable Products:")
    print("-----------------")
    for idx, product in enumerate(store_instance.get_all_products(), 1):
        print(f"{idx}. {product.show()}")


def show_total_amount(store_instance: store.Store) -> None:
    """
    Shows the total quantity of items in the store.
    
    Args:
        store_instance: Store instance to get total from
    """
    total = store_instance.get_total_quantity()
    print(f"\nTotal amount of items in store: {total}")


def make_order(store_instance: store.Store) -> None:
    """
    Handles the order process.
    
    Args:
        store_instance: Store instance to order from
    """
    shopping_list = []
    active_products = store_instance.get_all_products()
    
    if not active_products:
        print("\nNo active products available for purchase!")
        return
        
    while True:
        list_products(store_instance)
        print("\nEnter product number and quantity (e.g., '1 5'), or 'done' to finish:")
        
        user_input = input("> ").strip().lower()
        if user_input == 'done':
            break
            
        try:
            prod_num, quantity = map(int, user_input.split())
            if 1 <= prod_num <= len(active_products):
                product = active_products[prod_num - 1]
                shopping_list.append((product, quantity))
                print(f"Added to cart: {quantity}x {product.name}")
            else:
                print("Invalid product number!")
        except ValueError:
            print("Invalid input! Please use format 'product_number quantity'")
            
    if shopping_list:
        try:
            total_price = store_instance.order(shopping_list)
            print(f"\nOrder completed! Total price: ${total_price:.2f}")
        except ValueError as e:
            print(f"\nError processing order: {e}")
    else:
        print("\nNo items in order!")


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
            if isinstance(product, products.LimitedProduct):
                product.quantity = 250  # Reset limited products to 250
            else:
                product.quantity = 100  # Reset regular products to 100


def main():
    """Main entry point of the application."""
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
    
    best_buy = store.Store(product_list)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            list_products(best_buy)
        elif choice == '2':
            show_total_amount(best_buy)
        elif choice == '3':
            make_order(best_buy)
            reset_product_quantities(product_list)  # Reset quantities after order
        elif choice == '4':
            print("\nThank you for using the Store Management System!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
