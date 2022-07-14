import sys
import json
import traceback

from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument

from cool_utils import Terminal

class Internal:
    def __init__(self):
        self.bot = None
        self.owner = None
        self.config = None
        self.compromised = False
        self.application_id = None
        self.token = None
        self.threshold = None
        self.core_guild = None
        self.message_channel = None
        self.join_channel = None
        self.ads_channel = None
        self.alerts_channel = None
        self.errors_channel = None

    def pass_bot(self, bot):
        self.bot = bot

    def load_partial_config(self, file: str) -> None:
        with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.application_id = file_.get("application_id")
            self.token = file_.get("token")

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

    async def load_config(self, file: str) -> None:
        if self.bot is None:
            raise ValueError("Bot is not connected to Discord API.")

        async with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.owner = self.bot.get_user(self.config.get("owner"))
            self.application_id = self.config.get("application_id")
            self.token = self.config.get("token")
            self.threshold = self.config.get("threshold")
            self.core_guild = await self.bot.fetch_channel(self.config.get("core_guild"))
            self.message_channel = await self.bot.fetch_channel(self.config.get("message_channel"))
            self.join_channel = await self.bot.fetch_channel(self.config.get("join_channel"))
            self.ads_channel = self.config.get("ads_channel")
            self.alerts_channel = self.config.get("alerts_channel")
            self.errors_channel = self.config.get("errors_channel")
    
    async def setup(self) -> None:
        if self.config is None:
            raise ValueError("No Config files loaded.")

        Terminal.start_log()
        Terminal.display("Initiated Bot Setup.")