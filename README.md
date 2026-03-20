# 🍽️ NutriPro

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

**AI-powered recipe generator that transforms your ingredients into personalized dishes**

[Quickstart](#-快速开始) • [Features](#-核心特性) • [Installation](#-安装指南) • [Usage](#-使用指南) • [Contributing](#-贡献指南)

</div>

---

## 📖 简介

**NutriPro** 是一个智能营养配方系统，它使用先进的计算机视觉和AI技术来帮助用户根据现有食材创建个性化食谱。只需拍一张食材照片，NutriPro 就能：

- 🔍 **智能识别** 你所有的食材
- 📊 **精确计算** 营养和卡路里信息
- 👨‍🍳 **个性化推荐** 适合你的食谱建议

无论你是健身爱好者、节食者还是美食探险家，NutriPro 都能帮助你做出更智能的饮食选择！

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🖼️ **图像识别** | 使用先进的视觉AI识别食材 |
| 🧮 **营养分析** | 自动计算卡路里和营养成分 |
| 👨‍🍳 **食谱生成** | 基于喜好和目标的个性化食谱 |
| 🎯 **健身追踪** | 支持健身目标集成 |
| 🚫 **饮食限制** | 尊重过敏和素食等限制条件 |
| 👤 **个人档案** | 基于身高、体重、年龄的定制推荐 |
| 💻 **现代UI** | 精美的 Gradio Web 界面 |
| 🔗 **API接口** | 完整的后端 API 支持 |

---

## 📋 前置要求

在开始之前，请确保你的系统中已安装：

- **Python**: 3.8 或更高版本
- **pip**: Python 包管理器
- **Git**: 用于克隆代码库

<details>
<summary><b>查看系统检查命令</b></summary>

```bash
# 检查 Python 版本
python --version

# 检查 pip 版本
pip --version

# 检查 Git 版本
git --version
```

</details>

---

## 🚀 安装指南

### 步骤 1️⃣ : 克隆代码库

```bash
git clone https://github.com/yourusername/NutriPro.git
cd NutriPro
```

### 步骤 2️⃣ : 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 步骤 3️⃣ : 安装依赖

```bash
pip install -r requirements.txt
```

需要安装的主要依赖包括：
- `gradio` - Web 界面框架
- `langchain` - AI 代理框架
- `langgraph` - 工作流编排
- `pillow` - 图像处理
- `python-dotenv` - 环境变量管理

### 步骤 4️⃣ : 配置环境变量

创建 `.env` 文件在项目根目录：

```bash
cp .env.example .env
```

编辑 `.env` 文件并添加你的 API 密钥（如 OpenAI API Key）：

```env
OPENAI_API_KEY=your_api_key_here
# 其他配置...
```

### 步骤 5️⃣ : 验证安装

```bash
python -c "import gradio; import langchain; print('✅ 所有依赖已成功安装！')"
```

---

## 💡 使用指南

### 方式 1: Web 用户界面（推荐）

```bash
# 启动 Gradio Web 界面
python gradioInterface2.0.py
```

然后在浏览器中打开：`http://localhost:7860`

**使用步骤：**

1. 📸 **上传食材图片** - 点击上传按钮或拖拽图片
2. 🎯 **选择偏好** - 选择膳食类型、饮食限制、健身目标等
3. 👤 **输入个人信息**（可选）- 身高、体重、年龄、性别
4. ✅ **点击提交** - 获取个性化食谱推荐

<details>
<summary><b>界面参数详解</b></summary>

| 参数 | 描述 | 示例 |
|------|------|------|
| **膳食类型** | 早餐/午餐/晚餐/点心 | 午餐 |
| **饮食限制** | 素食/无麸质/无乳制品等 | 素食 |
| **餐食偏好** | 烤制/煮汤/沙拉等 | 烤制 |
| **健身目标** | 增肌/减脂/维持 | 减脂 |
| **个人信息** | 身高/体重/年龄/性别 | 170cm/70kg/25/M |

</details>

### 方式 2: Python API

```python
from botInterface import suggest_recipes
from PIL import Image

# 加载食材图片
food_image = Image.open("your_ingredients.jpg")

# 获取食谱建议
result = suggest_recipes(
    food_image=food_image,
    meal_type="lunch",
    dietary_restrictions="vegetarian",
    meal_preferences="grilled",
    fitness_goals="weight_loss",
    height_cm=170,
    weight_kg=70,
    age=25,
    gender="M"
)

print(result)
```

### 方式 3: 命令行界面

```bash
python botInterface.py
# 按照提示输入参数和图片路径
```

---

## 📊 输出示例

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
...
```

---

## 🏗️ 项目架构

```
NutriPro/
├── agents_chain/           # AI 代理链核心
│   ├── food_image_converter.py  # 食物图像识别 (vision_node)
│   ├── calorie_agent.py         # 营养计算代理 (calories_node)
│   ├── recipe_agent.py          # 食谱生成代理 (recipes_node)
│   ├── main_langchain.py        # 主工作流编排
│   └── utils.py                 # 工具函数和数据类
├── botInterface.py         # 后端 API 接口
├── gradioInterface2.0.py   # Web UI（推荐）
├── gradioInterface.py      # Web UI（备选）
├── LICENSE                 # MIT 许可证
└── README.md              # 项目文档
```

### 处理流程

```
用户输入 → 食物识别 → 营养计算 → 食谱生成 → 格式化输出
  ↓          ↓         ↓        ↓
[图片]    [成分]   [卡路里]   [食谱]
```

---

## 🔧 高级配置

### 自定义 AI 模型

编辑 `agents_chain/main_langchain.py` 修改所使用的模型：

```python
# 更改为其他 LLM 模型
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
```

### 调整视觉识别精度

在 `agents_chain/food_image_converter.py` 中调整：

```python
# 修改识别置信度阈值
CONFIDENCE_THRESHOLD = 0.75
```

---

## 🤝 贡献指南

我们欢迎来自社区的贡献！无论是 Bug 修复、新功能还是文档改进。

### 如何贡献

#### 1. **Fork 项目**
   ```bash
   点击 GitHub 上的 "Fork" 按钮
   ```

#### 2. **创建特性分支**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

#### 3. **提交你的更改**
   ```bash
   git add .
   git commit -m "Add some AmazingFeature"
   ```

#### 4. **推送到分支**
   ```bash
   git push origin feature/AmazingFeature
   ```

#### 5. **提交 Pull Request**
   - 在 GitHub 上打开一个 PR
   - 清晰描述你的更改内容
   - 等待审核反馈

### 贡献规范

- **代码风格**: 遵循 PEP 8
- **提交信息**: 写清晰、有意义的提交信息
- **文档**: 更新相关文档
- **测试**: 确保代码正常工作

### 代码支持区域

```
🔴 优先级 (高)
├─ 改进食材识别精度
├─ 添加更多食谱库
└─ 性能优化

🟡 优先级 (中)
├─ UI/UX 改进
├─ 新的饮食限制支持
└─ 多语言支持

🟢 优先级 (低)
├─ 文档翻译
└─ 单元测试覆盖
```

---

## 🐛 报告 Bug

遇到问题？请：

1. 在 [Issues](https://github.com/yourusername/NutriPro/issues) 页面检查是否已有相同问题
2. 如果没有，创建新 Issue 并提供：
   - 详细的问题描述
   - 复现步骤
   - 系统信息（OS、Python 版本等）
   - 错误日志

---

## 📝 常见问题 (FAQ)

<details>
<summary><b>Q: NutriPro 支持哪些格式的图片？</b></summary>

A: 支持所有常见格式：JPG、PNG、GIF、WebP 等。建议使用高质量的食材照片以获得最佳识别效果。

</details>

<details>
<summary><b>Q: 是否可以离线使用？</b></summary>

A: 不可以。NutriPro 需要互联网连接以调用 AI 模型（如 OpenAI API）进行识别和生成。

</details>

<details>
<summary><b>Q: 如何自定义食谱数据库？</b></summary>

A: 编辑 `agents_chain/recipe_agent.py` 文件，修改或扩展食谱数据源。

</details>

<details>
<summary><b>Q: 支持多少种饮食限制？</b></summary>

A: 目前支持：素食、无麸质、无乳制品、无坚果、低碳等。可通过修改配置文件添加更多。

</details>

---

## 📜 许可证

本项目采用 **MIT License** 进行许可。详见 [LICENSE](LICENSE) 文件。

```
Copyright (c) 2026 Johnny, Elliot and Oisin
```

---

## 👥 致谢

感谢所有贡献者和使用者的支持！

- 🙏 LangChain 团队提供的优秀框架
- 🙏 Gradio 团队的 Web UI 库
- 🙏 OpenAI 提供的 Vision API

---

## 📞 联系我们

有问题或建议？请通过以下方式联系：

- 📧 Email: support@nutripro.example.com


---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star 支持我们！**

[Back to Top](#-nutripro)

</div>
