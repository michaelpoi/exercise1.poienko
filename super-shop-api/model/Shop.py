import random


class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []

    def changeCustomer(self, c, address, name, dob):
        if address is not None: c.address = address
        if name is not None: c.name = name
        if dob is not None: c.dob = dob

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

    def ifNotExistsProductByName(self,name):
        for p in self.products:
            if name == p.name:
                return False
        return True
    def addProduct(self, p):
        if self.ifNotExistsProductByName(p.name):
            self.products.append(p)
            for d in self.coupons:
                if d.category == p.category:
                    p.coupons.append(d)
            return True
        return False


    def removeProduct(self, p):
        self.products.remove(p)

    def addCoupon(self, d):
        self.coupons.append(d)
        if d.isValid():
            for p in self.products:
                if p.category == d.category:
                    p.coupons.append(d)

    def getValidCoupons(self, category=None):
        valid_coupons = [d for d in self.coupons if d.isValid()]
        if category is None:
            return valid_coupons
        else:
            return [d for d in valid_coupons if d.category == category]

    def getCouponsByCategory(self, category):
        res = []
        for d in self.coupons:
            if d.category == category:
                res.append(d)
        if len(res) == 0:
            return False
        else:
            return res

    def RandomPickByCategory(self,category):
        list_cat = [item for item in self.products if item.category == category]
        return random.choice(list_cat)

    def getRecommendations(self,c):
        recos =[]
        categories = []
        for prod in c.purchase_history:
            categories.append(prod.category)
        set_categories = set(categories)
        weights = []
        for item in set_categories:
            weights.append(categories.count(item))
        weights = [item/sum(weights)*100 for item in weights]
        cat_to_rec = [i for i in random.choices(list(set_categories), weights=weights,k=10)]
        # I have done it with repetitions, because I do not have enough products to test it without repetitions
        for item in cat_to_rec:
            recos.append(self.RandomPickByCategory(item))
        return recos

    def getReorder(self):
        reorder = []
        for prod in self.products:
            if prod.CalculateT() > prod.quantity:
                reorder.append(prod)
        return reorder