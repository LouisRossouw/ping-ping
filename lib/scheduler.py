from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)


class TaskScheduler:

    def __init__(self, settings, run_action):

        self.settings = settings
        self.run_action = run_action
        self.scheduler = BackgroundScheduler()

    def start(self):

        schedules = self.settings.schedules

        for schedule in schedules:

            logging.info("Scheduling job: %s", schedule["name"])

            trigger = schedule["trigger"]

            if trigger == "cron":

                self.scheduler.add_job(
                    self.run_action,
                    "cron",
                    hour=schedule.get("hour"),
                    minute=schedule.get("minute"),
                    day_of_week=schedule.get("day_of_week"),
                    args=[self.settings, schedule["action"]],
                    id=schedule["name"]
                )

            elif trigger == "interval":

                interval_args = {}

                for key in ["seconds", "minutes", "hours", "days"]:
                    if schedule.get(key) is not None:
                        interval_args[key] = schedule[key]

                self.scheduler.add_job(
                    self.run_action,
                    "interval",
                    args=[self.settings, schedule["action"]],
                    id=schedule["name"],
                    **interval_args
                )

        logger.info("Starting scheduler")
        self.scheduler.start()
