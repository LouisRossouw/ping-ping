from fastapi import APIRouter, Depends, Request
from api import api_utils as api

router = APIRouter(prefix="/ping-ping")

def get_settings(request: Request):
    return request.app.state.settings

@router.get("/status")
def _get_status_ping_ping(range: str, interval: int, settings=Depends(get_settings)):
    return api.status_ping_ping(settings, interval, range)

@router.get("/service-config")
def _get_ping_ping_config(settings=Depends(get_settings)):
    return settings.get_config()
