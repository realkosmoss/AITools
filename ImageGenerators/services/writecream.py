from curl_cffi import requests
import uuid
from urllib.parse import urlparse

class WriteCream:
    def __init__(self):
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://www.writecream.com",
            "referer": "https://www.writecream.com/ai-image-generator-free-no-sign-up/",
            "sec-ch-ua": '"Chromium";v="135", "Not-A.Brand";v="8"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/135.0.0.0 Safari/537.36"
            ),
        }
        self.session = requests.Session(impersonate="chrome", headers=self.headers)
    
    def generate(self, prompt: str, aspect_ratio: str = "1:1", hd: str = "1") -> str | None:
        """
        Generate an image and return the direct image link.
        Returns None if generation fails or response is invalid.
        """
        app_id = "jymldhx2"
        cookies = {
            f"gist_identified_{app_id}": "0",
            f"gist_id_{app_id}": str(uuid.uuid4())
        }
        data = {
            "action": "generate_image",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "hd": hd,
        }

        resp = self.session.post(
            "https://www.writecream.com/wp-admin/admin-ajax.php",
            cookies=cookies,
            data=data,
        )
        if resp.status_code != 200:
            raise Exception(f"[WriteCream] Unexpected status code: {resp.status_code}")
        
        try:
            resp_data = resp.json()
        except Exception:
            return None
        
        image_link = resp_data.get("data", {}).get("image_link")
        if not image_link:
            return None

        image_link = image_link.replace("\\/", "/")

        parsed = urlparse(image_link)
        if parsed.scheme != "https" or not parsed.netloc:
            return None
        
        return image_link

# Example:
if __name__ == "__main__":
    writecream = WriteCream()
    prompt = "chicken nugget dancing"
    link = writecream.generate(prompt)
    print("prompt:", prompt, "Image link:", link)