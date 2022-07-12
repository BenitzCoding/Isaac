from cool_utils import Terminal

from discord.ext.commands import Cog

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def startup(self):
        self.bot.Internal.pass_bot(self.bot)
        self.bot.Internal.load_config("./config.json")
        Terminal.display("Bot client has initialised.")

    @Cog.listener("on_message")
    async def message(self, message):
        if message.user != self.bot.user:
            return