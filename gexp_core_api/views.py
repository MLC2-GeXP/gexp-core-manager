from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from gexp_core_api import serializers
from gexp_core_api.model_definitions.definitions import Category, Subcategory, Country, Population

chartDatas = {

    1: {
        'years' : [1950, 1960, 1970, 1980, 1990, 2000],
        'datasets' : [
            {
                'country_name' : 'Germany',
                'data' : [1.2, 2.5, 5.2, 100, 102, 104.4]
            },
            {
                'country_name' : 'Brazil',
                'data' : [2.2, 3.5, 4.2, 105, 106, 107.8]
            },
            {
                'country_name' : 'USA',
                'data' : [10.2, 20.5, 50.2, 100, 12, 104]
            }
        ]
    }
}
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
initialData = {
    1: {
        'countries' : [
            Country(id=1, name='Germany'),
            Country(id=2, name='USA'),
            Country(id=3, name='Brazil')
        ],
        'categories': [
            Category(id=1, name='Health', subcategories=[
                    Subcategory(id=11, name='Healthy subcategory1'),
                    Subcategory(id=12, name='Healthy subcategory2'),
                    Subcategory(id=13, name='Healthy subcategory3')
                ]),
            Category(id=2, name='Education', subcategories=[
                    Subcategory(id=22, name='Education subcategory')
                ]),
            Category(id=3, name='Living standards', subcategories=[
                    Subcategory(id=33, name='Living subcategory')
                ])
        ],
        'population': [
            Population(id=1, gender='Male'),
            Population(id=2, gender='Female'),
            Population(id=3, gender='All')
        ]
    }
}


class SearchView(APIView):
    '''
    Get data after applying filters(category/country/population/dates).
    '''
    def get(self, request, *args, **kwargs):
        '''
        Handles the GET request
        /search/{subcategoryId}/{populationId}/?countryIds=[1,2,3,4,5]&time={fromYear}-{toYear}
        '''

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


class DataView(APIView):
    '''
    Creating new data for specific subcategory && country && year using a form or upload a csv/xls file.
    \n When uploading an csv/xls file : if the subcategory does not exists, it gets created.

    '''

    def put(self, request, *args, **kwargs):
        '''
        Handles the PUT request to update data.
        /data
        '''
        if request.FILES:
            print('file: ' + request.FILES[file])
        else:
            print(request.data)

        return Response(request.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        '''
        Handles the POST request to create new data.
        /data
        '''
        if request.FILES:
            print('file: ' + request.FILES[file])
        else:
            print(request.data)

        return Response(request.data, status=status.HTTP_201_CREATED)


    def delete(self, request, *args, **kwargs):
        '''
        Handles the POST request to create new data.
        /data
        '''

        return Response(request.data, status=status.HTTP_200_OK)


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


class ChartDataViewSet(viewsets.ViewSet):
    serializer_class = serializers.ChartDataSerializer

    def list(self, request):
        serializer = serializers.ChartDataSerializer(instance=chartDatas.values(), many=True)
        return Response(serializer.data)


class InitialDataViewSet(viewsets.ViewSet):
    serializer_class = serializers.InitialDataSerializer

    def list(self, request):
        serializer = serializers.InitialDataSerializer(instance=initialData.values(), many=True)
        return Response(serializer.data)