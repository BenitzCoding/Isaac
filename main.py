import asyncio

from cool_utils import Terminal

from discord import Intents
from discord.ext import commands

from internal import Internal as System

Internal = System()
asyncio.run(Internal.load_config("./config.json"))
asyncio.run(Internal.setup())
intents = Intents.all()
intents.members = True

class Isaac(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Terminal.display("Isaac Initialised.")

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)

    async def close(self):
        Terminal.display("Isaac Session Terminated.")
        await super().close()

bot = Isaac(
    intents = intents,
    command_prefix = "/",
    case_insensitive = True,
    application_id = Internal.application_id
)

async def start_runtime():
    await bot.start(Internal.token)
    Terminal.display("Bot start invoked!")

if __name__ == "__main__":
    asyncio.run(start_runtime())