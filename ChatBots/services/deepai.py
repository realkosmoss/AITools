import math
import random

class DeepAICustomHash:
    @staticmethod
    def bit_not(x):
        return (~x) & 0xFFFFFFFF
    
    @staticmethod
    def to_signed_32bit(x):
        x = int(x) & 0xFFFFFFFF
        return x if x < 0x80000000 else x - 0x100000000
    
    @staticmethod
    def shitasshashfunction(c: str) -> str:
        a = [0] * 64
        for b in range(64):
            val = 4294967296 * math.sin((b + 1) % math.pi)
            a[b] = DeepAICustomHash.to_signed_32bit(val)

        d = 1732584193
        e = 4023233417
        g = [d, e, DeepAICustomHash.bit_not(d), DeepAICustomHash.bit_not(e)]

        l_bytes = c.encode('utf-8') + b'\x80'
        k = len(l_bytes)

        c_len = ((k - 1) // 4 + 2) | 15

        h = [0] * (c_len + 1)
        h[c_len] = 8 * k

        for i in range(k - 1, -1, -1):
            h[i >> 2] |= l_bytes[i] << (8 * (i % 4))

        b = 0
        while b < c_len:
            k_arr = g.copy()
            l_idx = 0

            while l_idx < 64:
                idx = l_idx >> 4

                funcs = [
                    (k_arr[0] & k_arr[1]) | (DeepAICustomHash.bit_not(k_arr[0]) & k_arr[3]),
                    (k_arr[3] & k_arr[0]) | (DeepAICustomHash.bit_not(k_arr[3]) & k_arr[1]),
                    k_arr[0] ^ k_arr[1] ^ k_arr[3],
                    k_arr[1] ^ (k_arr[0] | DeepAICustomHash.bit_not(k_arr[3]))
                ]

                func_val = funcs[idx]

                idx_arr = [l_idx, 5 * l_idx + 1, 3 * l_idx + 5, 7 * l_idx]
                idx_val = idx_arr[idx] & 15

                h_val = h[b | idx_val] if (b | idx_val) < len(h) else 0

                temp_sum = (k_arr[0] + func_val + a[l_idx] + h_val) & 0xFFFFFFFF

                rotate_k_arr = [7, 12, 17, 22,
                                5, 9, 14, 20,
                                4, 11, 16, 23,
                                6, 10, 15, 21]
                rotate_k = rotate_k_arr[4 * idx + (l_idx % 4)]

                temp_rot = ((temp_sum << rotate_k) | (temp_sum >> (32 - rotate_k))) & 0xFFFFFFFF

                new_val = (temp_rot + k_arr[1]) & 0xFFFFFFFF

                k_arr = [new_val, k_arr[0], k_arr[1], k_arr[2]]
                l_idx += 1

            for i in range(4):
                g[i] = (g[i] + k_arr[i]) & 0xFFFFFFFF

            b += 16

        c_str = ""
        for x in g:
            for i in range(4):
                byte = (x >> (8 * i)) & 0xFF
                c_str += f"{byte:02x}"
        return c_str[::-1]

from curl_cffi import requests
import json

class MessagesHandler:
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages.clear()

    def remove(self):
        self.messages.pop()

    def add(self, message: str, role: str = "user") -> None:
        """Adds a message to the context."""
        self.messages.append({"role": role, "content": message})
    
    def get(self):
        """Returns messages"""
        return self.messages

class DeepAIModels:
    standard = "standard"
    math = "math"        # Specialized in math?
    online = "online"    # Live web browsing

class DeepAI:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.5",
        "cache-control": "max-age=0",
        "dnt": "1",
        "priority": "u=0, i",
        "referer": "https://www.google.com/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }
    cookies = {
        "user_sees_ads": "true"
    }
    def __init__(self, model=DeepAIModels.standard, handle_messages_list=False):
        self.session = requests.Session(impersonate="chrome", headers=self.headers, cookies=self.cookies)
        self.MessagesHandler = MessagesHandler()
        self.handle_messages_list = handle_messages_list

        self.model = model
        self.app_base_url = "https://api.deepai.org"
        self.tryitApiKey = self.generate_tryit_api_key()

    def generate_tryit_api_key(self, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"):
        """boinkers"""
        myrandomstr = str(round(random.random() * 100000000000)) # Math.round((Math.random() * 100000000000))

        key = 'tryit-' + myrandomstr + '-' + DeepAICustomHash.shitasshashfunction(
            user_agent + DeepAICustomHash.shitasshashfunction(
                user_agent + DeepAICustomHash.shitasshashfunction(
                    user_agent + myrandomstr + 'hackers_become_a_little_stinkier_every_time_they_hack'
                )
            )
        )
        return key
    
    def generate(self, prompt): # there is no "save_chat_session", maybe for the best?
        headers = self.headers.copy()
        headers["sec-fetch-dest"] = "empty"
        headers["sec-fetch-mode"] = "cors"
        headers["sec-fetch-site"] = "same-site"

        headers["api-key"] = self.tryitApiKey

        form_data = {
            "chat_style": "chat",
            "chatHistory": json.dumps(self.MessagesHandler.get() + [{"role": "user", "content": prompt}]),
            "model": self.model,
            "hacker_is_stinky": "very_stinky",
        }
        
        resp = self.session.post(self.app_base_url + "/hacking_is_a_serious_crime", data=form_data, headers=headers) # 😂
        if resp.status_code == 200:
            if self.handle_messages_list:
                self.MessagesHandler.add(prompt, "user")
                self.MessagesHandler.add(resp.text, "assistant")
            return resp.text
        else:
            print(resp.text)
            raise Exception("[DeepAI] Well, non 200 status_code.")

if __name__ == "__main__":
    deepai = DeepAI()
    print(deepai.generate("hi how are you?!"))
