# inventory_operations.py
# Name: Sandu Stati Suman
# Date: 20/03/2026
# Description: Handles all the operations that are associated with managing
#              the inventory system such as adding products, updating product
#              characteristics and searching through the inventory.


"""
Inventory operations module.

This module contains all menu handler functions for inventory management.
These functions interact with Product and Inventory objects.

"""

import transaction_operations


def view_all_products_menu(inventory):
    """Return all products in a formatted table string for the GUI."""
    products = inventory.get_all_products()
    
    if not products:
        return "No products in inventory."
    
    # We build a string
    output = "--- All Products ---\n\n"
    output += f"{'ID':<6} {'Product':<20} {'Category':<15} {'Price':<10} {'Stock':<10} {'Min Stock':<10}\n"
    output += "=" * 73 + "\n"
    
    for product in products:
        output += f"{product.product_id:<6} {product.name:<20} {product.category:<15} €{product.price:<9} {product.quantity:<10} {product.min_stock:<10}\n"
    
    output += "=" * 73 + "\n"
    output += f"Total products: {len(inventory)}"

    return output


def add_product_menu(inventory, transactions):
    """Add a new product to inventory."""
    print("\n--- Add New Product ---")
    
    # Get product name
    name = input("Enter product name: ").strip()
    
    product_id = inventory.find_by_name(name)

    if product_id is not None:
        print(f"Error: Product '{name}' already exists.")
        return False
    
    # Get remaining details
    from main import get_valid_float, get_valid_int
    category = input("Enter category: ").strip()
    price = get_valid_float("Enter price (€): ", min_value=0.01)
    qty = get_valid_int("Enter current stock quantity: ", min_value=0)
    min_stock = get_valid_int("Enter minimum stock level: ", min_value=0)
    
    product_id = inventory.add_product(name, category, price, qty, min_stock)
    
    # Log transaction
    transaction_operations.log_transaction(transactions, "added", product_id, name, qty)
    
    print(f"\nProduct '{name}' added successfully with ID: {product_id}")
    return product_id


def update_stock_menu(inventory, transactions):
    """Update stock for a product (sale or delivery)."""
    print("\n--- Update Stock ---")
    
    # Get product name
    name = input("Enter product name: ").strip()
    
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    product = inventory.get_product(product_id)
    
    # Get transaction type
    transaction_type = input("Is this a (S)ale or (D)elivery? ").strip().lower()
    
    while transaction_type not in ['s', 'd', 'sale', 'delivery']:
        print("Error: Please enter 'S' for sale or 'D' for delivery")
        transaction_type = input("Is this a (S)ale or (D)elivery? ").strip().lower()
    
    # Get quantity
    from main import get_valid_int
    quantity = get_valid_int("Enter quantity: ", min_value=1)
    
    try:
        if transaction_type in ['s', 'sale']:
            trans_type = "sale"
            change = -quantity
            product.update_stock(change)
        else:  # delivery
            trans_type = "delivery"
            change = quantity
            product.update_stock(change)
        
        # Log transaction
        transaction_operations.log_transaction(transactions, trans_type, product_id, product.name, change)
        
        print(f"\nStock updated! {product.name} now has {product.quantity} units.")
        return True
        
    except ValueError as e:
        print(f"Error: {e}")
        return False


def update_product_details_menu(inventory):
    """Update product details (name, category, price, min_stock)."""
    print("\n--- Update Product Details ---")
    
    # Get product name
    name = input("Enter product name: ").strip()
    
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    product = inventory.get_product(product_id)
    
    # Display current details
    print(f"\nCurrent details for {product.product_id}:")
    print(f"  Name: {product.name}")
    print(f"  Category: {product.category}")
    print(f"  Price: €{product.price:.2f}")
    print(f"  Min Stock: {product.min_stock}")
    
    # Get update choice
    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Category")
    print("3. Price")
    print("4. Minimum Stock Level")
    print("5. Cancel")
    
    from main import get_valid_int
    choice = get_valid_int("Enter your choice (1-5): ", min_value=1)
    
    while choice not in range(1, 6):
        print("Error: Please enter a number between 1 and 5")
        choice = get_valid_int("Enter your choice (1-5): ", min_value=1)
    
    if choice == 5:
        print("Update cancelled.")
        return False
    
    try:
        if choice == 1:
            new_name = input("Enter new name: ").strip()
            product.name = new_name
            print(f"\nName updated successfully to: {new_name}")
        
        elif choice == 2:
            new_category = input("Enter new category: ").strip()
            product.category = new_category
            print(f"\nCategory updated successfully to: {new_category}")
        
        elif choice == 3:
            from main import get_valid_float
            new_price = get_valid_float("Enter new price (€): ", min_value=0.01)
            product.price = new_price
            print(f"\nPrice updated successfully to: €{new_price:.2f}")
        
        elif choice == 4:
            new_min_stock = get_valid_int("Enter new minimum stock level: ", min_value=0)
            product.min_stock = new_min_stock
            print(f"\nMinimum stock level updated successfully to: {new_min_stock}")
        
        return True
        
    except ValueError as e:
        print(f"Error: {e}")
        return False


def remove_product_menu(inventory, transactions):
    """Remove a product from inventory."""
    print("\n--- Remove Product ---")
    
    # Get product name
    name = input("Enter product name to remove: ").strip()
    
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    # Confirm removal
    confirm = input(f"Are you sure you want to remove '{name}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        removed = inventory.remove_product(product_id)
        
        if removed:
            # Log transaction
            transaction_operations.log_transaction(transactions, "removed", product_id, removed.name, 0)
            print(f"\nProduct '{removed.name}' removed successfully.")
            return True
    else:
        print("Removal cancelled.")
        return False


def search_products_menu(inventory):
    """Search for products by name or category."""
    print("\n--- Search Products ---")
    print("1. Search by name")
    print("2. Search by category")
    
    from main import get_valid_int
    choice = get_valid_int("Enter your choice (1-2): ", min_value=1)
    
    while choice not in [1, 2]:
        print("Error: Please enter 1 or 2")
        choice = get_valid_int("Enter your choice (1-2): ", min_value=1)
    
    if choice == 1:
        search_term = input("Enter product name (or part of name): ").strip()
        results = inventory.search_by_name(search_term)
    else:
        category = input("Enter category: ").strip()
        results = inventory.search_by_category(category)
    
    if not results:
        print("No products found matching your search.")
        return
    
    print(f"\nFound {len(results)} product(s):\n")
    print(f"{'ID':<6} {'Product':<20} {'Category':<15} {'Price':<10} {'Stock':<10}")
    print("=" * 61)
    
    for product in results:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} €{product.price:<9} {product.quantity:<10}")


def view_low_stock_menu(inventory):
    """Display products at or below minimum stock levels."""
    print("\n--- Low Stock Alerts ---")
    
    low_stock = inventory.get_low_stock_products()
    
    if not low_stock:
        print("No products are currently low on stock.")
        return
    
    print(f"Found {len(low_stock)} product(s) needing restocking:\n")
    print(f"{'ID':<6} {'Product':<20} {'Category':<15} {'Current':<10} {'Minimum':<10}")
    print("=" * 61)
    
    for product in low_stock:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} {product.quantity:<10} {product.min_stock:<10}")


def view_category_report_menu(inventory):
    """Generate and display category report."""
    print("\n--- Category Report ---")
    
    report = inventory.generate_category_report()
    
    if not report:
        print("No products in inventory.")
        return
    
    print(f"{'Category':<20} {'Count':<10} {'Total Value':<15}")
    print("=" * 45)
    
    total_products = 0
    total_value = 0.0
    
    for category, stats in sorted(report.items()):
        print(f"{category:<20} {stats['count']:<10} €{stats['value']:<14.2f}")
        total_products += stats['count']
        total_value += stats['value']
    
    print("=" * 45)
    print(f"{'TOTAL':<20} {total_products:<10} €{total_value:<14.2f}")


def view_transaction_log_menu(transactions):
    """View recent transaction history."""
    print("\n--- Transaction Log ---")
    
    if not transactions:
        print("No transactions recorded.")
        return
    
    from main import get_valid_int
    num = get_valid_int("How many recent transactions to display? (default 10): ", min_value=1)
    
    # Use transaction_operations module
    transaction_operations.view_transaction_log(transactions, num)
