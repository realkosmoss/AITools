# credits:
# https://github.com/AyGemuy/wudyver/blob/master/pages/api/ai/image/veer.js helped me find alot of their parameters.

from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import json

class VheerAES:
    def __init__(self):
        self.password = b"vH33r_2025_AES_GCM_S3cur3_K3y_9X7mP4qR8nT2wE5yU1oI6aS3dF7gH0jK9lZ" # lol chatgpt key
        self.salt = b"vheer-salt-2024"
        self.iterations = 100_000
        self.backend = default_backend()
        self.key = self.derive_key()

    def derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.iterations,
            backend=self.backend
        )
        return kdf.derive(self.password)

    def encrypt(self, plaintext: str) -> str:
        aesgcm = AESGCM(self.key)
        iv = os.urandom(12)
        data = plaintext.encode("utf-8")
        ct = aesgcm.encrypt(iv, data, None)
        encrypted = iv + ct
        return b64encode(encrypted).decode("utf-8")

    def decrypt(self, encrypted_b64: str) -> str:
        aesgcm = AESGCM(self.key)
        encrypted = b64decode(encrypted_b64)
        iv = encrypted[:12]
        ct = encrypted[12:]
        decrypted = aesgcm.decrypt(iv, ct, None)
        return decrypted.decode("utf-8")

VheerCryption = VheerAES()

def build_params(prompt, r, width, height, email, lan_code, member_type, aspect_ratio=None, flux_model=None):
    w = {
        "prompt": prompt,
        "type": r,
        "width": width,
        "height": height,
        "email": email or "",
        "lan_code": lan_code,
        "member_type": member_type
    }

    if r == 1:
        if aspect_ratio is not None:
            w["aspect_ratio"] = aspect_ratio
        if flux_model is not None:
            w["flux_model"] = flux_model
    elif r == 2:
        w["batch_size"] = 4
    elif r == 0:
        pass
    else:
        raise ValueError("Invalid type")

    return w

from curl_cffi import requests
import time

class Vheer:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.7",
            "DNT": "1",
            "Origin": "https://vheer.com",
            "Priority": "u=1, i",
            "Referer": "https://vheer.com/",
            "Sec-CH-UA": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }
        self.session = requests.Session(impersonate="chrome", headers=self.headers, timeout=30)

    def generate(self, prompt: str, width=1024, height=1024, aspect_ratio=1.0) -> str:
        """Returns an link to the image. (Expires after like 5 minutes)"""
        # 1st request
        params = build_params(
            prompt=prompt,
            r=1,
            width=width,
            height=height,
            email="admin@vheer.com", # :troll_face:
            lan_code="en",
            member_type=1,
            aspect_ratio=aspect_ratio,
            flux_model="1" #? (0, 1) havent seen an difference myself
        )

        encrypted_params = VheerCryption.encrypt(json.dumps(params))

        data = { "params": encrypted_params }
        resp = self.session.post("https://access.vheer.com/api/Vheer/UploadByFileNew", data=data) # Here we need to get the "data":{"code":"QF9XH1SU"
        if not resp.status_code == 200:
            raise Exception(f"1st request failed. (status_code={resp.status_code})")
        try:
            resp_json = resp.json()
        except Exception as e:
            raise Exception("Json failed to decode.", resp.text[:100])
        resp_data = resp_json.get("data", {})
        if not resp_data:
            raise Exception("No resp_data. (Json error)")
        resp_code = resp_data.get("code", {})
        if not resp_code:
            raise Exception("Failed to find response code (1st request)")
        # start on the image retrieving request
        encrypted_params = VheerCryption.encrypt(json.dumps({
            "type": 1,  # <- lmaoo, debugged everything just for this to be needed
            "code": resp_code
        }))
        payload = json.dumps([{"params": encrypted_params}])
    
        headers = self.headers.copy()
        headers.update({
            "Accept": "text/x-component",
            "Content-Type": "text/plain;charset=UTF-8",
            "Cookie": "_ez_retention_enabled_25=false",
            "Next-Action": "1eeefc61e5469e1a173b48743a3cb8dd77eed91b", # <- might need to change?
            "Referer": "https://vheer.com/app/text-to-image",
            "Sec-Fetch-Site": "same-origin"
        })
        start_time = time.time()
        while True:
            resp = self.session.post(
                "https://vheer.com/app/text-to-image",
                data=payload,
                headers=headers
            )
            if not resp.status_code == 200:
                raise Exception(f"Damn, image retrieving failed. (status_code={resp.status_code})")
            resp_decoded = resp.content.decode("utf-8")
            json_start = resp_decoded.find('{') # Because their shitty ass response server returns some crap. example: b'0:["$@1",["ijYiwdQBvSMAjXTwg4HxI",null]]\n1:{"message":"Success","data":{"downloadUrls":[...
            try:
                resp_json = json.loads(resp_decoded[json_start:])
            except Exception as e:
                raise json.JSONDecodeError("Json decode error.", e)
            resp_data = resp_json.get("data", {})
            is_done = resp_data.get("status") == "success"
            if is_done:
                urls = resp_data.get("downloadUrls", [])
                if urls:
                    #print(urls)
                    return urls[0]
                else:
                    raise Exception("No image links found.")

            current_time = time.time()
            if current_time - start_time >= 35: # Guess it just errored or sum
                raise Exception("Image gen timeout.")
            time.sleep(5)

# Example:
if __name__ == "__main__":
    vheer = Vheer()
    prompt = "chicken nugget dancing"
    link = vheer.generate(prompt)
    print("prompt:", prompt, "Image link:", link)