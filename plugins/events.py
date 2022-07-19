from cool_utils import Terminal

from discord.ext.commands import Cog

from buttons import BlockNukerButtons

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.message_repetition = {}
		self.bot_nuke = {}

	@Cog.listener("on_ready")
	async def startup(self):
		self.bot.Internal.pass_bot(self.bot)
		self.bot.Internal.load_config("./config.json")
		Terminal.display("Bot client has initialised.")

	@Cog.listener("on_error")
	async def error_handler(self, ctx, error):
		await self.bot.Internal.error(ctx, error)

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

		elif self.message_repetition.get(message.content) >= self.bot.Internal.message_threshold:
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

	@Cog.listener("on_guild_join")
	async def guild_join_handler(self, guild):
		owner = await self.bot.fetch_user(guild.owner_id)
		if self.bot_nuke.get(owner.id) is None:
			self.bot_nuke.update(
				{
					owner.id: {
						"count": 1,
						"guild_ids": [guild.id]
					}
				}
			)

		if owner.id in self.bot.Internal.blocked_users:
			await guild.leave()
			return await self.bot.Internal.ads_channel.send(f"Blocked guild {guild.name} (`{guild.id}`) due to it being owned by user ``")

		elif self.bot_nuke.get(owner.id) >= self.bot.Internal.guild_join_threshold:
			for guilds in self.bot_nuke.get(owner.id).get("guild_ids"):
				guild_object = await self.bot.fetch_guild(guilds)
				await guild_object.leave()

			message = f"User {owner.name}#{owner.discriminator} (`{owner.id}`) has attempted to nuke bot with {self.bot_nuke.get(owner.id).get('count')} guilds. Threats averted!\nWould you like to block this user?"
			buttons = BlockNukerButtons(message)

			await self.bot.Internal.ads_channel.send(message, view = buttons)
			await buttons.wait()
			if buttons.block:
				self.bot.Internal.block_user(owner.id)

		await self.bot.Internal.join_channel.send(f"**Guild:** {guild.name} (`{guild.id}`) [Scanned guild]")