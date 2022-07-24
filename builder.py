#!/usr/bin/python3

from cool_utils import Terminal

class snowflake(int):
    

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


get_response()