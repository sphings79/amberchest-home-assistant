"""Constants for the AmberChest integration."""

from datetime import timedelta

DOMAIN = "amberchest"

CONF_VERIFY_SSL = "verify_ssl"

DEFAULT_PORT = 8484
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

# AmberChest keeps its session tokens in memory, so a restart of the server
# invalidates ours. The client logs in again when that happens.
LOGIN_PATH = "/api/login"
STATE_PATH = "/api/state"
ACCOUNTS_PATH = "/api/accounts"
SCHEDULE_PATH = "/api/schedule"
