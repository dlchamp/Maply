from __future__ import annotations

import csv
import datetime
import os
import sys as s

import disnake
from disnake import __version__ as disnake_version
from disnake.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from maply import __version__ as bot_version
from maply import constants, log, utils
from maply.types import Country

logger = log.get_logger(__name__)


class Maply(commands.InteractionBot):
    """Base bot instance."""

    def __init__(
        self,
        *,
        intents: disnake.Intents,
        reload: bool,
        chunk_guilds_at_startup: bool,
    ) -> None:
        super().__init__(
            intents=intents,
            reload=reload,
            chunk_guilds_at_startup=chunk_guilds_at_startup,
        )

        self.start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

        self.engine = engine = create_async_engine(constants.Database.postgres_uri)
        self.db_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        self.countries: list[Country] = self.load_country_csv()

    async def on_ready(self) -> None:
        """Handle on_ready event."""
        message = (
            "----------------------------------------------------------------------\n"
            f"Running in DEV MODE: {constants.DEV}\n"
            f'Bot started at: {utils.now().strftime("%m/%d/%Y - %H:%M:%S")}\n'
            f"System Version: {s.version}\n"
            f"Disnake Version: {disnake_version}\n"
            f"Bot Version: {bot_version}\n"
            f"Connected to Discord as {self.user} ({self.user.id})\n"
            "----------------------------------------------------------------------\n"
        )
        logger.info(message)

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        """Alias of bot.db_session."""
        return self.db_session

    async def load_extensions(self) -> None:  # type: ignore
        """Load all extensions available in `ext`."""
        for item in os.listdir("csvbot/ext"):
            if "__" in item or not item.endswith("py"):
                continue

            ext = f"csvbot.ext.{item[:-3]}"
            self.load_extension(ext)
            logger.info(f"Cog loaded: {ext}")

    def load_country_csv(self) -> list[Country]:
        """Load the values from 'country_lat_long.csv into Country objects and cache."""
        countries: list[Country] = []

        with open("maply/country_lat_long.csv") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            # skip header
            next(reader, None)

            for row in reader:
                code, lat, lon, name = row
                countries.append(Country(code, name, lat, lon))

        return countries
