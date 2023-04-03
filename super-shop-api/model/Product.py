import uuid


class Product:
    def __init__(self, name, expiry, category ):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.expiry = expiry
        self.category = category
        self.quantity = 0
