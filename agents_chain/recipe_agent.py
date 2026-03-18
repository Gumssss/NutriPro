# recipes_agent.py
import json
from typing import List, Optional, Union
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .utils import extract_first_json, Ingredient, AgentState

recipe_model = ChatBedrockConverse(
    model="deepseek.v3.2",
    region_name="eu-west-2",
    temperature=0.0,
)

SYSTEM_JSON_INSTRUCTION = SystemMessage(
    content=(
        "You are an assistant that MUST output exactly a single JSON array of length 3 and NOTHING else.\n"
        "The array must contain exactly three objects following this schema:\n\n"
        "[\n"
        "  {\n"
        "    \"name\": \"string\",\n"
        "    \"kcal\": integer,\n"
        "    \"ingredients\": [\n"
        "      {\"name\": \"string\", \"quantity\": \"string\"}\n"
        "    ],\n"
        "    \"instructions\": [\"string\", ...],\n"
        "    \"protein\": number,\n"
        "    \"carbohydrates\": number\n"
        "  }\n"
        "]\n\n"
        "Do NOT include any explanation, commentary, markdown, or extra fields. Do NOT include units inside numeric fields. "
        "Return exactly three recipes that suit the user's provided information and fitness goals. If you cannot produce valid JSON, return []"
    )
)

def run_recipe_generator_local(user_info: dict, ingredients: List[Ingredient], conversation_primer: Optional[List[Union[HumanMessage, SystemMessage]]] = None) -> List[dict]:
    state_messages: List[Union[HumanMessage, SystemMessage]] = []
    if conversation_primer:
        state_messages.extend(conversation_primer)
    state_messages.append(SYSTEM_JSON_INSTRUCTION)

    ingredients_json = json.dumps(ingredients, ensure_ascii=False)
    user_info_text = (
        f"User details:\n"
        f"- Height: {user_info.get('height_cm')}\n"
        f"- Weight: {user_info.get('weight_kg')}\n"
        f"- Meal type: {user_info.get('mealtype')}\n"
        f"- Fitness goal: {user_info.get('goal')}\n\n"
    )
    human_prompt = (
        f"{user_info_text}"
        f"The available ingredients (detected from the image) are given below as a JSON array:\n"
        f"{ingredients_json}\n\n"
        "Generate exactly 3 recipes that use these ingredients where reasonable, following the required JSON schema." \
        "The only assumed ingredients should be oils, and seasonings - everything else must be from the list of ingredients"
    )
    state_messages.append(HumanMessage(content=human_prompt))

    response = recipe_model.invoke(state_messages)
    raw = response.content if hasattr(response, "content") else str(response)

    try:
        json_text = extract_first_json(raw)
        parsed = json.loads(json_text)
        if isinstance(parsed, list):
            return parsed
        else:
            return []
    except Exception:
        return []

# Compatibility wrapper for langgraph node
def recipes_node(state: AgentState) -> AgentState:
    ingredients = state.get("ingredients", [])
    user_info = state.get("user_info", {}) or {}

    primer = state.get("messages", [])  # type: ignore
    recipes = run_recipe_generator_local(user_info, ingredients, conversation_primer=primer)

    state["recipes"] = recipes
    state["messages"].append(AIMessage(content=json.dumps(recipes, ensure_ascii=False)))
    return state