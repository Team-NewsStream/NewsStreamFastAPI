import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from services.gcloud_oidc_auth import verify_internal_service_token
from services.tasks import fetch_and_save_news

router = APIRouter(tags=["Scheduler"], prefix="/v1")

logger = logging.getLogger(__name__)


@router.post(
    "/refresh-news",
    dependencies=[Depends(verify_internal_service_token)]
)
def schedule_news():
    """
    Schedules a task to fetch and save news using Celery. This endpoint
    triggers an asynchronous Celery task to retrieve and store the latest
    news articles in the database. It returns a success message and a task
    ID upon successfully queuing the task. If the task cannot be queued due
    to an error, an HTTPException is raised.

    :return: A dictionary containing a success message and the queued task’s ID
    :rtype: dict
    :raises HTTPException: If the task fails to queue, a 503 Service
        Unavailable error is raised with details about the failure.
    """
    try:
        task = fetch_and_save_news.delay()
        return {
            "message": "Task queued successfully",
            "task_id": task.id
        }
    except Exception as e:
        logger.error(f"Failed to queue task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to queue the task. Please check Celery worker status."
        )
