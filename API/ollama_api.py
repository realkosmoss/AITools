import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from typing import List
import re
from datetime import datetime
import time

# Services
# Chat
from ChatBots.services.cloudflare import Cloudflare, Models as CFModels
from ChatBots.services.deepai import DeepAI, DeepAIModels
from ChatBots.services.toolbaz import ToolBaz, Models as TBModels

# Defined services:
cloudflare = Cloudflare()
deepai = DeepAI(handle_messages_list=False)
toolbaz = ToolBaz()

# Classes
import classes

app = FastAPI(title="AITools API", version="1.0.0")

all_models = [CFModels, DeepAIModels]
all_models_services = {
    cloudflare: CFModels,
    deepai: DeepAIModels,
    toolbaz: TBModels
}

@app.api_route("/", methods=["GET", "HEAD"])
def main():
    return {"message": "Hello, world!"}

@app.post("/api/generate")
def generate(data: classes.Generate):
    date_rn = datetime.now().isoformat() + "Z"
    time_start = time.time_ns()


    selected_service = None
    selected_model_value = None

    for service, model_class in all_models_services.items():
        for key, value in vars(model_class).items():
            if not key.startswith("__") and key == data.model:
                selected_service = service
                selected_model_value = value
                break
        if selected_service:
            break

    if not selected_service:
        return {"error": f"model '{data.model}' not found"}
    if selected_service == deepai:
        model_attr = getattr(DeepAIModels, data.model)
        deepai.model = model_attr
        result = selected_service.generate(prompt=data.prompt)
    elif selected_service == cloudflare:
        real_model = selected_model_value.split("/")[-1]
        real_model = re.sub(r"\.", "_", real_model)
        real_model = real_model.replace("-", "_")
        model_attr = getattr(CFModels, real_model)
        result = selected_service.generate(prompt=data.prompt, api=False, model=model_attr) or selected_service.generate(prompt=data.prompt, api=False, model=model_attr)
    elif selected_service == toolbaz:
        model_attr = getattr(TBModels, data.model)
        result = selected_service.generate(prompt=data.prompt, model=model_attr)
    total_time = time.time_ns() - time_start
    return_json = {
        "model": data.model,
        "created_at": date_rn,
        "response": result,
        "done": True,
        "total_duration": total_time,
        "load_duration": total_time,
        "prompt_eval_count": 420,
        "prompt_eval_duration": total_time,
        "eval_count": 69,
        "eval_duration": total_time
    }
    return JSONResponse(content=return_json)#
# /api/chat
@app.post("/api/chat")
def chat(data: classes.ChatRequest):
    date_rn = datetime.now().isoformat() + "Z"
    time_start = time.time_ns()
    selected_service = None
    selected_model_value = None

    for service, model_class in all_models_services.items():
        for key, value in vars(model_class).items():
            if not key.startswith("__") and key == data.model:
                selected_service = service
                selected_model_value = value
                break
        if selected_service:
            break

    if not selected_service:
        return {"error": f"model '{data.model}' not found"}
    
    messages = data.messages.copy()
    prompt = messages[-1] if messages else None
    if prompt and prompt.role == "user":
        messages.pop() # Idfk how it handles ASSISTANT but WHO THE FUCK CARES, i need to rewrite all the services for this.
    if selected_service == deepai:
        deepai.MessagesHandler.messages = messages
        model_attr = getattr(DeepAIModels, data.model)
        deepai.model = model_attr
        result = selected_service.generate(prompt=prompt.content)
    elif selected_service == cloudflare:
        real_model = selected_model_value.split("/")[-1]
        real_model = re.sub(r"\.", "_", real_model)
        real_model = real_model.replace("-", "_")
        model_attr = getattr(CFModels, real_model)
        result = selected_service.generate(prompt=prompt.content, api=False, model=model_attr) or selected_service.generate(prompt=prompt.content, api=False, model=model_attr)
    elif selected_service == toolbaz:
        model_attr = getattr(TBModels, data.model)
        result = selected_service.generate(prompt=prompt.content, model=model_attr)
    total_time = time.time_ns() - time_start
    response_json = {
        "model": data.model,
        "created_at": date_rn,
        "message": {
            "role": "assistant",
            "content": result.encode("utf-8").decode("utf-8")
        },
        "done": True,
        "total_duration": total_time,
        "load_duration": total_time,
        "prompt_eval_count": 420,
        "prompt_eval_duration": total_time,
        "eval_count": 69,
        "eval_duration": total_time
    }
    return JSONResponse(content=response_json)
# /api/tags
@app.api_route("/api/tags", methods=["GET", "HEAD"])
def get_tags():
    model_items: List[classes.ModelItem] = []

    for models in all_models:
        model_items.extend([
            classes.ModelItem(name=key, model=value)
            for key, value in vars(models).items()
            if not key.startswith("__")
        ])
    
    return JSONResponse(content={"models": [item.model_dump() for item in model_items]})
# /api/show
@app.api_route("/api/show", methods=["GET", "HEAD", "POST"])
def show(): # just for show.
    response_json = {
        "modelfile": "no",
        "parameters": "num_keep                       24\nstop                           \"<|start_header_id|>\"\nstop                           \"<|end_header_id|>\"\nstop                           \"<|eot_id|>\"",
        "template": "{{ if .System }}<|start_header_id|>system<|end_header_id|>\n\n{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>\n\n{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ .Response }}<|eot_id|>",
        "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
            "llama"
            ],
            "parameter_size": "8.0B",
            "quantization_level": "Q4_0"
        },
        "model_info": {
            "general.architecture": "llama",
            "general.file_type": 2,
            "general.parameter_count": 8030261248,
            "general.quantization_version": 2,
            "llama.attention.head_count": 32,
            "llama.attention.head_count_kv": 8,
            "llama.attention.layer_norm_rms_epsilon": 0.00001,
            "llama.block_count": 32,
            "llama.context_length": 8192,
            "llama.embedding_length": 4096,
            "llama.feed_forward_length": 14336,
            "llama.rope.dimension_count": 128,
            "llama.rope.freq_base": 500000,
            "llama.vocab_size": 128256,
            "tokenizer.ggml.bos_token_id": 128000,
            "tokenizer.ggml.eos_token_id": 128009,
            "tokenizer.ggml.merges": [],
            "tokenizer.ggml.model": "gpt2",
            "tokenizer.ggml.pre": "llama-bpe",
            "tokenizer.ggml.token_type": [],
            "tokenizer.ggml.tokens": []
        },
        "capabilities": [
            "completion",
            "chat"
        ],
    }
    return JSONResponse(content=response_json)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ollama_api:app", host="0.0.0.0", port=11434, reload=False)