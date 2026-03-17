import gradio as gr

# Placeholder "black box" function
def suggest_recipes(food_image, meal_preferences):    
    #food_image: PIL image object
    #meal_preferences: string
    
    # Will be AI/recipe logic
    # For now return a dummy message
    return (
        "Based on the ingredients you provided and your preferences:\n\n"
        "- Recipe 1: Delicious stir-fry with the vegetables you have.\n"
        "- Recipe 2: Simple pasta dish tailored to your requirements.\n"
        "- Recipe 3: Quick salad using your available ingredients.\n\n"
        "Feel free to experiment and adjust spices or sauces to taste!"
    )

#Create Gradio interface
demo = gr.Interface(
    fn=suggest_recipes,
    inputs=[
        gr.Image(label="Upload a photo of the ingredients you have"),
        gr.Textbox(
            label="Enter your meal preferences or dietary requirements",
            placeholder="e.g., vegetarian, low-carb, spicy, gluten-free...")
    ],
    outputs=gr.Textbox(label="Suggested Recipes"),
    title="Recipe Suggestion Assistant 🍽️",
    description=(
        "Upload a photo of the ingredients you have on hand, "
        "then tell us any dietary restrictions or preferences. "
        "Our assistant will suggest some recipe ideas for you!"
    ),
    flagging_mode="never"  #prevents user flagging in UI
)

#Launch the app
demo.launch()
