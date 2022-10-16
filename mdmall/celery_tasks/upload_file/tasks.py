from celery_tasks.main import celery_app

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'xxxxxxxxxxxxxxxxxxxx'  # 替换为用户的secret_id
secret_key = 'xxxxxxxxxxxxxxxxxxx'  # 替换为用户的secret_key
region = 'ap-nanjing'  # 替换为用户的region
token = None  # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)


@celery_app.task(name='upload_file')
def tencent_upload_file(content, file_name):
    client.put_object(
        Bucket='czy-first-1302794566',
        Body=content,
        Key=file_name,
        StorageClass='STANDARD',
        EnableMD5=False
    )
