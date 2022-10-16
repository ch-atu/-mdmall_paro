from django.utils import timezone
from haystack import indexes
from .models import MobileGoods, ComputerGoods


class MobileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr="name")
    price = indexes.FloatField(model_attr="price")
    category_id = indexes.IntegerField(model_attr='category_id')
    image = indexes.EdgeNgramField()
    category_name = indexes.EdgeNgramField()
    specification = indexes.EdgeNgramField()

    @staticmethod
    def prepare_category_name(obj):
        return obj.category.name

    @staticmethod
    def prepare_image(obj):
        return obj.image.url

    @staticmethod
    def prepare_specification(obj):
        specification_list = []
        if obj.specification_1:
            specification_1 = '+'.join(
                [obj.specification_1.run_memory, obj.specification_1.storage, obj.specification_1.color])
            specification_list.append(specification_1)
        if obj.specification_2:
            specification_2 = '+'.join(
                [obj.specification_2.run_memory, obj.specification_2.storage, obj.specification_2.color])
            specification_list.append(specification_2)
        if obj.specification_3:
            specification_3 = '+'.join(
                [obj.specification_3.run_memory, obj.specification_3.storage, obj.specification_3.color])
            specification_list.append(specification_3)
        specification = '/'.join(specification_list)
        return specification

    def get_model(self):
        return MobileGoods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ComputerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr="name")
    price = indexes.FloatField(model_attr="price")
    category_id = indexes.IntegerField(model_attr='category_id')
    image = indexes.EdgeNgramField()
    category_name = indexes.EdgeNgramField()
    specification = indexes.EdgeNgramField()

    @staticmethod
    def prepare_category_name(obj):
        return obj.category.name

    @staticmethod
    def prepare_image(obj):
        return obj.image.url

    @staticmethod
    def prepare_specification(obj):
        specification_list = []
        if obj.specification_1:
            specification_1 = '+'.join(
                [obj.specification_1.size, obj.specification_1.run_memory, obj.specification_1.storage,
                 obj.specification_1.color])
            specification_list.append(specification_1)
        if obj.specification_2:
            specification_2 = '+'.join(
                [obj.specification_2.size, obj.specification_2.run_memory, obj.specification_2.storage,
                 obj.specification_2.color])
            specification_list.append(specification_2)
        if obj.specification_3:
            specification_3 = '+'.join(
                [obj.specification_3.size, obj.specification_3.run_memory, obj.specification_3.storage,
                 obj.specification_3.color])
            specification_list.append(specification_3)
        specification = '/'.join(specification_list)
        return specification

    def get_model(self):
        return ComputerGoods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
