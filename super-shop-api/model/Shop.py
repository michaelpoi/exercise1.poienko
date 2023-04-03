class Shop:
    def __init__(self):
        self.customers = []
        self.products = []

    def changeCustomer(self, id, address, name, dob):
        for c in self.customers:
            if c.customer_id == id:
                c.address = address
                c.name = name
                c.dob = dob
                return True
        return False

    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:  # customer does not exist with the given email address
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, c):
        self.customers.remove(c)

    def getCustomer(self, cust_id):
        for c in self.customers:
            if c.customer_id == cust_id:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c

    # Product section
    def getProduct(self, prod_id):
        for p in self.products:
            if p.product_id == prod_id:
                return p

    def getProductbySerial(self, sn):
        for p in self.products:
            if p.serial_number == sn:
                return p

    def addProduct(self, p):
        prod = self.getProductbySerial(p.serial_number)
        if prod is None:
            self.products.append(p)
            return True
        return False
