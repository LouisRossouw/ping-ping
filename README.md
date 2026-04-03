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

json configs are used to define the service, the http urls and it's endpoints to ping, and the scheduled / intervals. (the schedules & ping-apps slug & actions keys must match)

/confgs:
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
        "name": "TimeInProgress-website-client",
        "slug": "timeinprogress_client", // * Must match schedules.json action key
        "base_url": "https://www.timeinprogress.com/",
        "endpoints": ["api/health","api/stats"],
        "active": true,
        "notify": true
    },
]
```

schedules.json
```
[
    {
        "name": "timeinprogress-website-client",
        "action": "timeinprogress_client",  // * Must match ping-apps.json slug key, i should rename this to slug.
        "trigger": "interval",
        "hours": 1
    },
]

or specific days / time
    "hour": 18,
    "minute": 0
    or "day_of_week": "sun", # mon-fri
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
