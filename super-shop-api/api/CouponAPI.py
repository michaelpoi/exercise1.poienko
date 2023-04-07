from datetime import datetime

from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Coupon import Coupon
from model.data import my_shop

CouponAPI = Namespace('coupons', description='Coupons management')


@CouponAPI.route('/')
class CouponsOptions(Resource):
    @CouponAPI.doc(description="Add a new coupon", params={'category': 'Coupon category',
                                                           'value': 'Discount percentage',
                                                           'start_date': 'Start date',
                                                           'end_date': 'End date'})
    def post(self):
        date_format = '%d.%m.%Y'
        args = request.args
        category = args['category']
        value = int(args['value'])
        start_date = datetime.strptime(args['start_date'],date_format)
        end_date = datetime.strptime(args['end_date'], date_format)
        d = Coupon(category, value, start_date, end_date)
        if datetime.today() <= end_date:
            my_shop.addCoupon(d)
            return jsonify(d)
        return jsonify("Coupon with end_date < today can not be created")

    @CouponAPI.doc(desription="Get a list of all valid coupons")
    def get(self):
        return jsonify(my_shop.getValidCoupons())


