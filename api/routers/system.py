from fastapi import APIRouter, Depends, Request, Body
from api import api_utils as api

router = APIRouter()

def get_settings(request: Request):
    return request.app.state.settings

@router.get("/")
def root(settings=Depends(get_settings)):
    return {"info": f"{settings.name}"}

@router.get("/health")
def _health(settings=Depends(get_settings)):
    return api.health(settings)

@router.get("/logs")
def _get_logs(request: Request, lines: int = 20):
    return {"logs": request.app.state.settings.get_logs(lines)}

@router.get("/config")
def _get_config(settings=Depends(get_settings)):
    return settings.get_config()

@router.patch("/config")
def _patch_config(data: dict = Body(...), settings=Depends(get_settings)):
    return settings.update_config(data)
