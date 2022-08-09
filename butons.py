from discord.ui import View, button

class BlockNukerButtons(View):
	def __init__(self, message: str):
		super().__init__(timeout = None)
		self.block = None
		self.message = message[:34]

	@button
	async def unblock(self, button, interaction):
		self.block = True
		button.label = "Unblocked"
		for button_ in self.buttons:
			button_.disabled = True

		await interaction.response.edit_message(self.message)

	@button
	async def keep_block(self, button, interaction):
		self.block = True
		button.label = "Kept Blocked"
		for button_ in self.buttons:
			button_.disabled = True

		await interaction.response.edit_message(self.message)
