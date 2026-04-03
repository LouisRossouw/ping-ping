from fastapi import APIRouter, Depends, Request, Query
from typing import Optional
from api import api_utils as api

router = APIRouter(prefix="/ping-apps")

def get_settings(request: Request):
    return request.app.state.settings

@router.get("/")
def _get_ping_apps(app: Optional[str] = Query(None), settings=Depends(get_settings)):
    return api.get_ping_apps(settings, app)

@router.get("/status")
def _get_ping_apps_status(app: Optional[str] = Query(None), settings=Depends(get_settings)):
    return api.get_ping_apps_status(settings, app)

@router.get("/data")
def _get_ping_apps_data(app: str, range: str, interval: int, settings=Depends(get_settings)):
    return api.get_ping_apps_data(settings, app, range, interval)

@router.get("/schedules")
def _get_schedules(settings=Depends(get_settings)):
    return settings.schedules

@router.get("/actions")
def _get_actions(settings=Depends(get_settings)):
    return settings.actions
