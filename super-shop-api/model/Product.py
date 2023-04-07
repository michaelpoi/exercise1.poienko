import uuid
import random
import string


class Product:
    def __init__(self, name, expiry, category,price):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.expiry = expiry
        self.category = category
        self.quantity = 0
        sn = ''
        for i in random.choices((string.digits + string.ascii_uppercase), k=10):
            sn += i
        self.serial_number = sn
        self.removed_units = {}

    def changeStock(self, q,modify = True):
        if self.quantity + q < 0:
            return False
        if modify:
            self.quantity += q
        return True

    def sellProduct(self, c, q):
        if self.changeStock(-q):
            c.purchase_history.append(self)
            return True
        return False

    def removeItems(self, r, q):
        if self.changeStock(-q):
            if self.removed_units.get(r) is None:
                self.removed_units[r] = q
            else:
                self.removed_units[r] += q
            return True
        return False
