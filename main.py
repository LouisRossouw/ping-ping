from lib.settings import Settings
from lib.api import ServiceApi
from lib.scheduler import TaskScheduler
from lib.runner import run_action

settings = Settings()
scheduler = TaskScheduler(settings, run_action)
server = ServiceApi(settings, scheduler=scheduler)


@server.app.on_event("startup")
def start_scheduler():
    print(f"Starting {settings.name} Scheduler...")
    scheduler.start()


if __name__ == "__main__":
    server.run(host=settings.host, port=settings.port)
