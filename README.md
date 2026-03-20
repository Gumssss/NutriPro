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
Here are some pre-selected images that you can copy and paste into JOE for testing and demonstrations:
![35eed88aed9cc19e7a840a2cd9ba9d4c](https://github.com/user-attachments/assets/25893e7c-c093-4465-aca8-c7a0c11fcbff)
![a56a826b6e9f867805b5e83f5963518b](https://github.com/user-attachments/assets/d4229a35-a9b8-4f05-9f56-7581c709174c)
![206b2dd17d92378e16055b6c347ecd1d](https://github.com/user-attachments/assets/64060fef-0bfd-4ad7-b1fd-eaf753fcf5e2)



## Appendix 2 - example output
<img width="1600" height="922" alt="67e6b7d5ee5fa2f9f4303a8e43a86fbc" src="https://github.com/user-attachments/assets/1fd8ea31-7e5f-45da-b15a-546f09cee789" />

<img width="1600" height="929" alt="c5462a5660ee4f9fa9ca3ad1c2765181" src="https://github.com/user-attachments/assets/01aa0c1c-76d6-4c8a-b833-4a28664f1e4a" />



