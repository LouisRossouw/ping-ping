from core.settings import Settings
from api.api import ServiceApi
from core.scheduler import TaskScheduler
from core.runner import run_action

settings = Settings()
scheduler = TaskScheduler(settings, run_action)
server = ServiceApi(settings, scheduler=scheduler)


@server.app.on_event("startup")
def start_scheduler():
    print(f"Starting {settings.name} Scheduler...")
    scheduler.start()


if __name__ == "__main__":
    server.run(host=settings.host, port=settings.port)
