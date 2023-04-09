from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.data import my_shop

CustomerAPI = Namespace('customer',
                        description='Customer Management')


@CustomerAPI.route('/')
class GeneralCustomerOps(Resource):

    @CustomerAPI.doc(description="Get a list of all customers")
    def get(self):
        return jsonify(my_shop.customers)

    @CustomerAPI.doc(
        description="Register a new customer",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        email = args['email']
        address = args['address']
        dob = args['dob']
        new_customer = Customer(name, email, address, dob)
        # add the customer
        if my_shop.addCustomer(new_customer):
            return jsonify(new_customer)
        else:
            return jsonify("Customer with the email address already exists")


@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(description="Get data about a particular customer")
    def get(self, customer_id):
        search_result = my_shop.getCustomer(customer_id)
        return search_result  # this is automatically jsonified by flask-restx

    @CustomerAPI.doc(description="Delete an existing customer")
    def delete(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        my_shop.removeCustomer(c)
        return jsonify("Customer with ID {cust_id} was removed")

    @CustomerAPI.doc(
        description="Update customer data",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def put(self, customer_id):  # upd   (seems like it works properly)
        try:
            name = request.args['name']
        except:
            name = None
        try: address = request.args['address']
        except: address = None
        try: dob = request.args['dob']
        except: dob = None
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer was not found")
        my_shop.changeCustomer(c, address,name,dob)
        return jsonify("Customer info was updated")


@CustomerAPI.route('/verify')
class CustomerVerficiation(Resource):
    @CustomerAPI.doc(
        description="Verify customer email address",
        params={'token': 'Verification Token sent by email',
                'email': 'Customer Email'})
    def put(self):
        args = request.args
        token = args['token']
        email = args['email']
        customer = my_shop.getCustomerbyEmail(email)
        if customer is None:
            return jsonify("Customer not found.")
        if customer.verify(token):
            return jsonify("Customer is now verified.")
        else:
            return jsonify("Invalid token.")


@CustomerAPI.route('/<customer_id>/pwreset')
class CustomerPWReset(Resource):
    @CustomerAPI.doc(
        description="Generate a temporary password and send via email.", )
    def post(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if c is not None:
            c.generatetmppas()
            return jsonify(f"On email {c.email} was sent a temporary password: {c.tmppass}")
        else:
            return jsonify("Customer was not found")

    @CustomerAPI.doc(
        description="Allow password reset based on the temporary password",
        params={'temp_pw': 'Password sent by email',
                'new_pw': 'New password'})
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if c is None:
            return jsonify("Customer was not found")
        if c.tmppass is None:
            return jsonify("Temporary password was not created before")
        temp = request.args['temp_pw']
        new_pw = request.args['new_pw']
        if c.reset_password(temp, new_pw):
            return jsonify(f"Customer`s {customer_id} password was changed")
        else:
            return jsonify("Temporary password is incorrect")


@CustomerAPI.route('/<customer_id>/add2cart')
class Add2Cart(Resource):
    @CustomerAPI.doc(description="Add an item to a shopping cart",
                     params={'product-id': 'ID of added product', 'quantity': 'Number of units added'})
    def put(self, customer_id):
        p = my_shop.getProduct(request.args['product-id'])
        c = my_shop.getCustomer(customer_id)
        q = int(request.args['quantity'])
        if not p or not c:
            return jsonify('Product {prod-id} or Customer {cust-id} was not found')
        if q == -1:
            if c.removeFromCart(p):
                return jsonify("Product {prod_id} was removed from a cart")
            return jsonify("Product {prod-id} is not in cart")
        if c.add2cart(p, q):
            return jsonify("Product {prod-id} was added to a cart")
        return jsonify("Product {prod_id} can not be added to a cart")


@CustomerAPI.route('/<customer_id>/order')
class CreateOrder(Resource):
    @CustomerAPI.doc(description="Confirm an order",
                     params={'shipping_address': 'Shipping address',
                             'cardNr': 'Credit card number'})
    def post(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        address = request.args['shipping_address']
        cardNr = request.args['cardNr']
        if not c:
            return jsonify(f"Customer {customer_id} was not found")
        if Customer.verifyPaymentData(cardNr):
            if c.createOrder(address):
                return jsonify("Order is confirmed")
            return jsonify("Cart is empty or we dont have enough units of product")
        return jsonify("Card number is invalid")


@CustomerAPI.route('/<customer_id>/orders')
class GetOrders(Resource):
    @CustomerAPI.doc(description="Return customers orders")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if c:
            return jsonify(c.orders)
        return jsonify(f"Customer {customer_id} was not found")


@CustomerAPI.route('/<customer_id>/recommendations')
class GetRecommendations(Resource):
    @CustomerAPI.doc(description = "Get a list of 10 recommendations")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer was not found")
        if len(c.purchase_hisory) == 0:
            return jsonify("Customers purchase history is empty")
        return jsonify(my_shop.getRecommendations(c))

@CustomerAPI.route('/<customer_id>/returnable')
class ReturnableOrders(Resource):
    @CustomerAPI.doc(description = "List of returnable products")
    def get(self,customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"Customer {customer_id} was not found")
        return jsonify(c.Returnable())

@CustomerAPI.route('/<customer_id>/points')
class EarnedPoints(Resource):
    @CustomerAPI.doc(description="Get customers bonus points")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if c:
            return jsonify(f"Customer {customer_id} has {c.bonus_points} bonus points so far.")
        return jsonify(f"Customer {customer_id} was not found")

    @CustomerAPI.doc(description = "Add bonus points", params = {'bonus_points' : 'Number of added bonus points'})
    def put(self, customer_id):
        n = int(request.args['bonus_points'])
        c = my_shop.getCustomer(customer_id)
        if c:
            if n>0:
                c.bonus_points += n
                return jsonify("Bonus points were added")
            return jsonify("You can add positive number only")
        return jsonify(f"Customer {customer_id} was not found")