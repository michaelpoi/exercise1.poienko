class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []

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
        return False

    def addProduct(self, p):
        self.products.append(p)

    def removeProduct(self, p):
        self.products.remove(p)

    def addCoupon(self, d):
        self.coupons.append(d)

    def getValidCoupons(self):
        return [d for d in self.coupons if d.isValid()]

    def getCouponsByCategory(self, category):
        res = []
        for d in self.coupons:
            if d.category == category:
                res.append(d)
        if len(res) == 0:
            return False
        else:
            return res
