import os
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

    async def sync_application(self):
        await self.tree.sync(guild = Internal.core_guild)
        Terminal.display("Application synced successfully.")

    async def setup_hook(self):
        for filename in os.listdir("./plugins"):
            if filename.endswith(".py"):
                name = filename[:-3]
                try:
                    await self.load_extension(f"plugins.{name}")
                except Exception as e:
                    Terminal.error(f"Failed to load plugin {name}.")
                    Terminal.error(e)
                    continue
                Terminal.display(f"Loaded extension {name}.")

        self.loop.create_task(self.sync_application())

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