from django.conf import settings
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductRecommendSerializer,
)


class NoneInfoPagination(PageNumberPagination):
    # count, next, previous 를 제외하고 보여주기
    def get_paginated_response(self, data):
        return Response(data)


class ProductList(ListAPIView):

    """ Product List Definition """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = NoneInfoPagination

    def get_queryset(self):
        skin_type = self.request.query_params.get("skin_type", None)

        # 피부타입(내림차순) & 가격(오름차순) 정렬
        if skin_type is None:
            products = Product.objects.all()
        else:
            products = Product.objects.skin_type(skin_type)

        # 카테고리 필터
        category = self.request.query_params.get("category", None)

        if category is not None:
            products = products.filter(category__name=category)

        # 제외 성분 필터
        exclude_ingredients = self.request.query_params.get("exclude_ingredient", None)

        if exclude_ingredients is not None:
            exclude_ingredients = exclude_ingredients.split(",")
            for exclude in exclude_ingredients:
                products = products.exclude(ingredients__name=exclude)

        # 포함 성분 필터
        include_ingredients = self.request.query_params.get("include_ingredient", None)

        if include_ingredients is not None:
            include_ingredients = include_ingredients.split(",")
            for include in include_ingredients:
                products = products.filter(ingredients__name=include)

        return products


class ProductDetail(RetrieveAPIView):

    """ Product Detail Definition """

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        recommend_num = getattr(settings, "RECOMMEND_NUM")

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        skin_type = self.request.query_params.get("skin_type", None)
        # 피부타입(내림차순) & 가격(오름차순) 정렬
        if skin_type is None:
            products = Product.objects.all()
        else:
            products = Product.objects.skin_type(skin_type)

        products = products.exclude(id=instance.id)  # 자신은 추천 대상에서 제외
        products = products[:recommend_num]

        recommandation = ProductRecommendSerializer(products, many=True)

        return Response([serializer.data, *recommandation.data])
