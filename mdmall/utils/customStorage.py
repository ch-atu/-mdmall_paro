from django.core.files.storage import Storage
import random
import string
from celery_tasks.upload_file.tasks import tencent_upload_file


class TencentStorage(Storage):
    def __init__(self):
        pass

    def _open(self, name):
        pass

    def _save(self, name, content):
        random_name = ''.join(random.sample(string.ascii_letters + string.digits, 50))
        file_name = 'mdmall/images/goods/' + random_name + '.jpg'
        tencent_upload_file(content, file_name)
        return file_name

    def url(self, name):
        return 'https://czy-first-1302794566.cos.ap-nanjing.myqcloud.com/' + name

    def exists(self, name):
        return False
