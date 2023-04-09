import pytest
from datetime import datetime, timedelta
from _pytest.fixtures import fixture

from model.Product import Product
from model.Customer import Customer
from model.Order import Order
from model.Shop import Shop
from model.Coupon import Coupon


@fixture()
def exampleProduct1():
    p1 = Product("LG Washer", "09.04.2025", "dishwasher", 200)
    return p1


@fixture
def exampleShop():
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
    d1 = Coupon("dishwasher",0.15,'08.04.2023', '15.04.2023')
    shop.coupons.append(d1)
    shop.products.append(p1)
    shop.products.append(p2)
    shop.products.append(p3)
    return shop


def test_product_add(exampleProduct1):
    shop = Shop()
    p1 = exampleProduct1
    shop.addProduct(p1)
    assert p1 in shop.products
    shop.addProduct(p1)
    assert len(shop.products) == 1
    shop.addProduct(p1)
    assert len(shop.products) == 1


def test_sell(exampleShop):
    shop = exampleShop
    c1 = shop.customers[0]
    p1 = shop.products[0]
    p1.quantity = 10
    p1.sellProduct(c1,5)
    assert p1.quantity == 5
    assert len(c1.purchase_history) == 1
    assert len(p1.saled_units) == 1
    assert p1.sellProduct(c1,6) == False


def test_remove_product(exampleShop):
    shop = exampleShop
    p1 = shop.products[0]
    shop.removeProduct(p1)
    assert p1 not in shop.products

def test_reorder(exampleShop):
    shop = exampleShop
    p1 = shop.products[0]
    p1.saled_units.append((datetime.today(), 15))
    p1.saled_units.append((datetime.today() - timedelta(days=8), 10))
    assert p1.CalculateT() == 15
    p1.quantity = 14
    assert len(shop.getReorder()) == 1
    p1.quantity = 16
    assert len(shop.getReorder()) == 0
