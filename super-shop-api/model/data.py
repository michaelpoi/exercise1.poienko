# the instance of shop, where all data is stored.
from datetime import datetime

from model.Customer import Customer
from model.Shop import Shop
from model.Product import Product
from model.Coupon import Coupon
my_shop = Shop()

# Test data
c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
c1.customer_id = "c1"
my_shop.addCustomer(c1)
p1 = Product("Apple", "09.04.2023", "fruits",1.20)
p2 = Product("TV", "05.06.2023", "electronics", 150)
p1.product_id = "p1"
p2.product_id = "p2"
p1.changeStock(100)
p2.changeStock(10)
c1.add2cart(p1,20)
c1.add2cart(p2,1)
c1.createOrder("Wolf street, 5b")
date_format = '%d.%m.%Y'
d1 = Coupon("electronics", 15,datetime.strptime("07.04.2023", date_format), datetime.strptime("10.04.2023", date_format))
my_shop.addProduct(p1)
my_shop.addProduct(p2)
my_shop.addCoupon(d1)