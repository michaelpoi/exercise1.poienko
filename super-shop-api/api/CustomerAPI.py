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
    def put(self, customer_id):     #upd   (seems like it works properly)
        args = request.args
        if my_shop.changeCustomer(customer_id, args['address'], args['name'], args['dob']):
            return jsonify("Data has been changed", args)
        else:
            return jsonify("Customer has not been found")

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
        if c.reset_password(temp,new_pw):
            return jsonify(f"Customer`s {customer_id} password was changed")
        else:
            return jsonify("Temporary password is incorrect")




