# Ping Ping

Scheduled pings for my side projects, saves out response data that gets used in another project, and sends out a notification if server is down, it also exposes an API for this service.

Setup:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Or Docker:

`docker compose up -d --build`

/confgis directory is for config files:

```
config.json
{
      "name": "Ping Ping",
      "slug": "ping-ping",
      "host": "[IP_ADDRESS]",
      "port": 5005,
      "timeout": 15,
      "log_file": "service.log", // log file
      "notifications": true, // enable notifications
      "notify_bot": "null-face", // for telegram api service
      "tele_jam_api_baseurl": "http://[IP_ADDRESS]" // for telegram api service
}
```

ping-apps.json

```
[
    {
        "name": "Ping Ping",
        "slug": "ping-ping",
        "host": "[IP_ADDRESS]",
        "port": 5005,
        "timeout": 15,
        "log_file": "service.log", // log file
        "notifications": true, // enable notifications
        "notify_bot": "null-face", // for telegram api service
        "tele_jam_api_baseurl": "http://[IP_ADDRESS]" // for telegram api service
    }
]
```

schedules.json

```
[
    {
        "name": "Ping Ping",
        "slug": "ping-ping",
        "host": "[IP_ADDRESS]",
        "port": 5005,
        "timeout": 15,
        "log_file": "service.log", // log file
        "notifications": true, // enable notifications
        "notify_bot": "null-face", // for telegram api service
        "tele_jam_api_baseurl": "http://[IP_ADDRESS]" // for telegram api service
    }
]
```

## API

### System

- GET /health - Returns health of the service.
- GET /logs - Returns logs of the service.
- GET /config - Returns config of the service.
- PATCH /config - Updates config of the service.

### Service - WIP !

- GET /service/status - Returns status of the service.
- POST /service/restart - Restarts the service.
- POST /service/shutdown - Shuts down the service.
- POST /service/pause - Pauses a job.
- POST /service/resume - Resumes a job.

### Ping Apps

- GET /ping-apps - Returns list of ping apps.
- GET /ping-apps/status - Returns status of ping apps.
- GET /ping-apps/data - Returns data of ping apps.
- GET /ping-apps/schedules - Returns schedules of ping apps.
- GET /ping-apps/actions - Returns actions of ping apps.

### Ping Ping

- GET /ping-ping/status - Returns status of ping ping.
- GET /ping-ping/service-config - Returns config of ping ping.

### DOCS

- GET /docs - Returns API documentation.
- GET /redoc - Returns API documentation.
