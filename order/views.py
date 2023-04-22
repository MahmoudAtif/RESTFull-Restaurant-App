from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.filters import SearchFilter
# Create your views here.


class OrderViewSet(viewsets.GenericViewSet, generics.ListAPIView):

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['restaurant__name']

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'restaurant'
        ).filter(user=self.request.user)
        return queryset

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().prefetch_related(
            'items'
        ).filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    'code': 'Not Found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.OrderDetailSerializer(instance)
        return Response(
            {
                'code': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
    )
    def cancel(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().prefetch_related(
            'items'
        ).filter(pk=pk).first()
        
        if not instance:
            return Response(
                {
                    'code': 'Not Found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance.status = models.Order.OrderStatusEnum.CANCELED
        instance.save()
        return Response(
            {
                'code': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )
