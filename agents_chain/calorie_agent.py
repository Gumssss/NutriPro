import json
import re  # <-- added to parse kcal numbers from search results
from typing import List, Optional, Union
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
from langchain.tools import tool
from .utils import extract_first_json, Ingredient, AgentState
from langchain_community.tools import DuckDuckGoSearchRun


# Define custom search tool for agent usage
duck_tool = DuckDuckGoSearchRun(description="Only search for calorific information on the give websites")
custom_tool = duck_tool.bind(query_filter="(site:calories.info OR site:webmd.com OR site:myfitnesspal.com)")

@tool("CalorieSearch", description="Search sites for ingredient calorie values")
def calorie_search(query: str) -> str:
    return custom_tool.run(query)
# ----------------------------------------------------------------

# System prompt for agent
SYSTEM_JSON_INSTRUCTION = SystemMessage(
    content=(
        "return a JSON array of these food ingredients only (no extra text). Each ingredient object must have:\n"
        "{\"name\": \"string\", \"quantity\": \"int\", \"calories\": \"int\"}\n\n"
        "Do NOT include any explanation, commentary, markdown, or extra fields. Do NOT include units inside numeric fields. "
        "The calorific value within the JSON must be the calories of the quantity of the food in the JSON. If you cannot produce valid JSON, return []"
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
        result_str = str(result)
        import re
        match = re.search(r"AIMessage\(content='(\[.*?\])", result_str, re.DOTALL)
        if not match:
            raise ValueError("No AIMessage(content=...) JSON found in agent output")
        output = match.group(1)
        json_text = extract_first_json(output)
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
    print("[DEBUG] Final parsed ingredients:", ingredients_out)
    return ingredients_out

# Compatibility wrapper for langgraph node
def calories_node(state: AgentState) -> AgentState:
    ingredients = state.get("ingredients", [])

    primer = state.get("messages", [])  # type: ignore
    ingredients_calories = run_calorie_generator_local(ingredients, conversation_primer=primer)

    state["ingredients"] = ingredients_calories
    state["messages"].append(AIMessage(content=json.dumps(ingredients_calories, ensure_ascii=False)))
    return state
