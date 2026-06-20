# inventory.py
# Name: Sandu Stati Suman
# Description: Contains the Inventory class, which manages a collection of
#              Product objects and provides methods for searching, reporting,
#              and general maintenance of the stock.

from product import Product


class Inventory:
    """
    Manages a collection of Product objects, stored in a dictionary keyed
    by product ID.

    Attributes:
        _products (dict): Maps product_id -> Product object.
    """

    def __init__(self):
        """Initialises an empty inventory with no products."""
        self._products = {}

    def add_product(self, name, category, price, quantity, min_stock):
        """
        Create a new Product with a generated ID and add it to the inventory.

        Returns:
            str: The newly generated product_id.
        """
        product_id = self._generate_id()
        self._products[product_id] = Product(product_id, name, category, price, quantity, min_stock)

        return product_id

    def remove_product(self, product_id):
        """Remove a product by ID. Returns the removed Product, or None if not found."""
        if product_id not in self._products:
            return None
        removed_item = self._products[product_id]
        del self._products[product_id]

        return removed_item

    def get_product(self, product_id):
        """Retrieve a Product object by its ID. Returns None if not found."""
        if product_id not in self._products:
            return None

        return self._products[product_id]

    def get_all_products(self):
        """Return a list of all Product objects currently in the inventory."""
        return list(self._products.values())

    def find_by_name(self, name):
        """
        Find a product by an exact, case-insensitive name match.

        Returns:
            str or None: The matching product_id, or None if no match is found.
        """
        for product_id, product in self._products.items():
            if name.lower() == product.name.lower():
                return product_id
        return None

    def search_by_name(self, search_term):
        """Return a list of Product objects whose names contain the search term."""
        matches = list()
        search_term_lower = search_term.lower()

        for product in self._products.values():
            if search_term_lower in product.name.lower():
                matches.append(product)

        return matches

    def search_by_category(self, category):
        """Return a list of all Product objects within a specific category."""
        matches = list()
        category_lower = category.lower()

        for product in self._products.values():
            if category_lower == product.category.lower():
                matches.append(product)

        return matches

    def get_low_stock_products(self):
        """Return a list of Product objects currently at or below their minimum stock level."""
        low_stock_products_list = list()

        for product in self._products.values():
            if product.is_low_stock():
                low_stock_products_list.append(product)

        return low_stock_products_list

    def generate_category_report(self):
        """
        Calculate the product count and total stock value for each category.

        Returns:
            dict: Maps category name -> {"count": int, "value": float}.
        """
        category_statistics = dict()

        for product in self._products.values():
            category = product.category

            if category not in category_statistics:
                category_statistics[category] = {"count": 0, "value": 0}

            category_statistics[category]['count'] += 1
            category_statistics[category]['value'] += product.get_value()

        return category_statistics

    def calculate_total_value(self):
        """Calculate the total monetary value of all stock in the inventory."""
        inventory_value = 0

        for product in self._products.values():
            product_value = product.get_value()
            inventory_value += product_value

        return inventory_value

    def _generate_id(self):
        """Generate the next unique, incremental product ID (e.g. P001, P002, ...)."""
        if not self._products:
            product_id = "P001"
            return product_id

        max_num = 0
        for p_id in self._products.keys():
            num = int(p_id[1:])
            if num > max_num:
                max_num = num

        next_num = max_num + 1
        product_id = f"P{next_num:03d}"

        return product_id

    def __len__(self):
        """Return the total number of products in the inventory."""
        return len(self._products)