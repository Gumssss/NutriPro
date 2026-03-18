# master_graph.py
import json
from typing import List, Union
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .utils import AgentState, Ingredient
from .food_image_converter import vision_node
from .recipe_agent import recipes_node
from .calorie_agent import calories_node

def build_master_graph():
    graph = StateGraph(AgentState)

    graph.add_node("vision", vision_node)
    graph.add_node("recipes", recipes_node)
    graph.add_node("calories", calories_node)

    graph.add_edge(START, "vision")
    graph.add_edge("vision", "calories")
    graph.add_edge("calories", "recipes")
    graph.add_edge("recipes", END)

    return graph.compile() Generated recipes ---")
