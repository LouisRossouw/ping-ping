
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body
from typing import Optional

from lib import api_utils as api
from lib import utils as utils

load_dotenv()


class ServiceApi:
    def __init__(self, settings, scheduler=None):

        self.app = FastAPI()

        self.settings = settings
        self.scheduler = scheduler

        self._routes()

    def _routes(self):
        @self.app.get("/")
        def root():
            return {"info": f"{self.settings.name}"}

        @self.app.get("/health")
        def _health():
            return api.health(self.settings)

        @self.app.get("/logs")
        def _get_logs(lines: int = 20):
            return {"logs": self.settings.get_logs(lines)}

        @self.app.get("/config")
        def _get_config():
            return self.settings.get_config()

        @self.app.patch("/config")
        def _patch_config(data: dict = Body(...)):
            return self.settings.update_config(data)

        @self.app.get("/service/status")
        def _status_scheduler():
            return api.status_scheduler()

        @self.app.post("/service/restart")
        def _restart_scheduler():
            return api.restart_scheduler()

        @self.app.post("/service/shutdown")
        def _shutdown_scheduler():
            return api.shutdown_scheduler(self.scheduler)

        @self.app.post("/service/pause")
        def _pause_job(job_id: str = Query(None, description="Job ID to pause")):
            return api.pause_schedule(self.scheduler, job_id)

        @self.app.post("/service/resume")
        def _resume_job(job_id: str = Query(None, description="Job ID to resume")):
            return api.resume_job(self.scheduler, job_id)

        # **
        # Endpoints / Webapps / Ping apps

        @self.app.get("/ping-apps")
        def _get_ping_apps(app: Optional[str] = Query(None)):
            return api.get_ping_apps(self.settings, app)

        @self.app.get("/ping-apps/status")
        def _get_ping_apps_status(app: Optional[str] = Query(None)):
            return api.get_ping_apps_status(self.settings, app)

        @self.app.get("/ping-apps/data")
        def _get_ping_apps_data(app: str, range: str, interval: int):
            return api.get_ping_apps_data(self.settings, app, range, interval)

        @self.app.get("/ping-apps/schedules")
        def _get_schedules():
            return self.settings.schedules

        @self.app.get("/ping-apps/actions")
        def _get_actions():
            return self.settings.actions

        # --------
        # **

        # **
        # Ping Ping

        @self.app.get("/ping-ping/status")
        def _get_status_ping_ping(range: str, interval: int):
            return api.status_ping_ping(self.settings, interval, range)

        @self.app.get("/ping-ping/service-config")
        def _get_ping_ping_config():
            return self.settings.get_config()

        # -------- **

    def run(self, host="0.0.0.0", port=5005):
        uvicorn.run(self.app, host=host, port=port)
