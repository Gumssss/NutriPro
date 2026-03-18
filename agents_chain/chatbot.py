from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils import AgentState
from langgraph.graph import StateGraph, START, END

# Update any initial states previously set with a line
# for chat_history: Optional[List[BaseMessage]] before using with other files


chatbot = ChatBedrockConverse(
    model="qwen.qwen3-vl-235b-a22b",
    region_name="eu-west-2",
    temperature=0.0,
)

def chat_node(state):
    user_question = state["messages"][-1].content

    ingredients = state.get("ingredients", [])
    recipes = state.get("recipes", [])

    system_prompt = f"""
You are a helpful assistant answering questions about generated recipes the user has already seen.
Ingredients detected:
{ingredients}
Recipes generated:
{recipes}
Rules:
- Only use this information if necessary
- If unsure, say what's missing
- Be conversational
"""

    messages = [
        SystemMessage(content=system_prompt),
        *state.get("chat_history", []),
        HumanMessage(content=user_question)
    ]

    response = chatbot.invoke(messages)

    # update chat history
    chat_history = state.get("chat_history", [])
    chat_history += [
        HumanMessage(content=user_question),
        AIMessage(content=response.content)
    ]
    state["chat_history"] = chat_history
    return state

def build_chat_graph():
    graph = StateGraph(AgentState)

    graph.add_node("chat", chat_node)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)

    return graph.compile()

def main():
    # Build the compiled graph
    chat_graph = build_chat_graph()

    # When combined with the other agents, this will be the final state outputted by our main chain
    state = {
        "messages": [HumanMessage(content="Which recipe is highest in protein?")],
        "ingredients": [
            {"name": "chicken breast", "qty": "300g"},
            {"name": "spinach", "qty": "100g"},
        ],
        "recipes": [
            {"name": "Grilled Chicken Salad", "kcal": 550, "protein_g": 45, "instructions": "Grill the chicken..."},
            {"name": "Spinach Omelette", "kcal": 350, "protein_g": 20, "instructions": "Beat eggs..."}
        ],
        "chat_history": []  # optional
    }

    print("Starting chat (type 'exit' or 'quit' to stop)\n")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            # ignore blank lines
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

            # append user message to the state's messages list (the node reads last message)
        state.setdefault("messages", []).append(HumanMessage(content=user_input))

        state = chat_graph.invoke(state)

        chat_hist = state.get("chat_history", [])
        if chat_hist and isinstance(chat_hist[-1], AIMessage):
            print("\nAssistant:", chat_hist[-1].content)

if __name__ == "__main__":
    main()