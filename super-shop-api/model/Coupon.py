import random
import string
from datetime import datetime

class Coupon:
    def __init__(self,category,value, start_date, end_date):
        id = ''
        for i in random.choices(string.digits, k=10):
            id += i
        self.coupon_id = id
        self.category = category
        self.start_date = start_date
        self.end_date = end_date
        self.value = value/100

    def isValid(self):
        if self.start_date <= datetime.today() <= self.end_date:
            return True
        return False

