# utils.py
import base64
import re
from io import BytesIO
from typing import List, TypedDict, Union, Optional
from PIL import Image
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class Ingredient(TypedDict):
    name: str
    quantity: str

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]
    image_path: Optional[str]
    user_info: Optional[dict]
    ingredients: Optional[List[Ingredient]]
    recipes: Optional[list]
    #chat_history: Optional[List[BaseMessage]] #Uncomment this line when you are ready to integrate chatbot

def extract_first_json(text: str) -> str:
    text = text.strip()
    array_match = re.search(r'(\[.*\])', text, flags=re.DOTALL)
    if array_match:
        return array_match.group(1)
    obj_match = re.search(r'(\{.*\})', text, flags=re.DOTALL)
    if obj_match:
        return obj_match.group(1)
    raise ValueError("No JSON found in text")

def encode_image(image_path: str) -> str:
    """Read local image and convert to Base64 (JPEG format)"""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Save as JPEG in memory
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")
