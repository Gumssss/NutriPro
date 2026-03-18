import gradio as gr
from botInterface import suggest_recipes

with gr.Blocks(title="Recipe Suggestion Assistant 🍽️") as demo:

    gr.Markdown(
        "Upload a photo of your ingredients, tell us about dietary restrictions "
        "or meal preferences, and optionally provide personal details for more "
        "personalized suggestions."
    )

    # Two-column layout
    with gr.Row():
        # Left column: inputs
        with gr.Column():
            food_image = gr.Image(label="Upload a photo of the ingredients you have")
            meal_type = gr.Radio(
                choices=["Breakfast", "Lunch", "Dinner", "Snack", "Other"],
                label="Meal type"
            )
            dietary_restrictions = gr.Textbox(
                label="Dietary restrictions (optional)",
                placeholder="E.g., vegan, gluten-free, low sugar…"
            )
            meal_preferences = gr.Textbox(
                label="Meal preferences (optional)",
                placeholder="E.g., high-protein, Italian, low-carb, spicy..."
            )

            # Optional personal details in Accordion
            with gr.Accordion("Optional Personal Details", open=False):
                with gr.Row():
                    height_cm = gr.Number(label="Height (cm)")
                    weight_kg = gr.Number(label="Weight (kg)")
                with gr.Row():
                    age = gr.Number(label="Age")
                    gender = gr.Radio(
                        choices=["Male", "Female", "Other"],
                        label="Gender"
                    )

            submit_btn = gr.Button("Get Recipes")

        # Right column: output
        with gr.Column():
            output = gr.Textbox(label="Suggested Recipes", lines=20)

    # Connect the button
    submit_btn.click(
        fn=suggest_recipes,
        inputs=[
            food_image,
            meal_type,
            dietary_restrictions,
            meal_preferences,
            height_cm,
            weight_kg,
            age,
            gender
        ],
        outputs=output
    )

# Launch the app
demo.launch()