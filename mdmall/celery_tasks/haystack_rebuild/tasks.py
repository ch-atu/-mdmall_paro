from celery_tasks.main import celery_app
from goods.search_indexes import MobileIndex, ComputerIndex


@celery_app.task(name='rebuild_index')
def rebuild_index():
    # instance.reindex()
    MobileIndex().reindex()
    ComputerIndex().reindex()


