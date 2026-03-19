from agents_chain.main_langchain import build_master_graph
import io
from PIL import Image
import numpy as np
#Contain the functions for talking to the bots
#The string that is returned will be output to the user

def suggest_recipes(food_image, meal_type, dietary_restrictions, meal_preferences,height_cm=None,weight_kg=None,age=None,gender=None):    
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

    # Add optional details if provided
    if height_cm is not None:
        user_info["height_cm"] = height_cm
    if weight_kg is not None:
        user_info["weight_kg"] = weight_kg
    if age is not None:
        user_info["age"] = age
    if gender is not None:
        user_info["gender"] = gender

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


    # Build a list of recipe names at the top
    recipe_names = [r.get("name", f"Recipe {i+1}") for i, r in enumerate(recipes)]
    formatted = "**Based on your ingredients and preferences here are your recommended recipes:** \n" + " | ".join(recipe_names) + "\n\n"

    for i, r in enumerate(recipes, 1):
        formatted += "-"*60 + "\n"
        name = r.get("name", f"Recipe {i}")
        recipe_steps = r.get("instructions", [])
        calories = r.get("kcal", "N/A")
        recipe_ingredients = r.get("ingredients", [])  # list of ingredients

        # Format steps as bullets
        steps = "\n".join([f"- {step}" for step in recipe_steps])

        # Ingredients as bullets
        ingredients_list = "\n".join([
            f"- {ing.get('name', 'Unknown')}: {ing.get('quantity', '') if ing.get('quantity','')[-1] == "g" else ing.get('quantity','') + "g"}" 
            for ing in recipe_ingredients
        ])

        # Combine everything
        formatted += f"**{name}** (Calories: {calories})\n{'-'*30}\n"
        if ingredients_list:
            formatted += f"**Ingredients:**\n{ingredients_list}\n{'-'*30}\n"
        formatted += f"**Recipe:**\n{steps}\n\n"

    return formatted

