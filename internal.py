import json

from cool_utils import Terminal

class Internal:
    def __init__(self):
        self.bot = None
        self.owner = None
        self.config = None
        self.application_id = None
        self.token = None
        self.core_guild = None
        self.message_channel = None
        self.join_channel = None
        self.ads_channel = None
        self.alerts_channel = None
        self.errors_channel = None

    def pass_bot(self, bot):
        self.bot = bot

    def error(self, error: Exception) -> None:
        Terminal.error(f"{error}")

    def load_partial_config(self, file: str) -> None:
        with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.application_id = file_.get("application_id")
            self.token = file_.get("token")

    async def load_config(self, file: str) -> None:
        if self.bot is None:
            raise ValueError("Bot is not connected to Discord API.")

        async with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.owner = self.bot.get_user(self.config.get("owner"))
            self.application_id = self.config.get("application_id")
            self.token = self.config.get("token")
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
        Terminal.on_error(self.error)
        Terminal.display("Initiated Bot Setup.")