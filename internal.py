import json

from cool_utils import Terminal

class Internal:
    def __init__(self):
        self.config = None
        self.application_id = None
        self.token = None

    def error(self, error: Exception) -> None:
        Terminal.error(f"{error}")

    async def load_config(self, file: str) -> None:
        async with open(file, 'r') as file_:
            self.config = json.load(file_)
            self.application_id = self.config.get("application_id")
            self.token = self.config.get("token")
    
    async def setup(self) -> None:
        if self.config is None:
            raise ValueError("No Config files loaded.")

        Terminal.start_log()
        Terminal.on_error(self.error)
        Terminal.display("Initiated Bot Setup.")