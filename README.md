# 🍽️ NutriPro

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

**AI-powered recipe generator that transforms your ingredients into personalized dishes**

[Quickstart](#-quick-start) • [Features](#-core-features) • [Installation](#-installation-guide) • [Usage](#-usage-guide) • [Contributing](#-contributing-guide)

</div>

---

## 📖 Introduction

**NutriPro** is an intelligent nutrition recipe system that uses advanced computer vision and AI technology to help users create personalized recipes based on available ingredients. Simply snap a photo of your ingredients, and NutriPro can:

- 🔍 **Smart Recognition** of all your ingredients
- 📊 **Precise Calculation** of nutrition and calorie information
- 👨‍🍳 **Personalized Recommendations** of recipes suited for you

Whether you're a fitness enthusiast, a dieter, or a food adventurer, NutriPro helps you make smarter dietary choices!

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Recognition** | Advanced vision AI to identify ingredients |
| 🧮 **Nutrition Analysis** | Automatic calorie and nutrient calculation |
| 👨‍🍳 **Recipe Generation** | Personalized recipes based on preferences and goals |
| 🎯 **Fitness Tracking** | Integrated fitness goal support |
| 🚫 **Dietary Restrictions** | Respects allergies and vegetarian preferences |
| 👤 **User Profiles** | Customized recommendations based on height, weight, and age |
| 💻 **Modern UI** | Beautiful Gradio Web interface |
| 🔗 **API Interface** | Complete backend API support |

---

## 📋 Prerequisites

Before getting started, ensure you have installed:

- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository

<details>
<summary><b>View System Check Commands</b></summary>

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check Git version
git --version
```

</details>

---

## 🚀 Installation Guide

### Step 1️⃣: Clone the Repository

```bash
git clone https://github.com/yourusername/NutriPro.git
cd NutriPro
```

### Step 2️⃣: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies to install include:
- `gradio` - Web interface framework
- `langchain` - AI agent framework
- `langgraph` - Workflow orchestration
- `pillow` - Image processing
- `python-dotenv` - Environment variable management

### Step 4️⃣: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys (e.g., OpenAI API Key):

```env
OPENAI_API_KEY=your_api_key_here
# Other configurations...
```

### Step 5️⃣: Verify Installation

```bash
python -c "import gradio; import langchain; print('✅ All dependencies installed successfully!')"
```

---

## 💡 Usage Guide

### Method 1: Web User Interface (Recommended)

```bash
# Start the Gradio Web interface
python gradioInterface2.0.py
```

Then open in your browser: `http://localhost:7860`

**Usage Steps:**

1. 📸 **Upload Ingredient Photo** - Click upload button or drag and drop
2. 🎯 **Select Preferences** - Choose meal type, dietary restrictions, fitness goals, etc.
3. 👤 **Input Personal Information** (Optional) - Height, weight, age, gender
4. ✅ **Click Submit** - Get personalized recipe recommendations

<details>
<summary><b>Interface Parameters Details</b></summary>

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Meal Type** | Breakfast/Lunch/Dinner/Snack | Lunch |
| **Dietary Restrictions** | Vegetarian/Gluten-free/Dairy-free, etc. | Vegetarian |
| **Meal Preference** | Grilled/Soup/Salad, etc. | Grilled |
| **Fitness Goal** | Muscle gain/Fat loss/Maintenance | Fat loss |
| **Personal Info** | Height/Weight/Age/Gender | 170cm/70kg/25/M |

</details>

### Method 2: Python API

```python
from botInterface import suggest_recipes
from PIL import Image

# Load ingredient image
food_image = Image.open("your_ingredients.jpg")

# Get recipe suggestions
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

### Method 3: Command Line Interface

```bash
python botInterface.py
# Follow prompts to input parameters and image path
```

---

## 📊 Output Example

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

## 🏗️ Project Architecture

```
NutriPro/
├── agents_chain/           # AI agent chain core
│   ├── food_image_converter.py  # Food image recognition (vision_node)
│   ├── calorie_agent.py         # Nutrition calculation agent (calories_node)
│   ├── recipe_agent.py          # Recipe generation agent (recipes_node)
│   ├── main_langchain.py        # Main workflow orchestration
│   └── utils.py                 # Utility functions and data classes
├── botInterface.py         # Backend API interface
├── gradioInterface2.0.py   # Web UI (Recommended)
├── gradioInterface.py      # Web UI (Alternative)
├── LICENSE                 # MIT License
└── README.md              # Project documentation
```

### Processing Pipeline

```
User Input → Food Recognition → Nutrition Calculation → Recipe Generation → Formatted Output
    ↓            ↓                    ↓                      ↓
  [Image]    [Ingredients]      [Calories]              [Recipes]
```

---

## 🔧 Advanced Configuration

### Customize AI Model

Edit `agents_chain/main_langchain.py` to change the model used:

```python
# Switch to other LLM models
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
```

### Adjust Vision Recognition Accuracy

In `agents_chain/food_image_converter.py`, adjust:

```python
# Modify recognition confidence threshold
CONFIDENCE_THRESHOLD = 0.75
```

---

## 🤝 Contributing Guide

We welcome contributions from the community! Whether it's bug fixes, new features, or documentation improvements.

### How to Contribute

#### 1. **Fork the Project**
   ```bash
   Click the "Fork" button on GitHub
   ```

#### 2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

#### 3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add some AmazingFeature"
   ```

#### 4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

#### 5. **Submit a Pull Request**
   - Open a PR on GitHub
   - Clearly describe your changes
   - Await review feedback

### Contribution Standards

- **Code Style**: Follow PEP 8
- **Commit Messages**: Write clear, meaningful commit messages
- **Documentation**: Update relevant documentation
- **Testing**: Ensure code works properly

### Code Support Areas

```
🔴 Priority (High)
├─ Improve ingredient recognition accuracy
├─ Add more recipe database
└─ Performance optimization

🟡 Priority (Medium)
├─ UI/UX improvements
├─ New dietary restriction support
└─ Multi-language support

🟢 Priority (Low)
├─ Documentation translation
└─ Unit test coverage
```

---

## 🐛 Report Bugs

Found an issue? Please:

1. Check the [Issues](https://github.com/yourusername/NutriPro/issues) page to see if it already exists
2. If not, create a new Issue and provide:
   - Detailed problem description
   - Steps to reproduce
   - System information (OS, Python version, etc.)
   - Error logs

---

## 📝 Frequently Asked Questions (FAQ)

<details>
<summary><b>Q: What image formats does NutriPro support?</b></summary>

A: Supports all common formats: JPG, PNG, GIF, WebP, etc. High-quality ingredient photos are recommended for best recognition results.

</details>

<details>
<summary><b>Q: Can it be used offline?</b></summary>

A: No. NutriPro requires an internet connection to call AI models (such as OpenAI API) for recognition and generation.

</details>

<details>
<summary><b>Q: How can I customize the recipe database?</b></summary>

A: Edit the `agents_chain/recipe_agent.py` file to modify or extend the recipe data source.

</details>

<details>
<summary><b>Q: How many dietary restrictions are supported?</b></summary>

A: Currently supports: vegetarian, gluten-free, dairy-free, nut-free, low-carb, etc. More can be added by modifying configuration files.

</details>

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2026 Johnny, Elliot and Oisin
```

---

## 👥 Acknowledgments

Thank you to all contributors and users for your support!

- 🙏 LangChain team for the excellent framework
- 🙏 Gradio team for the Web UI library
- 🙏 OpenAI for providing the Vision API

---

## 📞 Contact Us

Have questions or suggestions? Reach us through:

- 📧 Email: support@nutripro.example.com
- 🐦 Twitter: [@NutriProAI](https://twitter.com)
- 💬 Discord: [Join our community](https://discord.gg/)
- 🌐 Website: [nutripro.example.com](https://example.com)

---

<div align="center">

**⭐ If this project is helpful to you, please give us a Star!**

[Back to Top](#-nutripro)

</div>
