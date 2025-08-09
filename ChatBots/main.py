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
            print("context:", Perchance.MessagesHandler.get())
            print("Removed 1.")
            continue
        perchance_response = Perchance.generate(user_input.strip())
        if not perchance_response:
            perchance_response = Perchance.generate(user_input.strip())
        print("[Perchance]", perchance_response) # if its empty just try again ig