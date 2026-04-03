from fastapi import APIRouter, Depends, Request, Query
from api import api_utils as api

router = APIRouter(prefix="/service")

def get_scheduler(request: Request):
    return request.app.state.scheduler

@router.get("/status")
def _status_scheduler():
    return api.status_scheduler()

@router.post("/restart")
def _restart_scheduler():
    return api.restart_scheduler()

@router.post("/shutdown")
def _shutdown_scheduler(scheduler=Depends(get_scheduler)):
    return api.shutdown_scheduler(scheduler)

@router.post("/pause")
def _pause_job(job_id: str = Query(None, description="Job ID to pause"), scheduler=Depends(get_scheduler)):
    return api.pause_schedule(scheduler, job_id)

@router.post("/resume")
def _resume_job(job_id: str = Query(None, description="Job ID to resume"), scheduler=Depends(get_scheduler)):
    return api.resume_job(scheduler, job_id)
