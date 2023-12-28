import os

from maply.log import get_logger

logger = get_logger(__name__)

try:
    import dotenv
except ModuleNotFoundError:
    pass
else:
    if dotenv.find_dotenv():
        logger.info("Found .env file, loading environment variables")

        dotenv.load_dotenv(override=True)


DEV: bool = os.getenv("BOT_DEBUG", "false").lower() == "true"

MAX_ROWS: int = 1000
MAX_ERROR_LENGTH: int = 3000


class Database:
    """Contains database config attributes."""

    _postgres_uri = os.environ["PG_URI"]
    _postgres_dev_uri = os.environ["PG_DEV_URI"]
    _alembic_uri = os.environ["ALEMBIC_URI"]
    _alembic_dev_uri = os.environ["ALEMBIC_DEV_URI"]

    postgres_uri = _postgres_dev_uri if DEV else _postgres_uri
    alembic_uri = _alembic_dev_uri if DEV else _alembic_uri


class Client:
    """Contains bot config attributes."""

    name = "Maply"
    support_server = "nmwaDS35sC"
    invite_link = (
        "https://discord.com/api/oauth2/authorize?"
        "client_id=975530567955267589&permissions=268471296&scope=bot%20applications.commands"
    )

    _token = os.environ["TOKEN"]
    _dev_token = os.environ["DEV"]

    token = _dev_token if DEV else _token
