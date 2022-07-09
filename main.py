from discord.ext import commands

from internal import Internal as System

Internal = System()
Internal.load_config("./config.json")
Internal.setup()

class Isaac(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

bot = Isaac(
    application_id = Internal.application_id
)

