# 🏪 Store Management System

A modern Python-based store management system that allows you to manage products and process orders efficiently.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Product Management**: Track products with names, prices, and quantities
- **Inventory Control**: Automatic stock updates after purchases
- **Order Processing**: Simple and intuitive ordering system
- **Active/Inactive Products**: Automatic product status management
- **User-Friendly Interface**: Clear command-line interface for all operations

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
1. MacBook Air M2, Price: 1450, Quantity: 100
2. Bose QuietComfort Earbuds, Price: 250, Quantity: 500
3. Google Pixel 7, Price: 500, Quantity: 250
```

## 🏗️ Project Structure

```
store-management/
├── main.py          # Main application entry point
├── products.py      # Product class definition
├── store.py         # Store class definition
└── README.md        # Project documentation
```

## 🎯 Class Overview

### Product Class
- Manages individual product details
- Handles product status (active/inactive)
- Validates product operations

### Store Class
- Manages collection of products
- Processes orders
- Tracks inventory

## 🔍 Features in Detail

### Product Management
- Each product has:
  - Name
  - Price
  - Quantity
  - Active status

### Order Processing
- Multiple items per order
- Automatic inventory updates
- Input validation
- Error handling

### Inventory Control
- Automatic product deactivation when out of stock
- Real-time quantity tracking
- Total inventory monitoring

## 🛡️ Error Handling

The system includes robust error handling for:
- Invalid product selections
- Insufficient stock
- Invalid input formats
- Out-of-range quantities

## 💻 Development

### Code Style
- Follows PEP 8 guidelines
- Type hints for better code clarity
- Comprehensive docstrings
- Clean and modular design

### Best Practices
- Object-Oriented Programming principles
- DRY (Don't Repeat Yourself)
- SOLID principles
- Defensive programming

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Built with modern Python features
- Designed for extensibility
- Focus on user experience

---
Made with ❤️ by Alexander Krause