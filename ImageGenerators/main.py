from services.vheer import Vheer
from services.writecream import WriteCream

if __name__ == "__main__":
    vheer = Vheer()
    writecream = WriteCream()

    user_input = input("Image prompt: ")
    print("[vheer]", vheer.generate(user_input.strip()))
    print("[writecream]", writecream.generate(user_input.strip()))