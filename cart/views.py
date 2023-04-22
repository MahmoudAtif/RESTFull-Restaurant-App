from rest_framework import status, viewsets
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from order.models import Order, OrderItem
from order.serializers import OrderDetailSerializer, CheckoutInputSerializer
from django.db import transaction
from users.custom_token_authentication import CustomTokenAuthentication
# Create your views here.


class CartViewset(viewsets.GenericViewSet):

    serializer_class = serializers.CartSerializer

    def get_object(self):
        cart, created = models.Cart.objects.get_or_create(
            user=self.request.user
        )
        return cart

    def list(self, request, *args, **kwargs):
        """Cart View"""
        cart = self.get_object()
        serializer = self.get_serializer(cart, many=False)
        return Response(
            {
                'code': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
    )
    def add(self, request, *args, **kwargs):
        """Add to cart"""
        serializer = serializers.AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get data
        restaurant = serializer.validated_data['restaurant']
        item = serializer.validated_data['item']
        quantity = serializer.validated_data.get('quantity', 0)
        # get cart item
        cart = self.get_object()
        item_in_cart = cart.items.filter(
            restaurant=restaurant, item=item
        ).first()

        quantity_in_cart = getattr(item_in_cart, 'quantity', 0)
        total_quantity = quantity_in_cart + quantity

        if item_in_cart:
            item_in_cart.quantity = total_quantity
            item_in_cart.save()
        else:
            models.CartItem.objects.create(
                cart=cart,
                restaurant=restaurant,
                item=item,
                quantity=total_quantity
            )
        return Response(
            {
                'code': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path=r"items/(?P<pk>[^/.]+)/remove",
    )
    def remove(self, *args, **kwargs):
        """remove cart item"""
        cart = self.get_object()
        pk = kwargs.get('pk')
        cart_item = cart.items.filter(pk=pk).first()
        self.check_cart_item(cart_item)
        cart_item.delete()
        return Response(
            {
                'code': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path=r'items/(?P<pk>[^/.]+)/update-quantity'
    )
    def update_quantity(self, request, *args, **kwargs):
        serializer = serializers.UpdateCartItemQuantity(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_object()
        pk = kwargs.get('pk')
        quantity = serializer.validated_data.get('quantity')
        cart_item = cart.items.filter(pk=pk).first()
        # return exception if not found
        self.check_cart_item(cart_item)

        # update
        cart_item.quantity = quantity
        cart_item.save()
        return Response(
            {
                'code': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        methods=['POST'],
        detail=False,
        authentication_classes=[CustomTokenAuthentication]
    )
    def checkout(self, *args, **kwargs):
        input_serializer = CheckoutInputSerializer(data=self.request.data)
        input_serializer.is_valid(raise_exception=True)

        cart = self.get_object()
        cart_items = cart.items.select_related('item')

        if not cart_items:
            return Response(
                {
                    'code': 'Empty Cart',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        restaurant = cart.items.select_related('item').first().restaurant

        # create order
        order = Order.objects.create(
            user=self.request.user,
            restaurant=restaurant,
            state=input_serializer.validated_data.get('state'),
            city=input_serializer.validated_data.get('city'),
            description=input_serializer.validated_data.get('description'),
            price=cart.sub_total,
            total_price=cart.total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=item.item,
                quantity=item.quantity,
                price=item.item.price
            )
        cart.clear()
        serializer = OrderDetailSerializer(order)
        return Response(
            {
                'code': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
    )
    def clear(self, *args, **kwargs):
        """clear all cart and cart items"""
        self.get_object().clear()
        return Response(
            {
                'code': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    def check_cart_item(self, cart_item):
        if not cart_item:
            raise NotFound(
                {
                    'code': 'Not Found'
                }
            )
        return True
