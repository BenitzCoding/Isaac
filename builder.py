#!/usr/bin/python3
import os
import sys
import json

from git import Git
from cool_utils import Terminal

# class snowflake(int):

def clone_git(repo: str) -> None:
	tree = ""
	for folders in (os.getcwd() + __file__).split("/")[:-1]:
		tree += f"/{folders}"

	tree += "/Compromised"

	if not repo.endswith(".git"):
		repo += ".git"

	GIT = Git(tree)
	try:
		GIT.clone(repo)
	except:
		raise ValueError("Git clone failed.")
	
def get_response(restart: bool = False) -> dict:
	Terminal.clear()
	print(f"{'-' * 21}\n|{' ' * 6}OPTIONS{' ' * 6}|\n{'-' * 21}\n|{' ' * 6}1.Setup{' ' * 6}|\n|{' ' * 6}2.Run{' ' * 8}|\n|{' ' * 6}3.Exit{' ' * 7}|\n{'-' * 21}") if not restart else None

	try:
		option = int(input("Select the number to choose what you'd like to do. [>] "))
	except:
		print("Invalid input.\nAbort.")

	if option == 1:
		token: str = input("Enter the bot token. [>] ")
		mongo_url: str = input("Enter the MongoDB url. [>] ")
		core_guild: int = input("Enter the core guild id. [>] ")
		owner: int = input("Enter the Discord owner id. [>] ")
		webhook: str = input("Enter the alarts webhook url. [>] ")
		error_webook: str = input("Enter the error webhook url. [>] ")
		while True:
			github: str = input("Enter the github repo url for safety discord blocks. [>] ")
			try:
				clone_git(github)
				break
			except ValueError:
				print("Git clone failed. Please try again.")
				continue

		run: bool = input("Would you like to run the bot after setup? [Y/N] ")
		return {
			"type": "setup",
			"run": run,
			"token": token,
			"mongo_url": mongo_url,
			"core_guild": core_guild,
			"owner": owner,
			"webhook": webhook,
			"error_webook": error_webook
		}

	elif option == 2:
		return {
			"type": "run"
		}

	elif option == 3:
		return {
			"type": "exit"
		}

	else:
		print("Invalid input.")
		return get_response(True)

def run():
	if not os.path.exists("config.json"):
		raise ValueError("No config file found.")

	os.system("python3 main.py")

def write_config(data: dict) -> None:
	with open("config.json", "w") as f:
		f.write(json.dumps(data))

def main():
	response = get_response()
	if response['type'] == "setup":
		write_config(response)
		run() if response['run'] else None

	elif response['type'] == "run":
		run()

	elif response['type'] == "exit":
		print("Exiting...")
		sys.exit(0)

	else:
		raise ValueError("Invalid response.")

main() if __name__ == "__main__" else None