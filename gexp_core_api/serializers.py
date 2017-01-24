from rest_framework import serializers

from gexp_core_api.model_definitions.definitions import Category, Subcategory, Datasets, ChartData


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


class SubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Subcategory(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    subcategories = SubcategorySerializer(many=True)

    def create(self, validated_data):
        return Category(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance




class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Category(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance