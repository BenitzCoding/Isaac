from cool_utils import Terminal

from discord.ext.commands import Cog

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_repetition = {}

    @Cog.listener("on_ready")
    async def startup(self):
        self.bot.Internal.pass_bot(self.bot)
        self.bot.Internal.load_config("./config.json")
        Terminal.display("Bot client has initialised.")

    @Cog.listener("on_error")
    async def error_handler(self, ctx, error):
        self.bot.Internal.error(ctx, error)

    @Cog.listener("on_message")
    async def message_handler(self, message):
        if message.user != self.bot.user or message.guild is not None:
            return

        if self.bot.Internal.compromised:
            return await message.delete()

        await self.bot.Internal.message_channel.send(f"**Message:** ```\n{message.content}\n```\n**Message Link:** {message.jump_url}")
        if self.message_repetition.get(message.content) is None:
            self.message_repetition.update(
                {
                    message.content: {
                        "count": 1,
                        "message_ids": [message.id]
                    }
                }
            )

        elif self.message_repetition.get(message.content) >= self.bot.Internal.threshold:
            for messages in self.message_repetition.get(message.content).get("message_ids"):
                message_object = await self.bot.fetch_message(messages)
                await message_object.delete()
                self.bot.Internal.compromised = True

            return await self.bot.Internal.alarts_channel.send(f"Message repeated {self.message_repetition.get(message.content).get('count')} times compromising bot.")

        else:
            self.message_repetition.update(
                {
                    message.content: {
                        "count": self.message_repetition.get(message.content).get("count") + 1,
                        "message_ids": self.message_repetition.get(message.content).get("message_ids").append(message.id)
                    }
                }
            )