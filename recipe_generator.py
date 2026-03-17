from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict, List, Union
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END

import json
import re

# ---------------------
# Data model
# ---------------------
class Ingredient(TypedDict):
    name: str
    quantity: str

class Recipes(TypedDict):
    name: str
    kcal: int
    ingredients: List[Ingredient]
    instructions: List[str]
    protein: float
    carbohydrates: float

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]

# Strict system message: require ONLY JSON (no extra text), exactly 3 recipes
SYSTEM_JSON_INSTRUCTION = SystemMessage(
    content=(
        "You are an assistant that MUST output exactly a single JSON array of length 3 and NOTHING else. "
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
        "Do NOT repeat any fields within a single recipe"
        "Return exactly three recipes that suit the user's provided information, and fitness goals. "
        "Do NOT repeat recipes"
        "If you cannot produce valid JSON, return an empty JSON array []."
    )
)

chat = ChatBedrockConverse(
    model="deepseek.v3.2",
    region_name="eu-west-2",
    temperature=0.0,
    max_tokens=None,
)

def extract_first_json(text: str) -> str:
    """
    Extract the first JSON array/object from text. Returns substring or raises ValueError.
    """
    # find the first '[' or '{' that starts a JSON structure and match to its closing bracket
    text = text.strip()
    # try to find a JSON array first
    array_match = re.search(r'(\[.*\])', text, flags=re.DOTALL)
    if array_match:
        return array_match.group(1)
    # fallback to object
    obj_match = re.search(r'(\{.*\})', text, flags=re.DOTALL)
    if obj_match:
        return obj_match.group(1)
    raise ValueError("No JSON found in text")

def processing_node(state: AgentState) -> AgentState:
    response = chat.invoke(state["messages"])
    raw = response.content if hasattr(response, "content") else str(response)
    # store raw assistant text for traceability
    state["messages"].append(AIMessage(content=raw))

    # Attempt to extract and parse JSON
    try:
        json_text = extract_first_json(raw)
        parsed = json.loads(json_text)
    except Exception as e:
        print("Failed to parse JSON from model response:", e)
        print("ERROR: couldn't get a valid JSON array of 3 recipes. Last assistant output:\n", raw)
        return state

    # At this point parsed is a valid list[Recipes]. You can proceed to use it.
    # For example, pretty-print it:
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    # Optionally, if you want to add the structured recipes back into state as an AIMessage with JSON only:
    state["messages"].append(AIMessage(content=json.dumps(parsed, ensure_ascii=False)))
    return state

# Build the graph/agent
graph = StateGraph(AgentState)
graph.add_node("node1", processing_node)
graph.add_edge(START, "node1")
graph.add_edge("node1", END)
agent = graph.compile()

# start conversation history with the strict system instruction
conversation_history = [SYSTEM_JSON_INSTRUCTION]

# main loop
prompt_template = PromptTemplate.from_template(
    "User details:\n"
    "- Height: {height} cm\n"
    "- Weight: {weight} kg\n"
    "- Meal type: {mealtype}\n"
    "- Fitness goal: {goal}\n\n"
    "Generate exactly 3 recipes following the required JSON schema."
)

height = input("Height (cm): ").strip()
weight = input("Weight (kg): ").strip()
mealtype = input("Meal type (breakfast/lunch/dinner): ").strip()
goal = input("Fitness goal: ").strip()

formatted_prompt = prompt_template.format(
    height=height,
    weight=weight,
    mealtype=mealtype,
    goal=goal
)

while True:
    conversation_history.append(HumanMessage(content=formatted_prompt))

    agent.invoke({"messages": conversation_history})

    retry = input("More Recipes? (y/n): ").strip().lower()
    if retry != "y":
        break