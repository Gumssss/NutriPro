import gradio as gr
from botInterface import suggest_recipes

# Placeholder "black box" function


#Create Gradio interface
demo = gr.Interface(
    fn=suggest_recipes,
    inputs=[
        gr.Image(label="Upload a photo of the ingredients you have"),
        gr.Radio(choices=["Breakfast", "Lunch", "Dinner", "Snack", "Other"], label="Meal type"),
        gr.Textbox(
            label="Dietary restrictions",
            placeholder="E.g., vegan, gluten-free, low sugar…"),
        gr.Textbox(
            label="Enter your meal preferences",
            placeholder="e.g., high-protein, italian, low-carb, spicy...")
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
