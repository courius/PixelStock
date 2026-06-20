# data_handler.py
# Description: File operations for Murphy's General Store Inventory System.
#              Handles loading, saving, and exporting data.

"""
Data handler module.

This module provides functions for persistent storage and data export.
It handles loading and saving inventory and transactions as JSON,
and exporting reports as CSV and text files.
"""

import json
import csv
from datetime import datetime
from product import Product
from inventory import Inventory


def load_inventory(filename):
    """
    Load inventory from a JSON file and rebuild it as an Inventory of Product objects.

    Parameters:
        filename (str): Path to the JSON file

    Returns:
        tuple: (status message, Inventory object). The Inventory is empty
               if the file doesn't exist or can't be read.
    """
    inventory = Inventory()

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for product_id, product_data in data.items():
            product = Product.from_dict(product_id, product_data)
            inventory._products[product_id] = product

        return f"Loaded  {len(inventory)}  products  from  {filename}", inventory

    except FileNotFoundError:
        return f"Note:  {filename} not  found.  Starting  with  empty  inventory.", inventory

    except json.JSONDecodeError:
        return f"Error:  {filename}  is  corrupted.  Starting  with  empty  inventory.", inventory

    except Exception as e:
        return f"Error  loading  inventory:  {e}", inventory


def save_inventory(inventory, filename):
    """
    Save inventory to a JSON file.

    Parameters:
        inventory (Inventory): Inventory object to save
        filename (str): Path to the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        data = {}
        for product_id, product in inventory._products.items():
            data[product_id] = product.to_dict()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Inventory saved to {filename}")
        return True

    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False


def load_transactions(filename):
    """
    Load transactions from a JSON file.

    Parameters:
        filename (str): Path to the JSON file

    Returns:
        tuple: (status message, list of transaction dictionaries). The list
               is empty if the file doesn't exist or can't be read.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            transactions = json.load(f)

        return f"Loaded  {len(transactions)}  transactions  from  {filename}", transactions

    except FileNotFoundError:
        return f"Note:  {filename}  not  found.  Starting  with  empty  transaction  log.", []

    except json.JSONDecodeError:
        return f"Error:  {filename}  is  corrupted.  Starting  with  empty  transaction  log.", []

    except Exception as e:
        return f"Error  loading  transactions:  {e}", []


def save_transactions(transactions, filename):
    """
    Save transactions to a JSON file.

    Parameters:
        transactions (list): List of transaction dictionaries
        filename (str): Path to the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)

        print(f"Transactions saved to {filename}")
        return True

    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def export_inventory_to_csv(inventory, filename):
    """
    Export the full inventory to a CSV file.

    Parameters:
        inventory (Inventory): Inventory object to export
        filename (str): Path to the CSV file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Price', 'Quantity', 'Min Stock'])

            for product in inventory.get_all_products():
                writer.writerow([
                    product.product_id,
                    product.name,
                    product.category,
                    f"{product.price:.2f}",
                    product.quantity,
                    product.min_stock
                ])

        print(f"Inventory exported to {filename}")
        return True

    except Exception as e:
        print(f"Error exporting inventory: {e}")
        return False


def export_low_stock_to_csv(inventory, filename):
    """
    Export only the low-stock products to a CSV file, with a suggested
    reorder quantity for each one.

    Parameters:
        inventory (Inventory): Inventory object
        filename (str): Path to the CSV file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        low_stock_products = inventory.get_low_stock_products()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Current', 'Minimum', 'Order'])

            for product in low_stock_products:
                order_qty = product.min_stock - product.quantity + 5
                writer.writerow([
                    product.product_id,
                    product.name,
                    product.category,
                    product.quantity,
                    product.min_stock,
                    order_qty
                ])

        print(f"Low stock report exported to {filename}")
        return True

    except Exception as e:
        print(f"Error exporting low stock report: {e}")
        return False


def generate_text_report(inventory, filename):
    """
    Generate a formatted plain-text report of the full inventory.

    Parameters:
        inventory (Inventory): Inventory object
        filename (str): Path to the text file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(" " * 15 + "MURPHY'S GENERAL STORE - INVENTORY REPORT\n")
            f.write(" " * 20 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"{'ID':<8} {'Product':<20} {'Category':<15} {'Price':<10} "
                   f"{'Stock':<10} {'Min':<10}\n")
            f.write("=" * 80 + "\n")

            for product in inventory.get_all_products():
                f.write(f"{product.product_id:<8} {product.name:<20} {product.category:<15} "
                       f"€{product.price:<9.2f} {product.quantity:<10} {product.min_stock:<10}\n")

            f.write("=" * 80 + "\n")
            total_value = inventory.calculate_total_value()
            f.write(f"Total Products: {len(inventory)}\n")
            f.write(f"Total Value: €{total_value:.2f}\n")
            f.write("=" * 80 + "\n")

        print(f"Report saved to {filename}")
        return True

    except Exception as e:
        print(f"Error generating report: {e}")
        return False