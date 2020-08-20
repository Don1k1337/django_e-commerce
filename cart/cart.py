from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """
        # storing current session
        self.session = request.session
        # getting the cart from the current session
        cart = self.session.get(settings.CART_SESSION_ID)
        # if no cart is present, create an empty cart using dict in session
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get
        the products from the DB.
        :param self:
        :return:
        """
        product_ids = self.cart.keys()
        # get the product obj and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        # Iterating using a generator
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # returning the sum of qty in the cart
    def __len__(self):
        """
        Count all existing items in the cart.
        :param self:
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its qty
        :param product:
        :param quantity:
        :param override_quantity:
        :return:
        """
        product_id = str(product.id)
        # using dict for JSON to serialize session data, cause
        # JSON only allows str key names
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as 'modified' to make sure it gets saved
        self.session.modified = True

        # removing a given product from the cart dict
        # and calling the save() method to upd the cart in the session
    def remove(self, product):
        """
        Remove a product from the cart
        :param self:
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # calc the costs of the items in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

