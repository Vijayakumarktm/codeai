from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def ui_ux_designer_agent(features_json):
    prompt = f"""
    You are a **Senior UI/UX Designer**.

    Below is the list of features for an MVP React.js web application:
    {features_json}

    ---
    ### Responsibilities:
    1. For each feature, design the **full set of UI screens/components** needed.
    2. For each screen:
       - Name it (Title Case, short).
       - Provide a short description of its purpose.
       - List the main UI elements/components.
       - Suggest important design details (color theme, layout style, etc.).
       - Mention any important interaction patterns (buttons, modals, drag-and-drop, etc.).
    3. Ensure the full set of screens covers the **entire user journey** from first use to feature completion.
    4. Make sure all screens are consistent with a **modern, responsive, accessible design**.

    ---
    ### Output JSON format:
    {{
        "screens": [
            {{
                "name": "Screen Name",
                "file_name": "screen_name.jsx",
                "description": "Short description of what this screen is for.",
                "elements": ["UI Element 1", "UI Element 2", "UI Element 3"],
                "design_details": "Color scheme, layout style, etc.",
                "interactions": ["Interaction Pattern 1", "Interaction Pattern 2"]
            }}
        ]
    }}
    ---
    Respond only in JSON. Do not include markdown or explanations.
    """
    return llm.invoke(prompt).strip()
