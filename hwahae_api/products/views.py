from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class NoneInfoPagination(PageNumberPagination):
    # count, next, previous 를 제외하고 보여주기
    def get_paginated_response(self, data):
        return Response(data)


class ProductList(ListAPIView):

    """ Product List Definition """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = NoneInfoPagination


class ProductDetail(RetrieveAPIView):

    """ Product Detail Definition """

    pass
