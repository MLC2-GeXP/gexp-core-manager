from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from gexp_core_api import serializers
from gexp_core_api.model_definitions.definitions import Category, Subcategory, Country

categories = {
    1: Category(id=1, name='Health', subcategories=[
        Subcategory(id=11, name='Healthy subcategory1'),
        Subcategory(id=12, name='Healthy subcategory2'),
        Subcategory(id=13, name='Healthy subcategory3')
    ]),
    2: Category(id=2, name='Education', subcategories=[
        Subcategory(id=22, name='Education subcategory')
    ]),
    3: Category(id=3, name='Living standards', subcategories=[
        Subcategory(id=33, name='Living subcategory')
    ])
}
countries = {
    1: Country(id=1, name='Germany'),
    2: Country(id=2, name='USA'),
    3: Country(id=3, name='Brazil')
}


class SearchView(APIView):
    '''
    /search/{subcategoryId}/{populationId}/?countryIds=[1,2,3,4,5]&time={fromYear}-{toYear}
    '''
    def get(self, request, *args, **kwargs):

        get_arg1 = request.GET.get('countryIds', None)
        get_arg2 = request.GET.get('time', None)

        print(get_arg1)
        print(get_arg2)
        print(kwargs['subcategoryId'], kwargs['populationId'])

        result = {
            "countryIds" : get_arg1,
            "time" : get_arg2,
            "subcategoryId": kwargs['subcategoryId'],
            "populationId" : kwargs['populationId']
        }
        return Response(result, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ViewSet):
    '''
    Categories
    '''

    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.CategorySerializer

    def list(self, request):
        '''On GET request'''
        serializer = serializers.CategorySerializer(instance=categories.values(), many=True)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.SubcategorySerializer

    def list(self, request):
        serializer = serializers.SubcategorySerializer(instance=categories.values(), many=True)
        return Response(serializer.data)


class CountryViewSet(viewsets.ViewSet):
    '''
    Countries
    '''

    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.CountrySerializer

    def list(self, request):
        '''On GET request'''
        serializer = serializers.CountrySerializer(instance=countries.values(), many=True)
        return Response(serializer.data)