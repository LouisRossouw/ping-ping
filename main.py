import os
import sys
import requests
import schedule
from time import sleep

import lib.utils as utils
import lib.save_data as save_data

root_dir = os.path.dirname(__file__)
sys.path.append(root_dir)

global settings


def run():
    """  Run. """

    global settings
    has_started = False
    schedule.every(settings.get('interval_min')).minutes.do(ping_apps)

    while True:

        settings = utils.read_json(os.path.join(root_dir, "configs", "main.json"))  # nopep8

        start_time = utils.start_time()
        schedule.run_pending()
        res_time = utils.calculate_request_time(start_time)

        data = {
            "res_time": res_time,
            "last_pinged": str(utils.get_dates_new()['date_now_full'])
        }

        if has_started:
            # This data is saved every 120 seconds;
            # the data is used in another app to determine if Mr Ping Ping is still active.
            save_data.save_data(None, "mr_ping_ping", data)

        has_started = True
        sleep(120)


def ping_ping(to_ping):
    """ Does a ping and returns response + data. """

    start_time = utils.start_time()

    if to_ping:
        try:
            response = requests.get(to_ping, timeout=settings.get('timeout'))
        except requests.RequestException:
            response = False

    res_time = utils.calculate_request_time(start_time)
    return response, res_time


def ping_apps():
    """ Pings apps and their given endpoints. """

    apps = utils.read_json(os.path.join(root_dir, 'configs/ping-apps.json'))

    if utils.is_internet_available():
        for app in apps:

            slug = app.get('slug')
            notify = app.get('notify')
            to_ping = app.get('active')
            base_url = app.get('base_url')
            endpoints = app.get('endpoints')

            is_endpoints = len(endpoints) > 0

            if to_ping:
                if is_endpoints:

                    endpoints_res = []
                    for endpoint in endpoints:

                        url_to_ping = f"{base_url}{endpoint}"
                        res, res_time = ping_ping(url_to_ping)
                        code = res.status_code if res else 500
                        success = code == 200

                        print_Status(slug, success, code, res_time)
                        report(app, code) if notify and not success else None

                        data = {
                            "endpoint": endpoint,
                            "full_url": url_to_ping,
                            "res_time": res_time,
                            "response": {
                                "code": code,
                                "success": success,
                                "data": res.json() if success else None
                            }
                        }

                        endpoints_res.append(data)

                    date_time = utils.get_dates_new()['date_now_full']
                    data = {
                        "date_time": str(date_time),
                        "pinged": app.get('slug'),
                        "success": success,
                        "endpoints_res": endpoints_res
                    }
                    save_data.save_data(slug, "pings", data)
                    sleep(1)

                else:
                    url_to_ping = f"{base_url}"
                    res, res_time = ping_ping(url_to_ping)
                    code = res.status_code if res else 500
                    success = code == 200

                    print_Status(slug, success, code, res_time)
                    report(app, code) if notify and not success else None

                    data = {
                        "endpoint": None,
                        "full_url": url_to_ping,
                        "res_time": res_time,
                        "response": {
                            "code": code,
                            "success": success,
                            "data": None
                        }
                    }

                    date_time = utils.get_dates_new()['date_now_full']
                    data = {
                        "date_time": str(date_time),
                        "pinged": app.get('slug'),
                        "success": success,
                        "endpoints_res": data
                    }
                    save_data.save_data(slug, "pings", data)
                    sleep(1)


def report(app, code):
    """ Sends a telegram message to admin. """

    if settings.get('notifications'):
        payload = [
            "👨‍🚀 Mr-Ping-Ping:\n\n",
            f"❌No Response: {app.get('slug')} : {code}"
        ]

        requests.post(url=utils.get_notify_endpoint(settings), json=payload)


def print_Status(name, success, code, res_time):
    """ Prints response """
    print(
        f"Mr-Ping-Ping: Checked - {name} | Res: {success} - {code} | Time: {res_time}")


if __name__ == '__main__':

    error_count = 0

    settings = utils.read_json(os.path.join(root_dir, "configs", "main.json"))  # nopep8

    print('Mr-Ping-Ping: Starting')

    ping_apps()
    run()

    while True:
        try:
            run()
            error_count = 0
        except Exception as e:
            print(e)
            sleep(60)

            error_count += 1

            if error_count >= 5:
                payload = [
                    "👨‍🚀 Mr-Ping-Ping:\n\n",
                    f"❌Something is wrong with Mr-Ping-Ping! \n\n Waiting for admin input."
                ]
                requests.post(url=utils.get_notify_endpoint(
                    settings), json=payload)

                input()
