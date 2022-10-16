from django.contrib import admin
from .models import ComputerSpecification, MobileSpecification, Category, Estimate, MobileGoods, ComputerGoods

from goods.search_indexes import MobileIndex, ComputerIndex
from celery_tasks.haystack_rebuild.tasks import rebuild_index

from django.core.files.base import ContentFile
# Register your models here.
class MobileGoodsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # a = open(r'C:\Users\63493\Desktop\1.jpg', mode='rb').read()
        # obj.image.save('imgfilename.jpg', ContentFile(a))
        obj.save()
        rebuild_index.delay()
        # mobile_index = MobileIndex()
        # rebuild_index.delay(mobile_index)
        # mobile_index.reindex()

    def delete_model(self, request, obj):
        obj.delete()
        rebuild_index.delay()
        # mobile_index = MobileIndex()
        # rebuild_index.delay(mobile_index)
        # mobile_index.reindex()


class ComputerGoodsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        rebuild_index.delay()
        # computer_index = ComputerIndex()
        # rebuild_index.delay(computer_index)
        # computer_index.reindex()

    def delete_model(self, request, obj):
        obj.delete()
        rebuild_index.delay()
        # computer_index = ComputerIndex()
        # rebuild_index.delay(computer_index)
        # computer_index.reindex()


admin.site.register(ComputerSpecification)
admin.site.register(MobileSpecification)
admin.site.register(Category)
admin.site.register(Estimate)
admin.site.register(MobileGoods, MobileGoodsAdmin)
admin.site.register(ComputerGoods, ComputerGoodsAdmin)
