from django.views.generic import View

from .models import Cart, Customer


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            customer = Customer.objects.create(
                user=request.user
            )
        cart = Cart.objects.filter(owner=customer).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
