from langchain_ollama import OllamaLLM
import os
from utils.clean_code_blocks import clean_code_blocks
llm = OllamaLLM(model="qwen2.5-coder")
import json

def ui_change_agent(change_desc, react_app_path):
    """AI agent that updates UI components automatically based on a description."""

    # Step 1: Collect all React source files
    project_files = []
    for root, _, files in os.walk(os.path.join(react_app_path, "src")):
        for file in files:
            if file.endswith((".jsx", ".js", ".tsx", ".ts")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    project_files.append({
                        "path": file_path,
                        "content": f.read()
                    })

    # Step 2: Create project summary for LLM
    project_summary = "\n\n".join([
        f"--- FILE: {os.path.relpath(f['path'], react_app_path)}\n{f['content']}"
        for f in project_files
    ])

    # Step 3: Prompt to LLM
    prompt = f"""
    You are a **senior React.js developer**.
    
    The project codebase is below:
    {project_summary}

    The requested UI change is:
    "{change_desc}"

    ---
    ### Instructions:
    1. Identify the file(s) that need to be updated for this change.
    2. Apply the change directly to the existing code.
    3. Return ONLY a JSON array of updated files, like this:
       [
         {{
           "file": "relative/path/to/file",
           "updated_code": "FULL updated code for that file"
         }}
       ]

    ---
    ### Output:
    - Return only the **full React component code** for this screen.
    - Important: Do not include explanations or markdown formatting.
    - Component should be **ready to paste into a React project** and work with the shared design system.
    """

    raw_output = clean_code_blocks(llm.invoke(prompt).strip())

    # Step 4: Parse LLM output
    try:
        updates = json.loads(raw_output)
    except json.JSONDecodeError:
        return f"❌ Could not parse AI output as JSON:\n{raw_output}"

    # Step 5: Apply updates
    for update in updates:
        file_path = os.path.join(react_app_path, update["file"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(update["updated_code"])
        print(f"✅ Updated: {update['file']}")

    return "🎨 UI changes applied successfully!"
