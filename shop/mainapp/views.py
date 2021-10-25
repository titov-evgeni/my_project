from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import View, DetailView
from django.contrib.contenttypes.models import ContentType
from .forms import UserRegistrationForm
from .mixins import CartMixin

from .models import (
    ProductsForMainPage,
    Smartphone,
    Notebook,
    Customer,
    Cart,
    CartProduct,
)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',
                  {'user_form': user_form})


class BaseView(View):

    @staticmethod
    def get(request):
        products = ProductsForMainPage.get_products_for_main_page(
            'notebook', 'smartphone',
        )
        return render(request, 'base.html', {'products': products, })


class ProductDetailView(DetailView):
    CT_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CartView(CartMixin, View):

    @staticmethod
    def get(request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        return render(request, 'cart.html', {'cart': cart, })


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id,
            final_price=product.price)
        self.cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner,
                                               cart=self.cart,
                                               content_type=content_type,
                                               object_id=product.id,
                                               final_price=product.price)
        self.cart.products.remove(cart_product)
        return HttpResponseRedirect('/cart/')

# class AddToCartSmartphone(View):
#
#     @staticmethod
#     def get(request, *args, **kwargs):
#         product_slug = kwargs.get('slug')
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer)
#         content_type = ContentType.objects.get(model='smartphone')
#         product = content_type.model_class().objects.get(slug=product_slug)
#         cart_product, created = CartProduct.objects.get_or_create(
#             user=cart.owner,
#             cart=cart,
#             content_type=content_type,
#             object_id=product.id,
#             final_price=product.price)
#         cart.products.add(cart_product)
#         return HttpResponseRedirect('/cart/')
#
#
# class DelFromCartSmartphone(View):
#
#     @staticmethod
#     def get(request, *args, **kwargs):
#         product_slug = kwargs.get('slug')
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer)
#         content_type = ContentType.objects.get(model='smartphone')
#         product = content_type.model_class().objects.get(slug=product_slug)
#         cart_product = CartProduct.objects.get(user=cart.owner,
#                                                cart=cart,
#                                                content_type=content_type,
#                                                object_id=product.id,
#                                                final_price=product.price)
#         cart.products.remove(cart_product)
#         return HttpResponseRedirect('/cart/')
