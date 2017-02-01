from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from gexp_core_api.models import Subcategory, Category, Country

from gexp_core_api import serializers
from gexp_core_api.model_definitions.definitions import Population
from gexp_core_api.services import services
from gexp_core_api.services.services import search_data


population = [
            Population(id=1, gender='Male'),
            Population(id=2, gender='Female'),
            Population(id=3, gender='All')
        ]


class DataView(APIView):
    '''
    Creating new data for specific subcategory && country && year using a form or upload a csv/xls file.
    \n When uploading an csv/xls file : if the subcategory does not exists, it gets created.

    '''
    def get(self, request, *args, **kwargs):
        '''
        Handles the GET request
        /data/{subcategoryId}/{populationId}/?countryIds=[1,2,3,4,5]&time={fromYear}-{toYear}
        '''

        get_arg1 = request.GET.get('countryIds', None)
        get_arg2 = request.GET.get('time', None)

        params = {
            "countryIds" : get_arg1,
            "time" : get_arg2,
            "subcategoryId": kwargs['subcategoryId'],
            "categoryId": kwargs['categoryId'],
            "indicatorId": kwargs['indicatorId'],
        }

        response = search_data(params)

        if response:
            return Response(response, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)

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
    queryset = Category.objects.all()

    def list(self, request):
        '''On GET request'''
        # categs = services.get_categories_subcategories()
        serializer = serializers.CategorySerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.SubcategorySerializer

    def list(self, request):
        serializer = serializers.SubcategorySerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


class CountryViewSet(viewsets.ViewSet):
    '''
    Countries
    '''

    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()

    def list(self, request):
        '''On GET request'''
        serializer = serializers.CountrySerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


class ChartDataViewSet(viewsets.ViewSet):
    serializer_class = serializers.ChartDataSerializer

    def list(self, request):
        serializer = serializers.ChartDataSerializer(instance=chartDatas.values(), many=True)
        return Response(serializer.data)


class InitialDataViewSet(viewsets.ViewSet):
    serializer_class = serializers.InitialDataSerializer

    def list(self, request):
        categories_list = Category.objects.all()
        population_list = [
            Population(id=1, gender='Male'),
            Population(id=2, gender='Female'),
            Population(id=3, gender='All')
        ]

        initialData = {
            'categories' : categories_list,
            'population' : population_list
        }

        serializer = serializers.InitialDataSerializer(instance=initialData)
        return Response(serializer.data)