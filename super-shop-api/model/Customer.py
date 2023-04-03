import uuid
import secrets
import string

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
    def reset_password(self,temp,new_pass):
        if temp == self.tmppass:
            self.password = new_pass
            self.tmppass = None
            return True
        return False
