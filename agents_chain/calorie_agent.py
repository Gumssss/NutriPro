import json
from typing import List, Optional, Union
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
from langchain.tools import tool
from .utils import extract_first_json, Ingredient, AgentState
# Define custom search tool for agent usage
from urllib.parse import urlparse
from langchain_core.tools import tool
from ddgs import DDGS

ALLOWED_DOMAINS = {
    "calories.info",
    "webmd.com",
    "myfitnesspal.com",
}

def _normalize_host(url: str) -> str:
    host = urlparse(url).netloc.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host

def _domain_allowed(url: str) -> bool:
    return _normalize_host(url) in ALLOWED_DOMAINS

def _site_query(query: str) -> str:
    site_part = " OR ".join(f"site:{domain}" for domain in sorted(ALLOWED_DOMAINS))
    return f"({query}) ({site_part})"

@tool(
    "CalorieSearch",
    description="Search only calories.info, webmd.com, and myfitnesspal.com",
)
def calorie_search(query: str) -> str:
    search_query = _site_query(query)

    try:
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(search_query, max_results=10))
    except Exception as e:
        return json.dumps({"error": f"search failed: {str(e)}"}, indent=2)

    filtered = []
    for r in raw_results:
        url = r.get("href") or r.get("link") or ""
        if url and _domain_allowed(url):
            filtered.append(
                {
                    "title": r.get("title", ""),
                    "link": url,
                    "snippet": r.get("body") or r.get("snippet") or "",
                }
            )

    return json.dumps(filtered, indent=2)
# ----------------------------------------------------------------

# System prompt for agent
SYSTEM_JSON_INSTRUCTION = SystemMessage(
    content=(
        "return a JSON array of these food ingredients only (no extra text). Each ingredient object must have:\n"
        "{\"name\": \"string\", \"quantity\": \"int\", \"calories\": \"int\"}\n\n"
        "Do NOT include any explanation, commentary, markdown, or extra fields. Do NOT include units inside numeric fields. "
        "The calorific value within the JSON must be the calories of the quantity of the food in the JSON"
    )
)

# LLM for agent
recipe_model = ChatBedrockConverse(
    model="qwen.qwen3-vl-235b-a22b",
    region_name="eu-west-2",
    temperature=0.0,
)

# Create agent with tool
agent = create_agent(
    recipe_model,
    tools=[calorie_search],
    system_prompt=SYSTEM_JSON_INSTRUCTION,
)


def run_calorie_generator_local(ingredients: List[Ingredient], conversation_primer: Optional[List[Union[HumanMessage, SystemMessage]]] = None) -> List[dict]:
    ingredients_json = json.dumps(ingredients, ensure_ascii=False)
    prompt = (
        f"The available ingredients (detected from the image) are given below as a JSON array:\n"
        f"{ingredients_json}\n\n"
        f"Using the information above, and the online search information, find the calories of each ingredient eact to its quantity. "
        "You may use the CalorieSearch tool to search calories.info for each ingredient. "
        "Return a JSON array of these food ingredients only (no extra text). Each ingredient object must have:\n"
        "{\"name\": \"string\", \"quantity\": \"int\", \"calories\": \"int\"}\n\n"
    )
    result = agent.invoke({"messages": [HumanMessage(content=prompt)]})
    try:
        # Always convert to string and use regex to extract AIMessage(content=...)
        ai_msg = next(
            (m for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
            None,
        )
        if ai_msg is None:
            print("[DEBUG] No AIMessage found in result:", result)
            return []

        content = ai_msg.content
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False)

        json_text = extract_first_json(content)
        parsed = json.loads(json_text)
        ingredients_out: List[Ingredient] = []
        if isinstance(parsed, list):
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                qty = item.get("quantity")
                cal = item.get("calories")
                if name:
                    ingredients_out.append(Ingredient(name=name, quantity=str(qty), calories=str(cal)))
        else:
            ingredients_out = []
    except Exception as e:
        print("[DEBUG] Exception in calorie agent:", e)
        return []
    print("[DEBUG] Final parsed ingredients Calorie Agent:", ingredients_out)
    return ingredients_out

# Compatibility wrapper for langgraph node
def calories_node(state: AgentState) -> AgentState:
    ingredients = state.get("ingredients", [])

    primer = state.get("messages", [])  # type: ignore
    ingredients_calories = run_calorie_generator_local(ingredients, conversation_primer=primer)

    state["ingredients"] = ingredients_calories
    state["messages"].append(AIMessage(content=json.dumps(ingredients_calories, ensure_ascii=False)))
    return state
