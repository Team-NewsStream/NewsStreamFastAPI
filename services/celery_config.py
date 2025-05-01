from celery import Celery

from core.settings import settings

celery_app = Celery(
    "news_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["services.tasks"]  # Tasks will live here
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_default_queue="news_queue",
    task_track_started=True,  # To see when retries begin
    task_annotations={
        'services.tasks.fetch_and_save_news': {
            'max_retries': 3,
            'retry_backoff': True,
            'retry_backoff_max': 180,  # Max 3 minutes between retries
            'retry_jitter': True,
        }
    },
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=25
)
