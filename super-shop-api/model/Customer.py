import uuid
import secrets
import string
from model.Order import Order

class Customer:
    def __init__(self, name, email, address, dob):
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.email = email
        self.bonus_points = 0
        self.status = "unverified"
        self.verification_token = str(uuid.uuid4())[:5]
        self.dob = dob
        self.tmppass = None
        self.password = "Somecreativepassword123"
        self.purchase_history = []
        self.cart = []
        self.orders = []

    def verify(self, token):
        if self.verification_token == token:
            self.status = "verified"
            self.verification_token = None
        return self.status == "verified"

    def generatetmppas(self):
        pas = ""
        letters = string.ascii_letters
        signs = string.punctuation
        digits = string.digits
        alphabet = letters + digits + signs
        n = 8
        for i in range(n):
            pas += secrets.choice(alphabet)
        self.tmppass = pas

    def reset_password(self, temp, new_pass):
        if temp == self.tmppass:
            self.password = new_pass
            self.tmppass = None
            return True
        return False

    def add2cart(self, p, q):
        if p.quantity - q >= 0:
            self.cart.append((p,q))
            return True
        return False

    def removeFromCart(self, p):
        for prod in self.cart:
            if prod[0] == p:
                self.cart.remove(prod)
                return True
        return False

    @staticmethod
    def verifyPaymentData(cardNr):  # Luhn algorithm to validate creditcard
        check_sum = 0
        is_second = False
        for digit in reversed(cardNr):
            digit = int(digit)
            if is_second:
                digit *= 2
                if digit > 9:
                    digit = digit - 9
            check_sum += digit
            is_second = not is_second
        return check_sum % 10 == 0

    def createOrder(self,address):
        if len(self.cart) == 0:
            return False
        val = [item for item in self.cart]
        o = Order(val, address)
        for p in self.cart:
            p[0].sellProduct(self, p[1])
        self.orders.append(o)
        self.cart.clear()
        price = o.price
        self.bonus_points += int(price)  # I assume that shop is european one
        return True

    def Returnable(self):
        return [item for item in self.orders if item.isReturnable()]

