import random
import string
import json
import base64
from time import time as _time
from curl_cffi import requests

class Fingerprint:
    def __init__(self, session: requests.Session):
        self.session = session
        self.SessionID = self._rand_string(36)

        self.user_agent, self.platform = self._user_agent()
        self.language = self._language()
        self.screen_width = self._screen_width()
        self.screen_height = self._screen_height()
        self.color_depth = self._color_depth()
        self.time_zone = self._time_zone()
        self.hardware_concurrency = self._hardware_concurrency()
        self.mouse_moves = self._mouse_moves()
        self.key_presses = self._key_presses()

    @staticmethod
    def _user_agent():
        browsers = ["Chrome", "Firefox", "Edg"]
        os_versions = ["Windows NT 10.0", "Windows NT 11.0", "Windows NT 8.1"]
        os_version = random.choice(os_versions)
        browser = random.choice(browsers)
        major = random.randint(100, 150)
        minor = random.randint(0, 9)
        if browser == "Firefox":
            ua = f"Mozilla/5.0 ({os_version}; Win64; x64; rv:{major}.0) Gecko/20100101 Firefox/{major}.0"
        elif browser == "Edg":
            ua = f"Mozilla/5.0 ({os_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.{minor}.0.0 Safari/537.36 Edg/{major}.{minor}.0.0"
        else:
            ua = f"Mozilla/5.0 ({os_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.{minor}.0.0 Safari/537.36"
        return ua, "Win64"

    @staticmethod
    def _language():
        return random.choice(["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "zh-CN", "ja-JP"])

    @staticmethod
    def _screen_width():
        return random.choice([1280, 1440, 1920, 2560, 3840])

    @staticmethod
    def _screen_height():
        return random.choice([1080, 1366, 1440, 1600, 2160, 2880])

    @staticmethod
    def _time_zone():
        return random.choice([
            "America/New_York", "America/Los_Angeles", "Europe/London", "Europe/Paris",
            "Asia/Tokyo", "Asia/Shanghai", "Asia/Kolkata", "Australia/Sydney",
            "America/Chicago", "America/Denver", "Europe/Berlin", "Europe/Moscow",
            "Africa/Johannesburg", "America/Sao_Paulo", "Pacific/Auckland"
        ])

    @staticmethod
    def _hardware_concurrency():
        return random.choice([4, 6, 8, 12, 16, 24, 32, 64])

    @staticmethod
    def _color_depth():
        return random.choice([8, 16, 24, 30, 36, 48])

    def _mouse_moves(self):
        return [{"x": random.randint(0, self.screen_width), "y": random.randint(0, self.screen_height)} for _ in range(random.randint(0, 100))]

    @staticmethod
    def _key_presses():
        return [random.choice(string.ascii_lowercase) for _ in range(random.randint(0, 50))]

    @staticmethod
    def _rand_string(length: int):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @staticmethod
    def _getCookie(session: requests.Session) -> int:
        resp = session.post("https://data.toolbaz.com/info.php?v=1&_v=j101&a=1786349895&t=pageview&_s=1")
        if resp.status_code == 200:
            data = resp.json()
            t_val = data.get("t")
            if t_val is not None:
                return t_val - int(_time())
        return 0

    def generate(self):
        bR6wF = {
            "nV5kP": self.user_agent,
            "lQ9jX": self.language,
            "sD2zR": f"{self.screen_width}x{self.screen_height}",
            "tY4hL": self.time_zone,
            "pL8mC": self.platform,
            "cQ3vD": self.color_depth,
            "hK7jN": self.hardware_concurrency or "unknown",
        }
        uT4bX = {
            "mM9wZ": self.mouse_moves, # mouse movement
            "kP8jY": self.key_presses # keyboard presses
        }

        data = {
            "bR6wF": bR6wF,
            "uT4bX": uT4bX,
            "tuTcS": int(_time()),
            "tDfxy": self._getCookie(self.session),
            "RtyJt": self._rand_string(36)
        }
        encoded = base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()
        return self._rand_string(6) + encoded

class Models:
    # By Google
    gemini_2_5_pro = "gemini-2.5-pro"
    gemini_2_5_flash = "gemini-2.5-flash"
    gemini_2_0_flash_thinking = "gemini-2.0-flash-thinking"
    gemini_2_0_flash = "gemini-2.0-flash"

    # By OpenAI
    gpt_oss_120b = "gpt-oss-120b"
    o3_mini = "o3-mini"
    gpt_4o_latest = "gpt-4o-latest"
    gpt_4o = "gpt-4o"

    # By ToolBaz
    toolbaz_v4 = "toolbaz_v4"
    toolbaz_v3_5_pro = "toolbaz_v3.5_pro"

    # By DeepSeek
    deepseek_v3 = "deepseek-v3"
    deepseek_r1 = "deepseek-r1"

    # By Facebook (Meta)
    llama_4_maverick = "Llama-4-Maverick"
    llama_3_3_70b = "Llama-3.3-70B"

    # Others (Unfiltered)
    l3_70b_euryale_v2_1 = "L3-70B-Euryale-v2.1"
    midnight_rose = "midnight-rose"
    unfiltered_x = "unfiltered_x"

class ToolBaz:
    def __init__(self):
        self.session = requests.Session(impersonate="tor145")
        self.fp = Fingerprint(self.session)

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "DNT": "1",
            "Origin": "https://toolbaz.com",
            "Referer": "https://toolbaz.com/",
            "Sec-CH-UA": '"(Not(A:Brand";v="8", "Chromium";v="98"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "User-Agent": self.fp.user_agent,
        }
        self.session.headers = self.headers
        self.session.cookies.set("SessionID", self.fp.SessionID)
        self.session.cookies.set("tdf", "0")

    def generate(self, prompt, model=Models.gemini_2_0_flash) -> str:
        token_payload = {
            "session_id": self.fp.SessionID,
            "token": self.fp.generate(),
        }
        resp = self.session.post("https://data.toolbaz.com/token.php", data=token_payload)
        if resp.status_code == 200:
            token2 = resp.json().get("token", "")
            if token2:
                write_data = {
                    "text": prompt,
                    "capcha": token2,
                    "model": model,
                    "session_id": self.fp.SessionID,
                }
                resp = self.session.post("https://data.toolbaz.com/writing.php", data=write_data)
                if resp.status_code == 200:
                    text = resp.text.rstrip()
                    lines = text.splitlines()
                    if lines and lines[-1].startswith("[model: ") and lines[-1].endswith("]"):
                        lines.pop()
                    return "\n".join(lines).strip()
                else:
                    raise Exception("[ToolBaz] Write post failed. (Try again.)")
            else:
                raise Exception("[ToolBaz] Token missing from response.")
        else:
            raise Exception("[ToolBaz] Token post failed. (Try again.)")

if __name__ == "__main__":
    toolbaz = ToolBaz()
    print(toolbaz.generate("Hello, how are you?"))
