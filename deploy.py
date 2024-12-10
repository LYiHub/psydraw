import os

import uvicorn
from langchain_openai import ChatOpenAI

from src.app.api import create_app
from src.model_langchain import HTPModel
import argparse

def get_parse():
    parser = argparse.ArgumentParser(description="HTP Model")
    parser.add_argument("--port", type=int, default=9557, help="Port number")
    
    return parser.parse_args()


TEXT_MODEL = "claude-3-5-sonnet-20240620"
MULTIMODAL_MODEL = "gpt-4o-2024-08-06"

text_model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    model = TEXT_MODEL,
    temperature=0.2,
    top_p = 0.75,
    seed=42,
)
multimodal_model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    model = MULTIMODAL_MODEL,
    temperature=0.2,
    top_p = 0.75,
    seed=42,
)

model = HTPModel(
    text_model=text_model,
    multimodal_model=multimodal_model,
    language="zh",
    use_cache=True
)

config = get_parse()

app = create_app(model)
uvicorn.run(app, host="127.0.0.1", port=config.port, log_level="info")