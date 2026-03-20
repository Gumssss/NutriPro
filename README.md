# JOE - AI Recipe Creator

## Overview
JOE is an AI recipe creator. Upload a photo of the ingredients you have available and any requirements you have, and JOE will give you three delicious recipes you could make.

## How to run
1. Ensure all requirements are installed on your device. A `requirements.txt` exists in this repository; run `pip install -r requirements.txt`.
2. The demo version runs using Gradio. Launch the GUI with:
   ```bash
   python gradioInterface2.0.py
   ```
3. After a short wait, the script will print a local URL (usually `http://127.0.0.1:7860`). Open it in a browser and JOE will appear.
4. Upload an ingredient photo (upload/copy-paste/camera), provide optional notes or restrictions, and click `Generate Recipes`.
5. Wait ~20-30 seconds for AI to process and return 3 recipes.
6. To stop hosting, press `Ctrl+C` in the terminal and wait for shutdown.

### AWS credentials
- JOE requires AWS Bedrock access to run the AI pipeline.
- Ensure your AWS credentials are set in the environment (e.g., `~/.aws/credentials`) or create a `.env` file in the project root with keys like:
  ```text
  OPENAI_API_KEY=your_api_key_here
  ```
- Keep credentials valid during use.

## Hosting publicly
To access JOE from another device (phone/tablet):
1. In `gradioInterface2.0.py`, change the final launch line from:
   ```python
demo.launch(theme=theme, css=css)
   ```
   to:
   ```python
demo.launch(theme=theme, css=css, share=True)
   ```
2. This returns a temporary public URL for external access.
3. Note: public access may be blocked by firewalls or corporate networks. Home networks generally work best.

Alternative: upload your phone photo to the computer and use the app locally.

## Common problems
- Each agent logs intermediate results in the terminal. Check those outputs for debugging.
- URL links returned by Gradio are valid only while the app is running and may change each run.
- Immediate recipe generation errors often indicate invalid or expired credentials. Refresh credentials and try again.
- Phone camera access may fail for some OS/browser combos; use file upload instead.
- If no ingredients are detected, the AI may produce irrelevant recipes. If no recipes appear, the model sometimes fails on contrived edge inputs.
- Old versions had calorie search errors due web scraping restrictions. This is now fixed by domain whitelisting (`calories.info`, `webmd.com`, `myfitnesspal.com`). If you see calorie search errors, upgrade to the latest version.

## Architecture Overview
The project is built as a modular agent pipeline using LangChain and LangGraph.

### Agent chain
- `agents_chain/` contains:
  - `food_image_converter.py`: image-to-ingredient conversion (vision_node)
  - `calorie_agent.py`: calories and nutrient extraction (calories_node)
  - `recipe_agent.py`: recipe generation (recipes_node)
  - `main_langchain.py`: pipeline builder using LangGraph
  - `utils.py`: common helper data structures and parsing utilities

- `botInterface.py` builds a middle-layer API and formats output for display.
- `gradioInterface2.0.py` is the main front-end launch point.

### Flow
1. User input via Gradio (image + preferences)
2. `botInterface.suggest_recipes` assembles input and state
3. `main_langchain.build_master_graph` composes agent graph:
   - `vision` -> `calories` -> `recipes`
4. Graph invokes sequential agents
5. Result JSON is returned and formatted for UI

## Appendix 1 - test images
Use these ideas as test inputs:
- vegetable mix (tomato, cucumber, bell pepper)
- poultry + rice + carrots
- tofu + spinach + mushrooms
- leftover pasta + cheese + broccoli

(If you have local sample images, place them in the project folder and provide the path in the UI.)

## Appendix 2 - example output
```
Based on your ingredients and preferences here are your recommended recipes: Grilled Vegetable Salad | Veggie Stir Fry

------------------------------------------------------------
**Grilled Vegetable Salad** (Calories: 250)
----------------------------------------------
**Ingredients:**
- Tomato: 2 medium
- Cucumber: 1 whole
- Bell Pepper: 1 whole
----------------------------------------------
**Recipe:**
- Wash all vegetables thoroughly
- Cut into bite-sized pieces
- Arrange on a plate
- Drizzle with olive oil and lemon juice
- Serve immediately

------------------------------------------------------------
**Veggie Stir Fry** (Calories: 320)
----------------------------------------------
**Ingredients:**
- Broccoli: 200g
- Carrots: 1 medium
- Onion: 1 small
----------------------------------------------
**Recipe:**
- Heat oil in a wok
- Add onions and cook until translucent
- Add vegetables and stir fry until tender
- Add sauce and serve with rice
```
