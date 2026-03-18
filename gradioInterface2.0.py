import gradio as gr
from botInterface import suggest_recipes

# 1. Theme and Advanced CSS Configuration
theme = gr.themes.Default(
    font=["Poppins", "sans-serif"],
    primary_hue=gr.themes.colors.yellow,
)

css = """
/* Full-screen container adaptation */
.gradio-container { 
    max-width: 100% !important; 
    margin: 0 !important; 
    padding: 30px 50px !important; 
    min-height: 100vh !important; 
    background-color: #F1EFE6 !important; 
}

/* Header area */
.header-text { text-align: center; margin-bottom: 30px; }
.header-text h1 { color: #2D2D2D !important; font-weight: 800 !important; font-size: 3rem !important; margin-bottom: 10px; }
.header-text p { color: #8A8A8A !important; font-size: 1.1rem !important; max-width: 800px; margin: auto; }

/* Advanced white card */
.custom-card { 
    background-color: #FFFFFF !important; 
    border-radius: 28px !important; 
    border: none !important; 
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.04) !important; 
    padding: 25px !important;
    margin-bottom: 20px !important;
}

/* Button design */
.submit-btn { 
    background-color: #2D2D2D !important; 
    color: #FFFFFF !important; 
    border-radius: 50px !important; 
    font-weight: 600 !important;
    border: none !important;
}
.clear-btn { 
    background-color: #E0E0E0 !important; 
    color: #2D2D2D !important; 
    border-radius: 50px !important; 
    font-weight: 600 !important;
    border: none !important;
}

/* Result output box - yellow highlight */
#output-card { 
    border: 2.5px solid #FCD635 !important; 
    border-radius: 20px !important;
    background-color: #FFFFFF !important;
}

/* Fix accordion panel style to integrate into card */
.gr-accordion { border: 1px solid #E5E5E5 !important; border-radius: 15px !important; overflow: hidden; }
input, textarea, .gr-number-input { border-radius: 12px !important; border-color: #E5E5E5 !important; }
"""

# 2. Build Interface
with gr.Blocks(title="JOE") as demo:
    
    # Top title
    with gr.Column(elem_classes="header-text"):
        gr.Markdown("# JOE")
        gr.Markdown(
            "Hi, I'm JOE, an AI Recipe Suggestion Assistant developed by Johnny, Oisin, and Elliot! "
            
        )

    with gr.Row(equal_height=True):
        # Left: Input area
        with gr.Column(scale=1):
            with gr.Column(variant="panel", elem_classes="custom-card"):
                gr.Markdown("### 📸 Ingredients")
                food_image = gr.Image(label="Ingredients Photo", type="pil", show_label=False)
                
                meal_type = gr.Radio(
                    choices=["Breakfast", "Lunch", "Dinner", "Snack", "Other"],
                    label="Meal type",
                    value="Lunch"
                )
                
                dietary_restrictions = gr.Textbox(
                    label="Dietary restrictions (optional)",
                    placeholder="E.g., vegan, gluten-free..."
                )
                
                meal_preferences = gr.Textbox(
                    label="Meal preferences (optional)",
                    placeholder="E.g., high-protein, Italian..."
                )

                # Body data accordion
                with gr.Accordion("👤 Optional Personal Details", open=False):
                    with gr.Row():
                        height_cm = gr.Number(label="Height (cm)")
                        weight_kg = gr.Number(label="Weight (kg)")
                    with gr.Row():
                        age = gr.Number(label="Age")
                        gender = gr.Radio(
                            choices=["Male", "Female", "Other"],
                            label="Gender"
                        )

                # Button group
                with gr.Row():
                    clear_btn = gr.Button("Clear", elem_classes="clear-btn")
                    submit_btn = gr.Button("Get Recipes ✨", elem_classes="submit-btn")

        # Right: Result output
        with gr.Column(scale=1):
            with gr.Column(variant="panel", elem_classes="custom-card"):
                gr.Markdown("### 🍽️ Suggested Recipes")
                output = gr.Textbox(
                    label=None, 
                    show_label=False,
                    lines=25, # Increase height to fit full screen
                    elem_id="output-card",
                    interactive=False
                )

    # 3. Logic binding (strictly follow the order you provided)
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

    # Clear logic
    clear_btn.click(
        fn=lambda: (None, None, None, None, None, None, None, None, ""),
        inputs=[],
        outputs=[
            food_image,
            meal_type,
            dietary_restrictions,
            meal_preferences,
            height_cm,
            weight_kg,
            age,
            gender,
            output
        ]
    )

# 4. Launch preview
if __name__ == "__main__":
    demo.launch(theme=theme, css=css)