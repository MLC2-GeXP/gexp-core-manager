"""gexp_core_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from gexp_core_api.views import CategoryViewSet, CountryViewSet, SearchView, DataView, ChartDataViewSet, \
    InitialDataViewSet

router = routers.DefaultRouter()
router.register(r'initialdata', InitialDataViewSet, base_name='initial data')
router.register(r'categories', CategoryViewSet, base_name='categories')
router.register(r'countries', CountryViewSet, base_name='countries')
router.register(r'chartdata', ChartDataViewSet, base_name='chartdata')

urlpatterns = router.urls + [
    url(r'^admin/', admin.site.urls),

    # this URL passes resource_id in **kw to SearchView
    # /search/{subcategoryId}/{populationId}/?countryIds=[1,2,3,4,5]&time={fromYear}-{toYear}
    url(r'^search/(?P<subcategoryId>\d+)/(?P<populationId>\d+)[/]?$', SearchView.as_view(), name='search'),
    url(r'^search[/]?$', SearchView.as_view(), name='search'),
    url(r'^data[/]?$', DataView.as_view(), name='data'),
    url(r'^data/upload[/]?$', DataView.as_view(), name='data'),
]
