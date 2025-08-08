from services.perchance import PerchanceChatBot

if __name__ == "__main__":
    Perchance = PerchanceChatBot() # automatic message handling

    while True:
        user_input = input("Chat prompt: ")
        # Handle commands?!
        message_lower = user_input.lower()
        if message_lower == "clear":
            Perchance.MessagesHandler.clear()
            print("Cleared messages.")
            continue
        if "remove" in message_lower:
            amount = message_lower.replace("remove", "")
            try:
                Perchance.MessagesHandler.remove(int(amount.strip()))
            except Exception as e:
                print("...", e)
                continue
            print("Removed 1.")
            continue
        print("[Perchance]", Perchance.generate(user_input.strip())) # if its empty just try again ig
