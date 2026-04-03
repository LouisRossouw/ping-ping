import uvicorn
from fastapi import FastAPI
from api.routers import system, service, ping_apps, ping_ping

class ServiceApi:
    def __init__(self, settings, scheduler=None):
        self.app = FastAPI()
        
        # Store instances in app.state for routers to access via dependencies
        self.app.state.settings = settings
        self.app.state.scheduler = scheduler

        self._include_routers()

    def _include_routers(self):
        self.app.include_router(system.router)
        self.app.include_router(service.router)
        self.app.include_router(ping_apps.router)
        self.app.include_router(ping_ping.router)

    def run(self, host="0.0.0.0", port=5005):
        uvicorn.run(self.app, host=host, port=port)
