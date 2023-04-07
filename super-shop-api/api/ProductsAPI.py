from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.Product import Product
from model.data import my_shop

ProductAPI = Namespace('product',
                       description='Product Management')


@ProductAPI.route('/')
class AddProductA(Resource):
    @ProductAPI.doc(params={'name': 'Product name',
                            'expiry': 'expiry date',
                            'category': 'product category',
                            'price': 'product price'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        expiry = args['expiry']
        category = args['category']
        price = args['price']
        new_product = Product(name, expiry, category, price)
        # add the product
        my_shop.addProduct(new_product)
        return jsonify(new_product)

    @ProductAPI.doc(description="Get list of all products")
    def get(self):
        return jsonify(my_shop.products)


@ProductAPI.route('/<product_id>')
class SpecificProductOps(Resource):
    @ProductAPI.doc(description="Deleting an existing product")
    def delete(self, product_id):
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"Product {product_id} was not found")
        else:
            my_shop.removeProduct(p)
            return jsonify(f"Product {product_id} was removed")

    @ProductAPI.doc(description="Get data about a particular product")
    def get(self, product_id):
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"Product {product_id} was not found")
        return jsonify(p)

    @ProductAPI.doc(description="Change the stock of an existing product",
                    params={'quantity': 'Number of units delivered'})
    def put(self, product_id):
        q = int(request.args['quantity'])
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"Product {product_id} was not found")
        if q > 0:
            p.changeStock(q)
            return jsonify("Stock of product was changed")
        else:
            return jsonify("Input is not valid")


@ProductAPI.route('/sell')
class ProductSale(Resource):
    @ProductAPI.doc(description="Sell a product",
                    params={'product-id': 'ID of the sold product', 'customer-id': 'Buyers ID',
                            'quantity': 'Number of units sold'})
    def put(self):
        c = my_shop.getCustomer(request.args['customer-id'])
        p = my_shop.getProduct(request.args['product-id'])
        q = int(request.args['quantity'])
        if not c or not p:
            return jsonify("Customer id or product id is incorrect")
        if q < 1:
            return jsonify("Invalid quantity")
        if p.sellProduct(c, q):
            return jsonify('Product was sold')
        return jsonify('Shop does not have enough units of product')


@ProductAPI.route('/remove')
class RemoveProduct(Resource):
    @ProductAPI.doc(description="Remove an item from inventory",
                    params={'product-id': 'ID of the removed product', 'quantity': 'Number of removed units',
                            'reason': 'Reason of removing'})
    def put(self):
        p = my_shop.getProduct(request.args['product-id'])
        q = int(request.args['quantity'])
        r = request.args['reason']
        if not p:
            return jsonify("Product {prod-id} was not found")
        if p.removeItems(r,q):
            return jsonify("Product units were removed")
        return jsonify("Not enough products to remove them")


@ProductAPI.route('/reorder')
class ProductReorder(Resource):
    pass
