from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from users.models import Favorite
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
# Create your views here.


class RestaurantViewSet(viewsets.GenericViewSet, generics.ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.ResturantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['name']
    search_fields = ['name', 'description']

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().prefetch_related(
            'groups', 'groups__items', 'groups__items__variants'
        ).filter(pk=pk).first()
        self.check_instance(instance)
        serializer = serializers.ResturantDeatilSerializer(instance)
        return Response(
            {
                'code': 'Success',
                'data': serializer.data
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        detail=True,
        authentication_classes=[TokenAuthentication],
        permission_classes=[IsAuthenticated],
        url_path=r'items/(?P<item_pk>[^/.]+)/favorite'
    )
    def favorite(self, request, pk, *args, **kwargs):
        """action for add item into user favorite"""
        instance = self.get_queryset().filter(pk=pk).first()
        self.check_instance(instance)
        item_pk = kwargs.get('item_pk')
        item = instance.items.filter(pk=item_pk, status=True).first()
        if not item:
            return Response(
                {
                    'code': 'Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.items.add(item)
        return Response(
            {
                'code': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        authentication_classes=[TokenAuthentication],
        permission_classes=[IsAuthenticated],
        url_path=r'items/(?P<item_pk>[^/.]+)/unfavorite'

    )
    def unfavorite(self, request, pk, *args, **kwargs):
        """action for remove item from user favorite"""
        instance = self.get_queryset().filter(pk=pk).first()
        self.check_instance(instance)
        item_pk = kwargs.get('item_pk')
        item = instance.items.filter(pk=item_pk, status=True).first()
        if not item:
            return Response(
                {
                    'code': 'Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.items.remove(item)
        return Response(
            {
                'code': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        authentication_classes=[TokenAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def review(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().prefetch_related(
            'groups', 'groups__items', 'groups__items__variants'
        ).filter(pk=pk).first()
        self.check_instance(instance)

        serializer = serializers.ReviewInputsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comment']
        rating = serializer.validated_data['rating']

        review_object = models.Review.objects.filter(
            restaurant=instance, user=request.user
        ).first()
        if review_object:
            return Response(
                {
                    'code': 'already reviewd'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create Review
        models.Review.objects.create(
            restaurant=instance,
            user=request.user,
            comment=comment,
            rating=rating
        )
        return Response(
            {
                'code': 'SUCCESS'
            },
            status=status.HTTP_201_CREATED
        )

    def check_instance(self, instance):
        if not instance:
            raise NotFound(
                {
                    'code': 'Not Found'
                }
            )
        return True
