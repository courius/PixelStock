# transaction_operations.py
# Name: Sandu Stati Suman
# Description: Logs every change made to stock (additions, sales, deliveries,
#              removals) so the inventory keeps a full history of activity.

"""
Transaction operations module.

Transactions are stored as a simple list of dictionaries rather than as a
class, since each entry only needs to be created once and read back later.
"""

from datetime import datetime


def log_transaction(transactions, trans_type, product_id, product_name, quantity):
    """
    Append a new transaction record to the transaction list.

    Parameters:
        transactions (list): The transaction list to append to
        trans_type (str): Type of transaction ("added", "sale", "delivery", "removed")
        product_id (str): ID of the affected product
        product_name (str): Name of the affected product
        quantity (int): Quantity change (positive for stock in, negative for stock out)
    """
    transaction = {
        "type": trans_type,
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat()
    }
    transactions.append(transaction)