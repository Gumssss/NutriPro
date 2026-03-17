import json
from typing import List, Optional, Union
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils import extract_first_json, encode_image, Ingredient, AgentState

vision_model = ChatBedrockConverse(
    model="amazon.nova-pro-v1:0",
    region_name="eu-west-2",
    temperature=0.0,
)

FOOD_SYSTEM_MESSAGE = SystemMessage(
    content=(
        "This is a VISION-ONLY agent, and cannot assume the existance of items"
        "Identify all raw food ingredients and their quantities in grams in this image."
        "return a JSON array of these food ingredients only (no extra text). Each ingredient object must have:\n"
        "{\"name\": \"string\", \"quantity\": \"int\"}\n\n"
    )
)

def run_foodvision_on_image_local(image_path: str, conversation_primer: Optional[List[Union[HumanMessage, SystemMessage]]] = None) -> List[Ingredient]:
    state_messages: List[Union[HumanMessage, SystemMessage]] = []
    if conversation_primer:
        state_messages.extend(conversation_primer)
    state_messages.append(FOOD_SYSTEM_MESSAGE)

    b64 = encode_image(image_path)
    content = [
        {"type": "text", "text": "Please parse the image and return ONLY the JSON array as instructed by system message. Calculate the overall quantity in grams"
        "by estimating the weight of a single item and multiplying it by the number of items of that type present in the picture"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
    ]
    image_message = HumanMessage(content=content)
    state_messages.append(image_message)

    response = vision_model.invoke(state_messages)
    raw = response.content if hasattr(response, "content") else str(response)

    try:
        json_text = extract_first_json(raw)
        parsed = json.loads(json_text)
        ingredients: List[Ingredient] = []
        if isinstance(parsed, list):
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                qty = item.get("quantity")
                if name:
                    ingredients.append(Ingredient(name=name, quantity=str(qty)))
        else:
            ingredients = []
    except Exception:
        ingredients = []

    return ingredients

# Compatibility wrapper for langgraph node
def vision_node(state: AgentState) -> AgentState:
    image_path = state.get("image_path")
    if not image_path:
        state["messages"].append(AIMessage(content="[]"))
        state["ingredients"] = []
        return state

    # optional: pass any existing messages as primer
    primer = state.get("messages", [])  # type: ignore
    ingredients = run_foodvision_on_image_local(image_path, conversation_primer=primer)

    # append raw structured outputs for traceability
    state["ingredients"] = ingredients
    state["messages"].append(AIMessage(content=json.dumps(ingredients, ensure_ascii=False)))
    return state