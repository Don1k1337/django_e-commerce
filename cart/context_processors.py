from .cart import Cart


# instantiating the cart and making available for all templates
# as a var - named cart
def cart(request):
    return {'cart': Cart(request)}
