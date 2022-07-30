#!/usr/bin/python3
import os
import json

from cool_utils import Terminal

# class snowflake(int):
    
def get_response() -> dict:
    Terminal.clear()
    print(f"{'-' * 21}\n|{' ' * 6}OPTIONS{' ' * 6}|\n{'-' * 21}\n|{' ' * 6}1.Setup{' ' * 6}|\n|{' ' * 6}2.Run{' ' * 8}|\n|{' ' * 6}3.Exit{' ' * 7}|\n{'-' * 21}")

    try:
        option: int = input("Select the number to choose what you'd like to do. [>] ")
    except:
        print("Invalid input.\nAbort.")

    if option == 1:
        token: str = input("Enter the bot token. [>] ")
        mongo_url: str = input("Enter the MongoDB url. [>] ")
        core_guild: int = input("Enter the core guild id. [>] ")
        owner: int = input("Enter the Discord owner id. [>] ")
        webhook: str = input("Enter the alarts webhook url. [>] ")
        error_webook: str = input("Enter the error webhook url. [>] ")

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

main() if __name__ == "__main__" else None