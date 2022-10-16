from rest_framework import serializers
from .models import MobileGoods, ComputerGoods

from drf_haystack.serializers import HaystackSerializer
from .search_indexes import MobileIndex, ComputerIndex


class Goods_MobilesSerializers(serializers.ModelSerializer):
    # run_memory = serializers.CharField(label='运行内存')
    # storage = serializers.CharField(label='存储容量')
    # color = serializers.CharField(label='颜色')

    class Meta:
        model = MobileGoods
        fields = ['id', 'name', 'price', 'image', 'stock', 'sales', 'category']


class Goods_MobilesDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = MobileGoods
        fields = '__all__'


class Goods_ComputerSerializers(serializers.ModelSerializer):
    class Meta:
        model = ComputerGoods
        fields = ['id', 'name', 'price', 'image', 'stock', 'sales', 'category', 'category_id']


# 创建haystack的序列化器
class GoodsSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [MobileIndex, ComputerIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = ['name', 'image', 'price', 'category_name', 'specification', 'id', 'category_id']
