# test_with_pytest.py
import secrets
import string
import uuid
import requests
import pytest
from _pytest.fixtures import fixture
from datetime import datetime, timedelta
from model.Customer import Customer
from model.Shop import Shop
from model.Product import Product
from model.Order import Order
#url = 'http://127.0.0.1:7890/customer'


@fixture
def exampleCustomer1():
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    return c1


@fixture
def exampleShop(exampleCustomer1):
    shop = Shop()
    # shop.customers.append(exampleCustomer1)
    c2 = Customer("Poienko Mykhailo", "poenko.mishany@gmail.com", "Poligonna str., 10b, Dnipro", "18.03.2005")
    shop.customers.append(c2)
    c3 = Customer("Bill White", "bill,white@mail.com", "1516, New-York", "17.10.1972")
    shop.customers.append(c3)
    c4 = Customer("Tom Black", "black.tom@example.com", "3453, London", "18.12.2000")
    shop.customers.append(c4)
    p1 = Product("LG Washer", "09.04.2025", "dishwasher", 200)
    p2 = Product("Iphone 14", "09.04.2029", "smartphone", 1200)
    p3 = Product("Samsung Washer", "09.04.2026", "dishwasher", 400)
    shop.products.append(p1)
    shop.products.append(p2)
    shop.products.append(p3)
    return shop


def test_customer_add(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert exampleCustomer1 in shop.customers
    # try adding again
    shop.addCustomer(exampleCustomer1)
    assert len(shop.customers) == 1  # should be added only once


@pytest.mark.parametrize('inp, out',
                         [('', None),
                          ('0', None),
                          (str(uuid.uuid4()), None)])
def test_customer_get(exampleCustomer1, inp, out):
    shop = Shop()
    shop.customers.append(exampleCustomer1)  # adding customer without using tested above function
    id_test = exampleCustomer1.customer_id
    assert shop.getCustomer(id_test) is exampleCustomer1
    assert shop.getCustomer(inp) == out


def test_customer_delete(exampleShop):
    shop = exampleShop
    c = shop.customers[0]
    shop.removeCustomer(c)
    assert len(shop.customers) == 2
    assert c not in shop.customers


def test_update_customer(exampleShop):
    shop = exampleShop
    c = shop.customers[0]
    name = "test_name"
    address = "test_address"
    dob = "test_dob"
    shop.changeCustomer(c, address, name, dob)
    assert c.name == "test_name"
    assert c.address == "test_address"
    assert c.dob == "test_dob"
    address = "test_changed_address"
    name = "test_changed_name"
    dob = "test_changed_dob"
    shop.changeCustomer(c, address, None, None)
    assert c.address == "test_changed_address"
    assert c.name == "test_name"
    assert c.dob == "test_dob"
    shop.changeCustomer(c, None, name, None)
    assert c.address == "test_changed_address"
    assert c.name == "test_changed_name"
    assert c.dob == "test_dob"
    shop.changeCustomer(c, None, None, dob)
    assert c.address == "test_changed_address"
    assert c.name == "test_changed_name"
    assert c.dob == "test_changed_dob"
    shop.changeCustomer(c, None, None, None)
    assert c.address == "test_changed_address"
    assert c.name == "test_changed_name"
    assert c.dob == "test_changed_dob"


def test_verify(exampleShop):
    shop = exampleShop
    c = shop.customers[0]
    token = c.verification_token
    assert token is not None
    assert c.verify(token) == True
    c.status = "unverified"
    cases = ['', "00000"]
    for i in range(10): cases.append(str(uuid.uuid4())[:5])
    for case in cases:
        assert c.verify(case) == False

def generatepas():
    pas = ""
    letters = string.ascii_letters
    signs = string.punctuation
    digits = string.digits
    alphabet = letters + digits + signs
    n = 8
    for i in range(n):
        pas += secrets.choice(alphabet)
    return pas

def test_pas_reset(exampleShop):
    shop = exampleShop
    c = shop.customers[0]
    assert c.tmppass is None
    c.generatetmppas()
    tmp = c.tmppass
    assert tmp is not None
    new_pass = "test_pass"
    res = c.reset_password(tmp, new_pass)
    assert res == True and c.password == "test_pass"
    assert c.tmppass is None
    c.generatetmppas()
    tmp = c.tmppass
    new_pass = "test_2"
    cases = ["1111111111", '', None]
    for i in range(10): cases.append(generatepas())
    for case in cases:
        assert c.reset_password(case,tmp) == False
    assert c.password == "test_pass"

def test_add2cart(exampleShop):
    shop = exampleShop
    p1 = shop.products[0]
    p2 = shop.products[1]
    c1 = shop.customers[1]
    assert len(c1.cart) == 0
    p1.quantity = 10 # add some product units to unlock adding to cart possibility
    c1.add2cart(p1,5)
    assert len(c1.cart) == 1
    assert c1.cart[0] == (p1,5) # check if product is added with quantity
    assert p1.quantity == 10 # quantity of product does not have to change
    assert c1.add2cart(p1,11) == False
    p2.quantity = 7
    c1.add2cart(p2,5)
    assert len(c1.cart) == 2
    assert c1.cart[1] == (p2,5)

def test_removeFromCart(exampleShop):
    shop = exampleShop
    c1 = shop.customers[0]
    p1 = shop.products[0]
    p2 = shop.products[1]
    c1.cart.append((p1,10))
    c1.cart.append((p2,7))
    c1.removeFromCart(p1)
    assert c1.cart[0] == (p2,7)
    c1.removeFromCart(p2)
    assert len(c1.cart) == 0

@pytest.mark.parametrize('inp, out',
                         [("374245455400126", True),
                          ("111111111111111", False),
                          (	"6250941006528599", True),
                          ("01010101010101010", False)])
def test_varifyPaymentData(inp, out):
    assert Customer.verifyPaymentData(inp) == out

def test_createOrder(exampleShop):
    shop = exampleShop
    c1 = shop.customers[0]
    p1 = shop.products[0]
    p2 = shop.products[1]
    p1.quantity = 10
    p2.quantity = 100
    c1.cart.append((p1,10))
    c1.cart.append((p2,57))
    cart = c1.cart
    address = "test_address"
    c1.createOrder(address)
    assert len(c1.cart) == 0
    assert len(c1.orders) == 1
    order = c1.orders[0]
    assert order.value[0] == (p1,10) and order.value[1] == (p2,57)
    assert order.postDate == datetime.today()
    assert order.price == p1.price * 10 + p2.price*57
    assert p1.quantity == 0 and p2.quantity == 43
    assert order.shipping_address == "test_address"
    #now cart is empty
    assert c1.createOrder(address) == False
    c1.cart.append((p1,10)) # we dont have enough products
    assert c1.createOrder(address) == False
    # test if bonus points are added
    assert c1.bonus_points == int(order.price)

def test_returnable(exampleShop):
    shop = exampleShop
    c1 = shop.customers[0]
    p1 = shop.products[0]
    p2 = shop.products[1]
    o = Order([(p1,10),(p2,53)], "1671 Kiyv")
    c1.orders.append(o)
    assert len(c1.Returnable()) == 1
    o.deliveryDate = datetime.today()
    assert len(c1.Returnable()) == 1
    o.deliveryDate = datetime.today() - timedelta(days = 7)
    assert len(c1.Returnable()) == 1
    o.deliveryDate = datetime.today() - timedelta(days=14)
    assert len(c1.Returnable()) == 1
    o.deliveryDate = datetime.today() - timedelta(days=15)
    assert len(c1.Returnable()) == 0

def test_recommendations(exampleShop):
    shop = exampleShop
    c1 = shop.customers[0]
    p1 = shop.products[0]
    p2 = shop.products[1]
    c1.purchase_history.append(p1)
    c1.purchase_history.append(p2)
    recos = shop.getRecommendations(c1)
    cat1= p1.category
    cat2 = p2.category
    assert len(recos) == 10
    for p in recos:
        if p.category != cat1 and p.category != cat2:
            assert False
    rand = shop.RandomPickByCategory(cat1)
    assert rand in shop.products and rand.category == cat1







