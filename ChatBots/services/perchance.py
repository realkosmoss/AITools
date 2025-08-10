# https://github.com/King-Chau/text-to-image-generator/tree/main thanksi
import asyncio
import random
import re
import json
import cloudscraper
from patchright.async_api import async_playwright

class CharacterConfig: # For the lore handling
    def __init__(self, user_name="Anon", user_description="", bot_name="Bot", bot_description="", scenario_and_lore=""):
        self.user_name = user_name
        self.user_description = user_description
        self.bot_name = bot_name
        self.bot_description = bot_description
        self.scenario_and_lore = scenario_and_lore

class MessagesHandler:
    def __init__(self, character_config: CharacterConfig = None):
        self.CharacterConfig = character_config or CharacterConfig()
        self.messages = []
        self.start = f"Please write the next 10 messages for the following chat/RP. Most messages should be a medium-length paragraph, including thoughts, actions, and dialogue. Create an engaging, captivating, and genuinely fascinating story. So good that you can't stop reading. Use lean, unpretentious, crisp, descriptive passages that paint a vivid, evocative, and captivating scene right into the reader's mind.\n\n# Reminders:\n- You can use *asterisks* to start and end actions and/or thoughts in typical roleplay style. Most messages should be detailed and descriptive, including dialogue, actions, and thoughts. Utilize all five senses for character experiences.\n- This story never ends. You must keep the story going forever. Drive the story forward, introducing new arcs and events when narratively appropriate. Introduce both external and internal conflicts to drive the story forward and keep things interesting and dynamic. Escalate tensions gradually, creating a sense of anticipation.\n- Aim for superb narrative pacing, and deep worldbuilding. Reveal the world/characters/plot gradually through character interactions and experiences. Allow the reader to discover its intricacies organically (instead of using exposition dumps).\n- Each message should be contained within a single paragraph. Add a blank line between each message. Balance moments of tension and relaxation to maintain reader engagement. Vary sentence and paragraph length to control the rhythm of the roleplay, switching from shorter, punchier sentences to longer, more descriptive ones as appropriate to create interesting variation in pace and structure.\n- Avoid unnecessary and unoriginal repetition of previous messages.\n- Bring characters to life by portraying their unique traits, thoughts, emotions, appearances, and speech patterns realistically. Consider the situation, motivations, and potential consequences. Ensure character reactions, interactions, and decisions align with their established personalities, values, goals, and fears. Use subtle gestures, distinctive quirks, and colloquialisms to create enriched, lifelike scenes. Allow characters' motivations and personalities to evolve authentically throughout the story, creating genuine character arcs.\n- Aggression, graphic violence, character toxicity, and vulgarity are allowed in scenarios with mature themes. Portray conflict realistically - i.e. without shallow resolutions or excessive positivity bias.\n- The overall goal is to create a genuinely fascinating and engaging roleplay/story. So good that you can't stop reading. Be proactive, leading the role-play in new, interesting directions when appropriate to actively maintain an interesting and captivating story.\n- Develop the story in a manner that a skilled author and engaging storyteller would. Craft conversations that reveal character, advance the plot, and feel natural. Use subtext and unique speech patterns to differentiate characters and convey information indirectly.\n- Narrator messages should be longer than normal messages.\n\n# Here's {self.CharacterConfig.bot_name}'s description/personality:\n---\n{self.CharacterConfig.bot_description}\n---\n\n# Here's {self.CharacterConfig.user_name}'s description/personality:\n---\n{self.CharacterConfig.user_description}\n---\n\n# Here's the initial scenario and world info:\n---\n{self.CharacterConfig.scenario_and_lore}\n---\n\n# Here's what has happened so far:\n---\n"
        self.end = f"\n---\n\nYour task is to write the next 10 messages in this chat/roleplay between {self.CharacterConfig.user_name} and {self.CharacterConfig.bot_name}. There should be a blank new line between messages.\nWrite the next 10 messages. Most messages should be a medium-length paragraph, including thoughts, actions, and dialogue."

    def get(self) -> str:
        rp_log = self.start + "\n\n"
        rp_log += "\n\n".join([f"{role}: {msg}" for role, msg in self.messages])
        rp_log += self.end
        return rp_log

    def add(self, message: str, role: str) -> None:
        self.messages.append((role, message))

    def remove(self, count: int = 1) -> None:
        for _ in range(count):
            if len(self.messages) >= 2:
                self.messages.pop()  # Remove bot reply
                self.messages.pop()  # Remove user message

    def clear(self) -> None:
        self.messages.clear()

class PerchanceChatBot:
    def __init__(self, messages: MessagesHandler = None, character_config: CharacterConfig = None):
        """
        You dont need to pass anything, it will create defaults automatically.
        But if you WANT to customize, you can pass your own instances.
        """
        self.CharacterConfig = character_config or CharacterConfig()
        self.MessagesHandler = messages or MessagesHandler(character_config=character_config)
        self.session = cloudscraper.CloudScraper()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "text/plain;charset=UTF-8",
            "DNT": "1",
            "Origin": "https://text-generation.perchance.org",
            "Priority": "u=1, i",
            "Referer": "https://text-generation.perchance.org/embed",
            "Sec-CH-UA": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
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

            await page.goto('https://perchance.org/ai-chat')

            iframe_element = await page.query_selector('xpath=//iframe[@src]')
            if not iframe_element:
                await browser.close()
                raise RuntimeError("iframe not found on the page")

            frame = await iframe_element.content_frame()
            if not frame:
                await browser.close()
                raise RuntimeError("Failed to get iframe content frame")

            await frame.click('xpath=//*[@id="sendMessageBtn"]') # Did it work? I dont know but it seems so lmao.

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

    def _check_cached_key(self, force_new=False):
        try:
            if force_new:
                return None
            with open('chat-perchance-last-key.txt', 'r') as file:
                key = file.readline().strip()
                if key:
                    # Verify if key is still valid
                    verification_url = 'https://text-generation.perchance.org/api/checkUserVerificationStatus'
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
        with open('chat-perchance-last-key.txt', 'w') as file:
            file.write(key)

    def get_access_code(self, force_new=False):
        key = self._check_cached_key(force_new)
        if key:
            return key

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        key = loop.run_until_complete(self._fetch_user_key())
        self._save_key(key)
        return key
    
    def generate(self, message: str):
        generate_url = 'https://text-generation.perchance.org/api/generate'

        user_key = self.get_access_code()

        create_params = {
            'userKey': user_key,
            'thread': 1,
            'requestId': random.random(),
            '__cache_bust': random.random()
        }

        startWith = f'{self.CharacterConfig.user_name}: {message}\n\n{self.CharacterConfig.bot_name}:'
        instruction = self.MessagesHandler.get()
        approxCharsPerToken = 3.4
        
        request_payload = {
            'instruction': instruction,
            'startWith': startWith,
            'stopSequences': [
                '\n\n',
                f"\n{self.CharacterConfig.user_name}:",
                f'\n{self.CharacterConfig.bot_name}:'
            ],
            'generatorName': 'ai-character-chat',
            'startWithTokenCount': round(len(startWith) / approxCharsPerToken),
            'instructionTokenCount': round(len(instruction) / approxCharsPerToken)
        }
        create_response = self.session.post(generate_url, params=create_params, json=request_payload)
        if 'invalid_key' in create_response.text:
            user_key = self.get_access_code(force_new=True)
            create_params['userKey'] = user_key
            create_response = self.session.post(generate_url, params=create_params, json=request_payload)
            if 'invalid_key' in create_response.text:
                raise Exception('Chat could not be generated (invalid key).')
            
        # Shitty ass way to get the full text content
        final_text = ''
        for line in create_response.text.splitlines():
            if not line.strip():
                continue
                
            data = json.loads(line.replace('data:', ''))

            bot_message = data.get('text')
            if not bot_message:
                continue

            final_text += bot_message
            if data.get('final'):
                break
        if final_text: # Check if empty response.
            self.MessagesHandler.add(message, self.CharacterConfig.user_name)
            self.MessagesHandler.add(final_text, self.CharacterConfig.bot_name)
        return final_text

# Example
if __name__ == '__main__':
    characterconfig = CharacterConfig(
        user_name="Anon",
        user_description="Im a very cool Anon!",
        bot_name="Anon girl",
        bot_description="I like Anon because he is cool.",
        scenario_and_lore="We are sitting being cool being Anon's."
    )
    chatbot = PerchanceChatBot(character_config=characterconfig)
    message = chatbot.generate('hi')
    print(message)
