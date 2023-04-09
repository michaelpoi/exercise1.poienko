from datetime import datetime, timedelta
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
        self.coupons = []
        self.discount = 0
        self.saled_units = []

    def changeStock(self, q,modify = True):
        if self.quantity + q < 0:
            return False
        if modify:
            self.quantity += q
        return True

    def sellProduct(self, c, q):
        if self.changeStock(-q):
            c.purchase_history.append(self)
            self.saled_units.append((datetime.today(), q))
            return True
        return False

    def CalculateT(self):
        t = 0
        for item in self.saled_units:
            if item[0] >= datetime.today() - timedelta(days=7):
                t += item[1]
        return t
    def removeItems(self, r, q):
        if self.changeStock(-q):
            if self.removed_units.get(r) is None:
                self.removed_units[r] = q
            else:
                self.removed_units[r] += q
            return True
        return False

    def ValidateCoupons(self):
        coupons = list.copy(self.coupons)
        for d in coupons:
            if not d.isValid():
                self.coupons.remove(d)

    def CalculateDiscount(self):
        self.ValidateCoupons()
        total = 0
        for d in self.coupons:
            total += d.value
        self.discount = total