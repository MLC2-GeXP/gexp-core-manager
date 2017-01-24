
class Category(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'subcategories'):
            setattr(self, field, kwargs.get(field, None))

class Subcategory(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name'):
            setattr(self, field, kwargs.get(field, None))


class Country(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name'):
            setattr(self, field, kwargs.get(field, None))

class ChartData(object):
    def __init__(self, **kwargs):
        for field in ('years', 'datasets'):
            setattr(self, field, kwargs.get(field, None))

class Datasets(object):
    def __init__(self, **kwargs):
        for field in ('country_name', 'data'):
            setattr(self, field, kwargs.get(field, None))
