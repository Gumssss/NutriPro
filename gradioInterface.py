import gradio as gr
from botInterface import suggest_recipes

# Placeholder "black box" function


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
