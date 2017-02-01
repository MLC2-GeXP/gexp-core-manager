from rest_framework import serializers

from gexp_core_api.model_definitions.definitions import Datasets, ChartData, Population, \
    InitialData
from gexp_core_api.models import Subcategory, Category, Country, Indicator


class DatasetsSerializer(serializers.Serializer):
    country_name = serializers.CharField(max_length=256)
    data = serializers.ListField(child=serializers.FloatField())

    def create(self, validated_data):
        return Datasets(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class ChartDataSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField(min_value=1890))
    datasets = DatasetsSerializer(many=True)

    def create(self, validated_data):
        return ChartData(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class IndicatorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)

    class Meta:
        model = Indicator
        fields = ('id', 'name')

class SubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    indicators = IndicatorSerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ('id', 'name')


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'subcategories')


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    dbpedia_url = serializers.CharField(max_length=2000)

    class Meta:
        model = Country
        fields = ('id', 'name', 'dbpedia_url')


class PopulationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    gender = serializers.CharField(max_length=256)


    def create(self, validated_data):
        return Population(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class InitialDataSerializer(serializers.Serializer):

    categories_list = Category.objects.all()
    population_list = [
                Population(id=1, gender='Male'),
                Population(id=2, gender='Female'),
                Population(id=3, gender='All')
            ]

    categories = CategorySerializer(categories_list, many=True)
    population = PopulationSerializer(population_list, many=True)

    class Meta:
        fields = ('countries', 'categories', 'population')


    def create(self, validated_data):
        return InitialData(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

