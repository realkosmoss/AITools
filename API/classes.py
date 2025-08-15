from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# /api/generate
class Generate(BaseModel):
    model: str  # (required) the model name
    prompt: str  # the prompt to generate a response for
    suffix: Optional[str] = None  # the text after the model response
    images: Optional[List[str]] = None  # (optional) a list of base64-encoded images (for multimodal models such as llava)
    think: Optional[bool] = False  # (for thinking models) should the model think before responding?
    
    format: Optional[str] = None  # the format to return a response in. Format can be json or a JSON schema
    options: Optional[Dict[str, Any]] = None  # additional model parameters listed in the documentation for the Modelfile such as temperature
    system: Optional[str] = None  # system message to (overrides what is defined in the Modelfile)
    template: Optional[str] = None  # the prompt template to use (overrides what is defined in the Modelfile)
    stream: Optional[bool] = True  # if false the response will be returned as a single response object, rather than a stream of objects
    raw: Optional[bool] = False  # if true no formatting will be applied to the prompt
    keep_alive: Optional[str] = "5m"  # controls how long the model will stay loaded into memory following the request (default: 5m)
    context: Optional[Any] = None  # (deprecated) the context parameter returned from a previous request to /generate

# /api/chat
class Message(BaseModel):
    role: str  # system, user, assistant, or tool
    content: str

class ChatRequest(BaseModel):
    model: str  # required model name
    messages: List[Message]
    stream: Optional[bool] = True
    # Will not work:
    tools: Optional[List[str]] = None
    think: Optional[bool] = False
    format: Optional[str] = None  # json or JSON schema
    options: Optional[dict] = None  # temperature, etc.
    keep_alive: Optional[str] = "5m"  # e.g., "5m" for 5 minutes

class ChatResponse(BaseModel):
    model: str
    created_at: datetime
    message: Message
    done: bool
    total_duration: int  # nanoseconds? (as in your example)
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int
# /api/tags
class ModelDetails(BaseModel):
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str

DUMMY_DETAILS = ModelDetails(
    parent_model="Not implemented on everything",
    format="N/A",
    family="N/A",
    families=["N/A"],
    parameter_size="N/A",
    quantization_level="N/A"
)

class ModelItem(BaseModel):
    name: str  # Model display name
    model: str  # Model identifier
    modified_at: str = "1970-01-01T00:00:00Z"  # Not really needed anyway
    size: int = 690000000  # Size in bytes
    digest: str = "AI-Tools-000"
    details: ModelDetails = DUMMY_DETAILS # Not making this