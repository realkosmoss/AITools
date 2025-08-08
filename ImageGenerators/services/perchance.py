# https://github.com/King-Chau/text-to-image-generator/tree/main thanks, i legit skidded all of this.
import asyncio
import random
import re
from urllib.parse import quote_plus, urlencode
from time import sleep
import cloudscraper
from patchright.async_api import async_playwright

def upload_image_link(session: cloudscraper.CloudScraper, image_url: str):
    """Downloads the image and uploads it to freeimage.host."""
    img_resp = session.get(image_url, stream=True)
    if not img_resp.ok:
        return None
    r = session.post(
        'https://freeimage.host/api/1/upload',
        data={
            'key': '6d207e02198a847aa98d0a2a901485a5',
            'action': 'upload',
            'format': 'json'
        },
        files={
            'source': ('image.jpg', img_resp.content)
        }
    )
    if r.ok:
        return r.json()['image']['url']
    return None

class PerchanceImageGenerator:
    styles = {
        'cinematic': (
            'cinematic shot, dynamic lighting, 75mm, Technicolor, Panavision, cinemascope, sharp focus, fine details, 8k, HDR, realism, realistic, key visual, film still, superb cinematic color grading, depth of field',
            'bad lighting, low-quality, deformed, text, poorly drawn, holding camera, bad art, bad angle, boring, low-resolution, worst quality, bad composition, disfigured'
        ),
        'realistic': (
            'highly realistic, realistic portrait, (nsfw), anatomically correct, realistic photograph, real colors, award winning photo, detailed face, realistic eyes, beautiful, sharp focus, high resolution, volumetric lighting, incredibly detailed, masterpiece, breathtaking, exquisite, great attention to skin and eyes',
            'unrealistic, animated, 3d, sketches, (text), low-quality, deformed, extra limbs, blurry, bad art, (logo), watermark, blurred, cut off, extra fingers, bad quality, distortion of proportions, deformed fingers, elongated body, cropped image, deformed hands, deformed legs, deformed face, twisted fingers, double image, long neck, extra limb, plastic, disfigured, mutation, sloppy, ugly, pixelated, bad hands, aliasing, overexposed, oversaturated, burnt image, fuzzy, poor quality, deformed arms'
        )
    }
    def __init__(self, resolution='512x768', guidance_scale=7):
        self.resolution = resolution
        self.guidance_scale = guidance_scale
        self.session = cloudscraper.CloudScraper()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Priority": "u=0, i",
            "Sec-CH-UA": '"Chromium";v="135", "Not-A.Brand";v="8"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }
        self.session.headers.update(self.headers)

    async def _fetch_user_key(self):
        url_data = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            def request_handler(request):
                url_data.append(request.url)

            page.on("request", request_handler)

            await page.goto('https://perchance.org/ai-text-to-image-generator')

            iframe_element = await page.query_selector('xpath=//iframe[@src]')
            if not iframe_element:
                await browser.close()
                raise RuntimeError("iframe not found on the page")

            frame = await iframe_element.content_frame()
            if not frame:
                await browser.close()
                raise RuntimeError("Failed to get iframe content frame")

            await frame.click('xpath=//button[@id="generateButtonEl"]')

            key = None
            pattern = r'userKey=([a-f\d]{64})'

            for _ in range(60):  # timeout ~60s max
                all_urls = ''.join(url_data)
                keys = re.findall(pattern, all_urls)
                if keys:
                    key = keys[0]
                    break
                url_data.clear()
                await asyncio.sleep(1)

            await browser.close()

            if not key:
                raise RuntimeError("Failed to retrieve userKey within timeout")

            return key

    def _check_cached_key(self):
        try:
            with open('perchance-last-key.txt', 'r') as file:
                key = file.readline().strip()
                if key:
                    # Verify if key is still valid
                    verification_url = 'https://image-generation.perchance.org/api/checkVerificationStatus'
                    params = {
                        'userKey': key,
                        '__cacheBust': random.random()
                    }
                    resp = self.session.get(verification_url, params=params)
                    if 'not_verified' not in resp.text:
                        return key
        except FileNotFoundError:
            pass
        return None

    def _save_key(self, key):
        with open('perchance-last-key.txt', 'w') as file:
            file.write(key)

    def get_access_code(self):
        key = self._check_cached_key()
        if key:
            return key

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        key = loop.run_until_complete(self._fetch_user_key())
        self._save_key(key)
        return key

    def _build_prompts(self, prompt, style, negative_prompt):
        if style == 'RANDOM':
            style_choice = random.choice(list(self.styles.keys()))
        elif style in self.styles:
            style_choice = style
        else:
            raise ValueError(f"Style {style} is not recognized. Choose from {list(self.styles.keys())}")

        prompt_style = self.styles[style_choice][0]
        negative_prompt_style = self.styles[style_choice][1]

        prompt_query = quote_plus(f"{prompt}, {prompt_style}")
        negative_prompt_query = quote_plus(f"{negative_prompt}, {negative_prompt_style}")

        return prompt_query, negative_prompt_query

    def generate(self, amount=1, prompt='RANDOM', negative_prompt='', style='RANDOM'):
        create_url = 'https://image-generation.perchance.org/api/generate'
        download_url = 'https://image-generation.perchance.org/api/downloadTemporaryImage'

        prompt_query, negative_prompt_query = self._build_prompts(prompt, style, negative_prompt)

        for idx in range(1, amount + 1):
            user_key = self.get_access_code()

            create_params = {
                'prompt': prompt_query,
                'negativePrompt': negative_prompt_query,
                'userKey': user_key,
                '__cache_bust': random.random(),
                'seed': '-1',
                'resolution': self.resolution,
                'guidanceScale': str(self.guidance_scale),
                'channel': 'image-generator-professional',
                'subChannel': 'public',
                'requestId': random.random()
            }

            create_response = self.session.get(create_url, params=create_params)
            if 'invalid_key' in create_response.text:
                raise Exception('Image could not be generated (invalid key).')

            retries = 0
            image_id = None
            while retries < 5:
                try:
                    data = create_response.json()
                    if data and 'imageId' in data:
                        image_id = data['imageId']
                        break
                    else:
                        print(f"Attempt {retries+1}: No imageId found, retrying...")
                except Exception as e:
                    print(f"Attempt {retries+1}: JSON parsing error or other exception: {e}")

                retries += 1
                sleep(8)
                create_response = self.session.get(create_url, params=create_params)

            if not image_id:
                raise Exception("Failed to get imageId after retries.")


            download_url = f"{download_url}?{urlencode({'imageId': image_id})}"
            
            permalink = upload_image_link(self.session, download_url)
            if permalink:
                return permalink
            return download_url

if __name__ == "__main__":
    perchance = PerchanceImageGenerator()
    link = perchance.generate(prompt="chicken nugget", style="realistic")
    print(link)