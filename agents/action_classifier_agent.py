from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def action_classifier_agent(task_desc):
    prompt = f"""
    You are an AI assistant classifying software development requests.

    Task description: "{task_desc}"

    Possible categories:
    1. "ui_change" → Changes to existing UI or screen.
    2. "bug_fix" → Fixing errors, broken features, or incorrect logic.
    3. "new_feature" → Adding completely new features or screens.

    Respond with only one category string.
    """
    return llm.invoke(prompt).strip().lower()
