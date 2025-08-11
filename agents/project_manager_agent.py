from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def project_manager_agent(idea):
    prompt = f"""
    You are an expert **Product Manager**.

    Your task is to take the following project idea and turn it into a **complete MVP plan** for a React.js web application.

    ---
    ### Project Idea:
    "{idea.strip()}"
    ---

    ### Responsibilities:
    1. Understand the client’s goal from the idea.
    2. Define the **core features/modules** required for the MVP.
    3. For each feature, suggest a short description.
    4. Maintain priority order (most essential first).
    5. Keep feature names in Title Case.

    ---
    ### Output JSON format:
    {{
        "app_name": "<Short App Name>",
        "goal": "<One-line summary of the app’s purpose>",
        "features": [
            {{
                "feature_name": "Feature Name",
                "description": "Short explanation of the feature"
            }}
        ]
    }}
    ---
    Respond only in JSON. Do not include markdown, commentary, or extra text.
    """
    return llm.invoke(prompt).strip()