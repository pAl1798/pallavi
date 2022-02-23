from django import template

from djproject.ecomm.views import register



register = template.Library()


@register.filter(name = 'isexistincart')
def isexistincart(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False



@register.filter(name="cartquantity")
def cartquantity(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return False


#@register.filter(name = "total_price")
#def totral_price(product,cart):
    