from agents_chain.main_langchain import build_master_graph
import io
from PIL import Image
import numpy as np
#Will contain the functions for talking to the bots
#Change as needed
#The string that is returned will be output to the user

def suggest_recipes(food_image, meal_type, dietary_restrictions, meal_preferences):    
    if food_image is None:
        return "Please upload an image of your ingredients first!"
    
    if isinstance(food_image, np.ndarray):
        food_image = Image.fromarray(food_image)
    # --- Convert PIL image to file-like object ---
    image_bytes = io.BytesIO()
    food_image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    
    # Save temporarily as a file path for the pipeline
    temp_image_path = "temp_food.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(image_bytes.read())

    # --- Build user info dictionary for AI ---
    user_info = {
        "mealtype": meal_type,
        "goal": meal_preferences,
        "dietary_restrictions": dietary_restrictions
        # Add other user info if needed (height, weight, etc.)
    }

    # --- Build and compile the master graph ---
    agent = build_master_graph()

    # --- Prepare initial state ---
    initial_state = {
        "messages": [],  # if your nodes use LLM messages
        "image_path": temp_image_path,
        "user_info": user_info,
        "ingredients": None,
        "recipes": None
    }

    # --- Run the AI pipeline ---
    result_state = agent.invoke(initial_state)

    # --- Extract and format results ---
    ingredients = result_state.get("ingredients", [])
    recipes = result_state.get("recipes", [])

    if not recipes:
        return "The AI could not generate recipes for these ingredients."

    formatted = "Based on your ingredients and preferences:\n\n"
    for i, r in enumerate(recipes, 1):
        name = r.get("name", f"Recipe {i}")
        calories = r.get("calories", "N/A")
        formatted += f"- {name} (Calories: {calories})\n"

    return formatted
