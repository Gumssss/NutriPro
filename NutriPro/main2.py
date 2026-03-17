import os
import json
import base64
from typing import List, TypedDict, Dict, Any
from dotenv import load_dotenv
from PIL import Image
import io

# Import LangChain and AWS libraries
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# 1. Load environment variables (.env file)
load_dotenv()

# 2. Define global state structure
class AgentState(TypedDict):
    image_base64: str            # Uploaded image (Base64)
    user_profile: Dict[str, Any] # User profile and goals
    ingredients_data: Dict[str, Any] # Output from Agent 1: ingredients + calories
    final_recipes: List[Dict[str, Any]] # Output from Agent 2: recipes
    nutrition_report: str        # Output from Agent 2: summary

# 3. Initialize AWS Bedrock model
# Use latest v2 model to avoid legacy errors
llm = ChatBedrockConverse(
    model="amazon.nova-pro-v1:0",
    region_name="eu-west-2"
)

# --- 4. Define node functions ---

def food_vision_agent(state: AgentState):
    """Agent 1: Detect food ingredients from image"""
    print("--- Running Node: Agent 1 (Vision Parser) ---")
    
    message = HumanMessage(
        content=[
            {
                "type": "text", 
                "text": "Identify all raw food ingredients in this image. Estimate the calories for each one and only output the sum. Return ONLY a JSON object with keys 'ingredients' (list) and 'total_base_calories' (number)."
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{state['image_base64']}"},
            },
        ]
    )
    
    response = llm.invoke([message])
    content = response.content
    print(content)

    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    
    return {"ingredients_data": json.loads(content)}

def nutrition_recipe_agent(state: AgentState):
    """Agent 2: Create meal plan and nutrition advice"""
    print("--- Running Node: Agent 2 (Meal Planner) ---")
    
    ingred_info = state["ingredients_data"]
    profile = state["user_profile"]
    
    prompt = f"""
    You are a Nutritionist and Professional Chef.
    USER PROFILE: {json.dumps(profile)}
    AVAILABLE INGREDIENTS: {json.dumps(ingred_info['ingredients'])} (Total base cal: {ingred_info['total_base_calories']})
    
    Output a raw JSON object with keys 'recipes' (list) and 'summary' (string).
    """
    
    response = llm.invoke(prompt)
    content = response.content
    
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    
    result_data = json.loads(content)
    
    return {
        "final_recipes": result_data.get("recipes", []),
        "nutrition_report": result_data.get("summary", "")
    }

# --- 5. Build workflow (LangGraph) ---

workflow = StateGraph(AgentState)
workflow.add_node("vision_parser", food_vision_agent)
workflow.add_node("meal_planner", nutrition_recipe_agent)
workflow.set_entry_point("vision_parser")
workflow.add_edge("vision_parser", "meal_planner")
workflow.add_edge("meal_planner", END)

app = workflow.compile()

# --- 6. Utility function: convert image to Base64 ---
def encode_image(image_path: str) -> str:
    """Read local image and convert to Base64 (JPEG format)"""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Save as JPEG in memory
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

# --- 7. Run demo (test code) ---
if __name__ == "__main__":
    # Make sure this image exists in your folder
    TEST_IMAGE = "test_food.jpg" 
    
    if os.path.exists(TEST_IMAGE):
        print(f"✅ Found test image: {TEST_IMAGE}")
        img_b64 = encode_image(TEST_IMAGE)
    else:
        print(f"❌ Error: {TEST_IMAGE} not found. Please add an image with this name.")
        # Use a default placeholder image
        img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

    test_input = {
        "image_base64": img_b64,
        "user_profile": {
            "age": 28,
            "weight": 70,
            "gender": "male",
            "goal": "cutting",
            "allergies": ["peanuts"],
            "meal_type": "Dinner"
        }
    }
    
    print("Starting AI Food Agent Pipeline...")
    try:
        final_state = app.invoke(test_input)
        print("\n" + "="*50)
        print("Ingredients detected:", final_state['ingredients_data']['ingredients'])
        print("Suggested recipes:")
        for r in final_state['final_recipes']:
            print(f"- {r.get('name')} (Calories: {r.get('calories')} kcal)")
        print("Nutrition summary:", final_state['nutrition_report'])
        print("="*50)
    except Exception as e:
        print(f"Error during execution: {e}")
