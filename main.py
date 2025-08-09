from ImageGenerators.services.perchance import PerchanceImageGenerator
from ImageGenerators.services.vheer import Vheer
from ImageGenerators.services.writecream import WriteCream

from ChatBots.services.perchance import PerchanceChatBot
from ChatBots.services.deepai import DeepAI

import os
import sys
import time

# "init" colors
os.system("")

# color codes
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

def typewriter(text, delay=0.002):
    """Print text with a typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    banner = f"""{MAGENTA}{BOLD}
    ___    ____   ______            __
   /   |  /  _/  /_  __/___  ____  / /____
  / /| |  / /     / / / __ \\/ __ \\/ / ___/
 / ___ |_/ /     / / / /_/ / /_/ / (__  )
/_/  |_/___/    /_/  \\____/\\____/_/____/
{RESET}"""
    typewriter(banner, 0.0005)

def print_menu():
    print(f"{GREEN}{BOLD}Image Generators:{RESET}")
    print(f" {YELLOW}1.{WHITE} Perchance")
    print(f" {YELLOW}2.{WHITE} Vheer")
    print(f" {YELLOW}3.{WHITE} Writecream")
    print(f"\n{CYAN}{BOLD}Chat Bots:{RESET}")
    print(f" {YELLOW}4.{WHITE} Perchance")
    print(f" {YELLOW}5.{WHITE} DeepAI")

def main() -> None:
    print_banner()
    typewriter(f"{CYAN}{BOLD}Hello, Anon.{RESET}\n", 0.01)

    # Preload services
    perchance = PerchanceImageGenerator()
    vheer = Vheer()
    writecream = WriteCream()

    while True:
        print_menu()
        choice = input(f"\n{MAGENTA}>>> Select an option (or 'q' to quit): {RESET}").strip().lower()

        if choice == "q":
            typewriter(f"{CYAN}Goodbye, Anon.{RESET}", 0.01)
            break

        if choice == "1":
            prompt = input(f"{CYAN}Image prompt: {RESET}")
            print(f"{GREEN}Result:{RESET} {perchance.generate(prompt)}")

        elif choice == "2":
            prompt = input(f"{CYAN}Image prompt: {RESET}")
            print(f"{GREEN}Result:{RESET} {vheer.generate(prompt)}")

        elif choice == "3":
            prompt = input(f"{CYAN}Image prompt: {RESET}")
            print(f"{GREEN}Result:{RESET} {writecream.generate(prompt)}")

        elif choice == "4":
            print(f"{MAGENTA}{BOLD}Commands:{RESET}")
            print(f" {YELLOW}clear{WHITE} – Clears all context")
            print(f" {YELLOW}remove N{WHITE} – Removes last N messages")
            print(f" {YELLOW}break{WHITE} – Exit chat mode")
            perchanceChatBot = PerchanceChatBot()

            while True:
                user_input = input(f"{CYAN}You:{RESET} ").strip()
                message_lower = user_input.lower()

                if message_lower == "clear":
                    perchanceChatBot.MessagesHandler.clear()
                    print(f"{GREEN}Messages cleared.{RESET}")
                    continue

                if message_lower.startswith("remove"):
                    try:
                        amount = int(message_lower.replace("remove", "").strip())
                        perchanceChatBot.MessagesHandler.remove(amount)
                        print(f"{GREEN}Removed {amount} message(s).{RESET}")
                    except Exception as e:
                        print(f"{YELLOW}Error:{RESET} {e}")
                    continue

                if message_lower == "break":
                    break

                perchance_response = perchanceChatBot.generate(user_input) or perchanceChatBot.generate(user_input)
                print(f"{WHITE}Bot:{RESET} {perchance_response}")
        elif choice == "5":
            print(f"{MAGENTA}{BOLD}Commands:{RESET}")
            print(f" {YELLOW}clear{WHITE} – Clears all context")
            print(f" {YELLOW}remove{WHITE} – Removes last messages")
            print(f" {YELLOW}break{WHITE} – Exit chat mode")
            DeepAIChatBot = DeepAI(handle_messages_list=True)

            while True:
                user_input = input(f"{CYAN}You:{RESET} ").strip()
                message_lower = user_input.lower()

                if message_lower == "clear":
                    DeepAIChatBot.MessagesHandler.clear()
                    print(f"{GREEN}Messages cleared.{RESET}")
                    continue

                if message_lower.startswith("remove"):
                    try:
                        DeepAIChatBot.MessagesHandler.remove() # User message
                        DeepAIChatBot.MessagesHandler.remove() # AI Message
                        print(f"{GREEN}removed (2) message(s).{RESET}")
                    except Exception as e:
                        print(f"{YELLOW}Error:{RESET} {e}")
                    continue

                if message_lower == "break":
                    break

                perchance_response = DeepAIChatBot.generate(user_input) or DeepAIChatBot.generate(user_input)
                print(f"{WHITE}Bot:{RESET} {perchance_response}")
        else:
            print(f"{YELLOW}Invalid option, try again.{RESET}")

if __name__ == "__main__":
    main()
