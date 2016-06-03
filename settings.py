import os
import motor

LISTENING_PORT = 8080
DEBUG = False
ASYNC_HTTP_MAX_CLIENT = 50

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

ES_RESULT_SIZE = 1000

BRIDGE_FIELDS = [{"title": "Nickname", "data": "nickname", "className": "nickname"},
                 {"title": "First Seen", "data": "first_seen", "className": "first_seen"},
                 {"title": "Last Seen", "data": "last_seen", "className": "last_seen"},
                 {"title": "Last Restarted", "data": "last_restarted", "className": "last_restarted"},
                 {"title": "Flags", "data": "flags", "className": "flags"},
                 {"title": "Platform", "data": "platform", "className": "platform"},
                 {"title": "Transports", "data": "transports", "className": "transports"},
                 {"title": "IP", "data": "ip_address", "className": "ip_address"},
                 {"title": "Bandwidth", "data": "bandwidth", "className": "bandwidth"},
                 {"title": "Atlas", "data": "hashed_fingerprint", "className": "atlas"},
                 ]

RELAY_FIELDS = [{"title": "Nickname", "data": "nickname", "className": "nickname"},
                {"title": "First Seen", "data": "first_seen", "className": "first_seen"},
                {"title": "Last Seen", "data": "last_seen", "className": "last_seen"},
                {"title": "Last Restarted", "data": "last_restarted", "className": "last_restarted"},
                {"title": "Flags", "data": "flags", "className": "flags"},
                {"title": "Platform", "data": "platform", "className": "platform"},
                {"title": "Geo", "data": "geo", "className": "geo"},
                {"title": "IP", "data": "ip_address", "className": "ip_address"},
                {"title": "Bandwidth", "data": "bandwidth", "className": "bandwidth"},
                {"title": "Atlas", "data": "fingerprint", "className": "atlas"},
                ]

BRIDGE_ES_FIELDS = ["nickname", "first_seen", "last_seen", "last_restarted", "platform", "transports", "or_addresses",
                    "hashed_fingerprint", "flags", "advertised_bandwidth"]

RELAY_ES_FIELDS = ["nickname", "first_seen", "last_seen", "last_restarted", "platform", "transports", "or_addresses",
                   "fingerprint", "flags", "bandwidth", "geo", "dir_address"]

DB_NAME = "onionstats"
COLL_RELAYS = "relays"
COLL_BRIDGES = "bridges"

client = motor.MotorClient('mongodb://localhost:27017')
db = client[DB_NAME]
