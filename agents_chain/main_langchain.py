# master_graph.py
import json
from typing import List, Union
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils import AgentState, Ingredient
from food_image_converter import vision_node
from recipe_agent import recipes_node

def build_master_graph():
    graph = StateGraph(AgentState)

    graph.add_node("vision", vision_node)
    graph.add_node("recipes", recipes_node)

    graph.add_edge(START, "vision")
    graph.add_edge("vision", "recipes")
    graph.add_edge("recipes", END)

    return graph.compile()

if __name__ == "__main__":
    agent = build_master_graph()

    # Build initial state with user info and image path
    image_path = input("Path to image: ").strip()
    height = input("Height (cm): ").strip()
    weight = input("Weight (kg): ").strip()
    mealtype = input("Meal type (breakfast/lunch/dinner): ").strip()
    goal = input("Fitness goal: ").strip()

    user_info = {
        "height_cm": height,
        "weight_kg": weight,
        "mealtype": mealtype,
        "goal": goal
    }

    initial_state: AgentState = {
        "messages": [],          
        "image_path": image_path,
        "user_info": user_info,
        "ingredients": None,
        "recipes": None
    }

    result_state = agent.invoke(initial_state)

    print("\n--- Detected ingredients ---")
    print(json.dumps(result_state.get("ingredients", []), indent=2, ensure_ascii=False))

    print("\n--- Generated recipes ---")
    print(json.dumps(result_state.get("recipes", []), indent=2, ensure_ascii=False))