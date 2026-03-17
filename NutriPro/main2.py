import os
import json
import base64
from typing import List, TypedDict, Dict, Any
from dotenv import load_dotenv
from PIL import Image
import io

# 导入 LangChain 和 AWS 相关库
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# 1. 加载环境变量 (.env 文件)
load_dotenv()

# 2. 定义全局状态结构 (State)
class AgentState(TypedDict):
    image_base64: str           # 用户上传的图片 (Base64)
    user_profile: Dict[str, Any] # 用户生理数据和目标
    ingredients_data: Dict[str, Any] # Agent 1 的输出：食材 + 基础热量
    final_recipes: List[Dict[str, Any]] # Agent 2 的输出：食谱列表
    nutrition_report: str        # Agent 2 的输出：营养分析总结

# 3. 初始化 AWS Bedrock 模型
# 更新模型 ID 为最新的 v2 版本，避免 Legacy 限制错误
llm = ChatBedrockConverse(
    model="amazon.nova-pro-v1:0",
    region_name= "eu-west-2"
)

# --- 4. 节点函数定义 ---

def food_vision_agent(state: AgentState):
    """Agent 1: 视觉识别食材"""
    print("--- 执行节点: Agent 1 (视觉解析器) ---")
    
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
    """Agent 2: 膳食规划"""
    print("--- 执行节点: Agent 2 (膳食规划专家) ---")
    
    ingred_info = state["ingredients_data"]
    profile = state["user_profile"]
    
    prompt = f"""
    You are an Nutritionist & Professional Chef.
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

# --- 5. 构建立体工作流 (LangGraph) ---

workflow = StateGraph(AgentState)
workflow.add_node("vision_parser", food_vision_agent)
workflow.add_node("dietary_planner", nutrition_recipe_agent)
workflow.set_entry_point("vision_parser")
workflow.add_edge("vision_parser", "dietary_planner")
workflow.add_edge("dietary_planner", END)

app = workflow.compile()

# --- 6. 工具函数：图片转 Base64 ---
def encode_image(image_path: str) -> str:
    """读取本地图片文件并转换为 JPEG 格式的 Base64 字符串"""
    with Image.open(image_path) as img:
        # 转换为 RGB 模式（如果不是的话）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # 保存为 JPEG 格式的字节流
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

# --- 7. 运行演示 (测试代码) ---
if __name__ == "__main__":
    # --- 重要：请确保你的目录下确实有这张图片，或者修改这个名字 ---
    TEST_IMAGE = "test_food.jpg" 
    
    if os.path.exists(TEST_IMAGE):
        print(f"✅ 找到测试图片: {TEST_IMAGE}")
        img_b64 = encode_image(TEST_IMAGE)
    else:
        print(f"❌ 错误: 未能在目录下找到 {TEST_IMAGE}。请放置一张食材照片并命名为 {TEST_IMAGE}")
        # 退出程序或使用默认模拟数据
        img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

    test_input = {
        "image_base64": img_b64,
        "user_profile": {
            "age": 28,
            "weight": 70,
            "gender": "male",
            "goal": "cutting",
            "allergies": ["peanuts"],
            "meal_type" : "Dinner"
        }
    }
    
    print("启动 AI Food Agent Pipeline...")
    try:
        final_state = app.invoke(test_input)
        print("\n" + "="*50)
        print("【Agent 1 识别出的食材】:", final_state['ingredients_data']['ingredients'])
        print("【Agent 2 建议的食谱】:")
        for r in final_state['final_recipes']:
            print(f"- {r.get('name')} (热量: {r.get('calories')} kcal)")
        print("【营养专家寄语】:", final_state['nutrition_report'])
        print("="*50)
    except Exception as e:
        print(f"运行出错: {e}")