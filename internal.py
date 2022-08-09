import os
import sys
import json
import traceback

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Union

from discord import User
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument

from git import Repo, Git
from cool_utils import Terminal

def clone_git(repo: str) -> None:
    tree = ""
    for folders in (os.getcwd() + __file__).split("/")[:-1]:
        tree += f"/{folders}"

    tree += "/Compromised"

    if not repo.endswith(".git"):
        repo += ".git"

    GIT = Git(tree)
    try:
        GIT.clone(repo)
    except:
        raise ValueError("Git clone failed.")

class Internal:
    def __init__(self):
        self.bot = None
        self.owner = None
        self.config = None
        self.compromised = False
        self.application_id = None
        self.token = None
        self.threshold = None
        self.message_threshold = None
        self.core_guild = None
        self.message_channel = None
        self.join_channel = None
        self.ads_channel = None
        self.alerts_channel = None
        self.errors_channel = None
        self.mongo = None

    def pass_bot(self, bot):
        self.bot = bot

    def load_partial_config(self, file: str) -> None:
        with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.application_id = file_.get("application_id")
            self.token = file_.get("token")

    async def rapid_compromised_checks(self):
        while True:
            if self.compromised:
                await self.alerts_channel.send("Bot has been compromised, The Bot's token will now be leaked. please regenerate token when available.")
                await self.bot.close()
                sys.exit(1)

    async def error(self, ctx, error: Exception) -> None:
        ignored_exceptions = (CommandNotFound, BadArgument, MissingRequiredArgument)

        if isinstance(error, ignored_exceptions):
            return

        Terminal.error(f"-------")
        Terminal.error(f"Ignoring exception in command {ctx.command}:", file = sys.stderr)
        print("\033[91m")
        traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
        Terminal.error(f"-------")

        channel = await self.bot.fetch_channel(self.errors_channel)
        await channel.send(f"```py\nIgnoring exception in command {ctx.command}:\n{type(error)} {error} {error.__traceback__}\n```")

        return

    async def fetch(self, collection: str, query: dict, list: bool = False) -> Union[dict, list]:
        if self.mongo is None:
            raise ValueError("No Config files loaded.")

        if list:
            try:
                return await self.mongo[collection].find(query)
            except Exception as error:
                raise error

        else:
            try:
                return await self.mongo[collection].find_one(query)
            except Exception as error:
                raise error

    async def block_user(self, user: User) -> None:
        if self.mongo is None:
            raise ValueError("No Config files loaded.")

        if user.id in await self.fetch(
            "nukers",
            {
                "_id": "blocked"
            }
        ):
            return False

        try:
            await self.mongo['nukers'].update_one(
                {
                    "_id": "blocked"
                },
                {
                    "$addToSet": {
                        "users": user.id
                    }
                }
            )
            return True
        except Exception as error:
            raise error

    async def unblock_user(self, user: User) -> bool:
        if self.mongo is None:
            raise ValueError("No Config files loaded.")

        if user.id not in await self.fetch(
            "nukers",
            {
                "_id": "blocked"
            }
        ):
            return False

        try:
            await self.mongo['nukers'].update_one(
                {
                    "_id": "blocked"
                },
                {
                    "$pull": {
                        "users": user.id
                    }
                }
            )
            return True
        except Exception as error:
            raise error

    async def load_config(self, file: str) -> None:
        if self.bot is None:
            raise ValueError("Bot is not connected to Discord API.")

        async with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.owner = self.bot.get_user(self.config.get("owner"))
            self.application_id = self.config.get("application_id")
            self.token = self.config.get("token")
            self.threshold = self.config.get("threshold")
            self.message_threshold = self.config.get("message_threshold")
            self.core_guild = await self.bot.fetch_channel(self.config.get("core_guild"))
            self.message_channel = await self.bot.fetch_channel(self.config.get("message_channel"))
            self.join_channel = await self.bot.fetch_channel(self.config.get("join_channel"))
            self.ads_channel = self.config.get("ads_channel")
            self.alerts_channel = self.config.get("alerts_channel")
            self.errors_channel = self.config.get("errors_channel")
            self.mongo = AsyncIOMotorClient(self.config.get("mongo"))['isaac']

    async def setup(self) -> None:
        if self.config is None:
            raise ValueError("No Config files loaded.")

        Terminal.start_log()
        Terminal.display("Initiated Bot Setup.")
