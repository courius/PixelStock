# product.py
# Name: Sandu Stati Suman
# Description: Contains the Product class, which represents a single
#              inventory item with validated attributes and stock management.


class Product:
    """
    Represents a single product in the inventory system.

    Attributes:
        product_id (str)
        name (str)
        category (str)
        price (float)
        quantity (int)
        min_stock (int)
    """

    def __init__(self, product_id, name, category, price, quantity, min_stock):
        """Initialise a new Product instance with validated attributes."""
        self.__product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.min_stock = min_stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value == "" or value.isspace():
            raise ValueError("Name cannot be empty or only whitespace.")
        self.__name = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        if value == "" or value.isspace():
            raise ValueError("Category cannot be empty or only whitespace.")
        self.__category = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = value

    @property
    def min_stock(self):
        return self.__min_stock

    @min_stock.setter
    def min_stock(self, value):
        if value < 0:
            raise ValueError("Minimum stock level cannot be negative.")
        self.__min_stock = value

    # METHODS

    def update_stock(self, amount_change):
        """
        Update the product quantity by the given amount.

        Args:
            amount_change (int): Positive to add stock, negative to remove it.

        Raises:
            ValueError: If the resulting quantity would be less than zero.
        """
        updated_stock = self.quantity + amount_change

        if updated_stock < 0:
            raise ValueError("Quantity cannot go below zero.")
        self.quantity = updated_stock

    def get_value(self):
        """Return the total monetary value of the current stock (price * quantity)."""
        return self.price * self.quantity

    def is_low_stock(self):
        """Return True if the current quantity is at or below the min_stock level."""
        if self.quantity <= self.min_stock:
            return True
        return False

    def to_dict(self):
        """Return a dictionary representation of the product, for JSON storage."""
        attributes_dictionary = {"Name": self.name, "Category": self.category, "Price": self.price, "Quantity": self.quantity, "Minimum Stock": self.min_stock}
        return attributes_dictionary

    @classmethod
    def from_dict(cls, product_id, data):
        """
        Create a new Product instance from a dictionary (e.g. loaded from JSON).

        Args:
            product_id (str)
            data (dict)

        Returns:
            Product: A new instance built from the given data.
        """
        name = data.get('Name')
        category = data.get('Category')
        price = data.get('Price')
        quantity = data.get('Quantity')
        min_stock = data.get('Minimum Stock')

        return cls(product_id, name, category, price, quantity, min_stock)

    def __str__(self):
        """Return a readable string representation of the product's details."""
        return f"{self.name} ({self.product_id}) | {self.category} | Price: €{self.price} - Quantity: {self.quantity} - Min. Stock: {self.min_stock}"