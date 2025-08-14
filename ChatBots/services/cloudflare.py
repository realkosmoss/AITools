from curl_cffi import requests
import time, json
import random, string

def Kx(alphabet: str, size: int):
    def generator():
        return ''.join(random.choice(alphabet) for _ in range(size))
    return generator

def Yx(prefix=None, size=16, alphabet=string.digits + string.ascii_letters, separator='-'):
    n = Kx(alphabet, size)
    if prefix is None:
        return n
    if separator in alphabet:
        raise Exception(f'The separator "{separator}" must not be part of the alphabet "{alphabet}".')
    
    def prefixed_generator():
        return f"{prefix}{separator}{n()}"
    
    return prefixed_generator
hm = Yx()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com/",
    "Priority": "u=0, i",
    "Sec-CH-UA": '"Chromium";v="135", "Not-A.Brand";v="8"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

api_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://playground.ai.cloudflare.com",
    "Referer": "https://playground.ai.cloudflare.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Priority": "u=1, i",
    "Sec-CH-UA": '"Chromium";v="135", "Not-A.Brand";v="8"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

class Messages:
    def __init__(self):
        self.messages = []
    
    def add(self, role, content) -> None:
        self.messages.append({
            "role": role,
            "content": content,
            "parts": [{
                "type": "text",
                "text": content
            }]
        })
    
    def remove(self):
        self.messages.pop()
    
    def _hi(self, role, content) -> list:
        return [{
            "role": role,
            "content": content,
            "parts": [{
                "type": "text",
                "text": content
            }]
        }]

    def get(self) -> list:
        return self.messages

class Models:
    deepseek_coder_6_7b_base_awq = "@hf/thebloke/deepseek-coder-6.7b-base-awq"
    deepseek_coder_6_7b_instruct_awq = "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"
    deepseek_math_7b_instruct = "@cf/deepseek-ai/deepseek-math-7b-instruct"
    deepseek_r1_distill_qwen_32b = "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b"
    discolm_german_7b_v1_awq = "@cf/thebloke/discolm-german-7b-v1-awq"
    falcon_7b_instruct = "@cf/tiiuae/falcon-7b-instruct"
    gemma_3_12b_it = "@cf/google/gemma-3-12b-it"
    gemma_7b_it = "@hf/google/gemma-7b-it"
    hermes_2_pro_mistral_7b = "@hf/nousresearch/hermes-2-pro-mistral-7b"
    llama_2_13b_chat_awq = "@hf/thebloke/llama-2-13b-chat-awq"
    llama_2_7b_chat_fp16 = "@cf/meta/llama-2-7b-chat-fp16"
    llama_2_7b_chat_int8 = "@cf/meta/llama-2-7b-chat-int8"
    llama_3_8b_instruct = "@cf/meta/llama-3-8b-instruct"
    llama_3_8b_instruct_awq = "@cf/meta/llama-3-8b-instruct-awq"
    llama_3_1_8b_instruct_awq = "@cf/meta/llama-3.1-8b-instruct-awq"
    llama_3_1_8b_instruct_fp8 = "@cf/meta/llama-3.1-8b-instruct-fp8"
    llama_3_2_11b_vision_instruct = "@cf/meta/llama-3.2-11b-vision-instruct"
    llama_3_2_1b_instruct = "@cf/meta/llama-3.2-1b-instruct"
    llama_3_2_3b_instruct = "@cf/meta/llama-3.2-3b-instruct"
    llama_3_3_70b_instruct_fp8_fast = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    llama_4_scout_17b_16e_instruct = "@cf/meta/llama-4-scout-17b-16e-instruct"
    llama_guard_3_8b = "@cf/meta/llama-guard-3-8b"
    llamaguard_7b_awq = "@hf/thebloke/llamaguard-7b-awq"
    meta_llama_3_8b_instruct = "@hf/meta-llama/meta-llama-3-8b-instruct"
    mistral_7b_instruct_v0_1 = "@cf/mistral/mistral-7b-instruct-v0.1"
    mistral_7b_instruct_v0_1_awq = "@hf/thebloke/mistral-7b-instruct-v0.1-awq"
    mistral_7b_instruct_v0_2 = "@hf/mistral/mistral-7b-instruct-v0.2"
    mistral_small_3_1_24b_instruct = "@cf/mistralai/mistral-small-3.1-24b-instruct"
    neural_chat_7b_v3_1_awq = "@hf/thebloke/neural-chat-7b-v3-1-awq"
    openchat_3_5_0106 = "@cf/openchat/openchat-3.5-0106"
    openhermes_2_5_mistral_7b_awq = "@hf/thebloke/openhermes-2.5-mistral-7b-awq"
    phi_2 = "@cf/microsoft/phi-2"
    qwen1_5_0_5b_chat = "@cf/qwen/qwen1.5-0.5b-chat"
    qwen1_5_1_8b_chat = "@cf/qwen/qwen1.5-1.8b-chat"
    qwen1_5_14b_chat_awq = "@cf/qwen/qwen1.5-14b-chat-awq"
    qwen1_5_7b_chat_awq = "@cf/qwen/qwen1.5-7b-chat-awq"
    qwen2_5_coder_32b_instruct = "@cf/qwen/qwen2.5-coder-32b-instruct"
    qwq_32b = "@cf/qwen/qwq-32b"
    sqlcoder_7b_2 = "@cf/defog/sqlcoder-7b-2"
    starling_lm_7b_beta = "@hf/nexusflow/starling-lm-7b-beta"
    tinyllama_1_1b_chat_v1_0 = "@cf/tinyllama/tinyllama-1.1b-chat-v1.0"
    una_cybertron_7b_v2_bf16 = "@cf/fblgit/una-cybertron-7b-v2-bf16"
    zephyr_7b_beta_awq = "@hf/thebloke/zephyr-7b-beta-awq"

class Payload:
    @staticmethod
    def generate(
        id: int,
        messages: list = None,
        **kwargs
    ) -> dict:
        payload = {
            "id": id,
            "lora": None,
            "max_tokens": 2048,
            "messages": messages,
            "model": Models.llama_4_scout_17b_16e_instruct,
            "stream": True,
            "system_message": "You are a helpful assistant",
            "tools": []
        }
        payload.update(kwargs)
        return payload
    
class Cloudflare:
    def __init__(self):
        self.session = requests.Session(impersonate="chrome", headers=headers)
        self.session.get("https://playground.ai.cloudflare.com/")
        
        self.id = hm()
        self.messages = Messages()
    
    def generate(self, prompt, api=False, **kwargs) -> str | dict:
        """api=True returns a dict with messageId, text, and token usage."""
        # Build payload
        messages = self.messages.get() + self.messages._hi(role="user", content=prompt)
        payload = Payload.generate(id=self.id, messages=messages, **kwargs)

        resp = self.session.post(
            "https://playground.ai.cloudflare.com/api/inference",
            headers=api_headers,
            json=payload
        )
        if resp.status_code == 403: # Anti bot
            time.sleep(5)
            resp = self.session.post(
                "https://playground.ai.cloudflare.com/api/inference",
                headers=api_headers,
                json=payload
            )

        message_id = None
        chunks = []
        prompt_tokens = None
        completion_tokens = None

        for line in resp.text.splitlines():
            line = line.strip()
            if "200 f:" in line or "f:{" in line:
                message_id = line.replace('200', '').replace('f:', '').strip()
                try:
                    message_id = json.loads(message_id).get("messageId")
                except json.JSONDecodeError:
                    message_id = None

            elif line.startswith("0:"):
                chunk = line[2:].strip()
                if chunk.startswith('"') and chunk.endswith('"'):
                    chunk = chunk[1:-1]
                chunks.append(chunk)

            elif line.startswith(("e:", "d:")):
                try:
                    data = json.loads(line.split(":", 1)[1])
                    usage = data.get("usage", {})
                    if usage:
                        prompt_tokens = usage.get("promptTokens")
                        completion_tokens = usage.get("completionTokens")
                except json.JSONDecodeError:
                    pass

        ai_response = "".join(chunks)

        if api:
            return {
                "messageId": message_id,
                "text": ai_response,
                "promptTokens": prompt_tokens,
                "completionTokens": completion_tokens
            }

        return ai_response

if __name__ == "__main__":
    cf = Cloudflare()
    response = cf.generate(
        "Hello!",
        max_tokens=690,
        model=Models.llama_4_scout_17b_16e_instruct,
        stream=True,
        system_message="You are an Llama 4 scout 17b. You always brag about how cool your model is."
    )
    print(response)
    # or just
    response = cf.generate(
        "Hello!",
        model=Models.llama_4_scout_17b_16e_instruct,
    )
    print(response)
