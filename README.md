# 🏪 Store Management System

A modern Python-based store management system that allows you to manage products, process orders, and handle promotions efficiently.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Product Management**: Track products with names, prices, and quantities
- **Multiple Product Types**: Regular, Non-stocked, and Limited products
- **Promotion System**: Support for various promotion types
  - Percentage discounts
  - Second item half price
  - Buy 2, get 1 free
- **Inventory Control**: Automatic stock updates after purchases
- **Order Processing**: Simple and intuitive ordering system
- **Active/Inactive Products**: Automatic product status management
- **User-Friendly Interface**: Clear command-line interface for all operations
- **Magic Methods**: Pythonic implementation with properties and magic methods

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/store-management.git
cd store-management
```

2. Make sure you have Python 3.6+ installed:
```bash
python --version
```

3. No additional dependencies required! The system uses only Python standard library.

## 🚀 Usage

Run the main program:
```bash
python main.py
```

### 📋 Available Commands

The system offers four main operations:

1. **List Products** - View all active products in store
2. **Show Total Amount** - Display total inventory count
3. **Make Order** - Process a new order
4. **Quit** - Exit the program

### 💡 Example Usage

```plaintext
=== Store Management System ===
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
============================

> 1
Available Products:
-----------------
1. MacBook Air M2, Price: $1450, Quantity: 100 [Second Half price!]
2. Bose QuietComfort Earbuds, Price: $250, Quantity: 500 [Third One Free!]
3. Google Pixel 7, Price: $500, Quantity: 250
4. Windows License, Price: $125, Quantity: 0 [30% off!]
5. Shipping, Price: $10, Quantity: 250, Max per order: 1
```

## 🏗️ Project Structure

```
store-management/
├── main.py          # Main application entry point
├── products.py      # Product class definitions
├── store.py         # Store class definition
├── promotions.py    # Promotion system
├── test_product.py  # Product tests
├── test_menu.py     # Menu functionality tests
└── README.md        # Project documentation
```

## 🎯 Class Overview

### Product Classes
- **Product**: Base class for regular products
- **NonStockedProduct**: For digital items (no quantity tracking)
- **LimitedProduct**: For items with maximum purchase limits
- Features:
  - Properties for name, price, quantity
  - Magic methods for comparison and string representation
  - Promotion support
  - Active status management

### Store Class
- Manages collection of products
- Processes orders
- Tracks inventory
- Supports store combination with `+` operator
- Product containment checking with `in` operator

### Promotion Classes
- **Promotion**: Abstract base class
- **PercentDiscount**: Percentage-based discounts
- **SecondHalfPrice**: Second item at half price
- **ThirdOneFree**: Buy 2, get 1 free

## 🔍 Features in Detail

### Product Management
- Each product has:
  - Name
  - Price
  - Quantity (except NonStockedProduct)
  - Active status
  - Optional promotion

### Order Processing
- Multiple items per order
- Automatic inventory updates
- Input validation
- Error handling
- Promotion application
- Quantity limits enforcement

### Inventory Control
- Automatic product deactivation when out of stock
- Real-time quantity tracking
- Total inventory monitoring
- Automatic quantity reset after orders

## 🛡️ Error Handling

The system includes robust error handling for:
- Invalid product selections
- Insufficient stock
- Invalid input formats
- Out-of-range quantities
- Invalid promotion parameters
- Maximum purchase limit violations

## 💻 Development

### Code Style
- Follows PEP 8 guidelines
- Type hints for better code clarity
- Comprehensive docstrings
- Clean and modular design
- Magic methods and properties
- Object-oriented design patterns

### Best Practices
- Object-Oriented Programming principles
- DRY (Don't Repeat Yourself)
- SOLID principles
- Defensive programming
- Comprehensive test coverage
- Clear separation of concerns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Built with modern Python features
- Designed for extensibility
- Focus on user experience
- Comprehensive test suite
- Clean and maintainable code

---
Made with ❤️ by Alexander Krause