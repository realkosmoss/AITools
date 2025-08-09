from services.vheer import Vheer
from services.writecream import WriteCream
from services.perchance import PerchanceImageGenerator

if __name__ == "__main__":
    vheer = Vheer()
    writecream = WriteCream()
    perchance = PerchanceImageGenerator()

    user_input = input("Image prompt: ")
    print("[vheer]", vheer.generate(user_input.strip()))
    print("[writecream]", writecream.generate(user_input.strip()))
    print("[perchance]", perchance.generate(user_input.strip()))
