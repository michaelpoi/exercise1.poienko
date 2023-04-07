from datetime import timedelta, datetime


class Order:
    def __init__(self, value, shipping_address):
        self.value = value
        self.shipping_address = shipping_address
        self.postDate = datetime.today()
        # I assume that shop delivers orders in 3 days
        self.deliveryDate = self.postDate + timedelta(days=3)
        self.price = self.calculateTotalPrice()

    def calculateTotalPrice(self):
        suma = 0
        for o in self.value:
            suma += o[0].price * o[1]
        return suma

    def isReturnable(self):
        end_date = self.deliveryDate + timedelta(days=14)
        if datetime.today() <= end_date :
            return True
        else:
            return False
