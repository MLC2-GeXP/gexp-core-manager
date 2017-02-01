import requests

from gexp_core_api.models import Subcategory, Category, Country, Indicator
from gexp_core_api.serializers import CountrySerializer, SubcategorySerializer

base_url = 'http://52.174.33.166/gexp/'
categs_url = base_url + 'categoriesAndSubcategories'
countries_url = base_url + 'countries'
search_url = base_url + 'QueryDataApi?'

def get_categories_subcategories():
    r = requests.get(categs_url)

    Category.objects.all().delete()
    Subcategory.objects.all().delete()

    for categ in r.json():
        category = Category.objects.create(name=categ['CategoryName'])
        category.save()
        for subcateg in categ['SubcategorieList']:
            subcategory = Subcategory.objects.create(category=category, name=subcateg['SubcategoryName'])
            subcategory.save()
            for indicator in subcateg['Indicators']:
                indi = Indicator.objects.create(subcategory=subcategory, name=indicator['Indicator'])
                indi.save()


def get_countries():
    r = requests.get(countries_url)

    Country.objects.all().delete()

    for country in r.json():
        country_obj = Country.objects.create(name=country['CountryName'], dbpedia_url=country['DbpediaUrl'])
        country_obj.save()


def retrieve_countries_urls(ids_string):
    urls = []

    ids = ids_string[1:-1].split(',')
    serializer = CountrySerializer(instance=Country.objects.all(), many=True)

    for c in serializer.data:
        for id in ids:
            if id == str(c['id']):
                urls.append(c['dbpedia_url'])
    return urls

def retrieve_subcategory_name(id):

    queryset = list(Subcategory.objects.all())
    for s in queryset:
        if str(s.id) == id:
            return s.name

    return None

def retrieve_indicator_name(id):

    queryset = list(Indicator.objects.all())
    for i in queryset:
        if str(i.id) == id:
            return i.name

    return None

def retrieve_category_name(id):

    queryset = list(Category.objects.all())
    for c in queryset:
        if str(c.id) == id:
            return c.name

    return None

def search_data(params):
    countries = retrieve_countries_urls(params['countryIds'])
    countries = ','.join(map(str, countries))
    category = retrieve_category_name(params['categoryId'])
    subcategory = retrieve_subcategory_name(params['subcategoryId'])
    indicator = retrieve_indicator_name(params['indicatorId'])

    query_url = search_url + 'countryUrl=' + countries + '&subcategory=' + subcategory + \
                 '&category=' + category + '&indicator=' + indicator

    if params['time']:
        time = params['time'].split('-')
        if len(time) > 1:
            startYear = time[0]
            endYear = time[1]

            query_url += '&startYear=' + startYear + '&endYear=' + endYear

    print('URL:' + query_url)
    r = requests.get(query_url)

    if r.status_code == 500:
        return None


    if r.status_code == 404:
        return None

    years = []
    country_values = {}
    for datamodel in r.json():

        if not datamodel['Year'] in years:
            years.append(datamodel['Year'])
        country_name = datamodel['Country']['CountryName']

        if country_name in country_values:
            country_values[country_name].append(datamodel['Value'])
        else:
            country_values[country_name] = []

    chartDatas = serialize_chart_data(country_values, years)

    response = {
        'lineChartData' : chartDatas,
        'geoChartData' : chartDatas,
        'recommendation' : [],
    }

    return response

def serialize_chart_data(country_values, years):
    datasets = []
    for country_name, values in country_values.items():
        objc = {
            'country_name': country_name,
            'data': values
        }
        datasets.append(objc)

    chartDatas = {
        'years': years,
        'datasets': datasets
    }

    return chartDatas

#
# chartDatas = {
#     'years' : [1950, 1960, 1970, 1980, 1990, 2000],
#     'datasets' : [
#         {
#             'country_name' : 'Germany',
#             'data' : [1.2, 2.5, 5.2, 100, 102, 104.4]
#         },
#         {
#             'country_name' : 'Brazil',
#             'data' : [2.2, 3.5, 4.2, 105, 106, 107.8]
#         },
#         {
#             'country_name' : 'USA',
#             'data' : [10.2, 20.5, 50.2, 100, 12, 104]
#         }
#     ]
# }
# response = {
#     'lineChartData' : chartDatas,
#     'geoChartData' : chartDatas,
#     'recommendation' : [],
# }
