import os
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def bug_fix_agent(bug_desc, react_app_path):
    """Find and fix bugs in the React project based on a description."""
    
    # Step 1: Read all relevant project files
    project_files = []
    for root, _, files in os.walk(os.path.join(react_app_path, "src")):
        for file in files:
            if file.endswith((".jsx", ".js", ".ts", ".tsx")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    project_files.append({
                        "path": file_path,
                        "content": f.read()
                    })

    # Step 2: Build prompt for the LLM
    project_summary = "\n\n".join([f"--- FILE: {f['path']}\n{f['content']}" for f in project_files])

    prompt = f"""
    You are a **senior full-stack engineer** skilled in debugging and fixing React.js + TailwindCSS projects.

    The project files are:
    {project_summary}

    The reported bug is:
    "{bug_desc}"

    ---
    ### Task:
    1. Identify the root cause of the bug.
    2. Modify only the necessary file(s) to fix the bug.
    3. Keep all other functionality intact.
    4. Return a JSON array of objects:
       [
         {{
           "file": "relative/path/to/file",
           "updated_code": "FULL updated file code here"
         }}
       ]
    """

    fixes_json = llm.invoke(prompt).strip()

    # Step 3: Apply fixes
    import json
    try:
        fixes = json.loads(fixes_json)
    except json.JSONDecodeError:
        return f"❌ Could not parse AI output as JSON:\n{fixes_json}"

    for fix in fixes:
        file_path = os.path.join(react_app_path, fix["file"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fix["updated_code"])
        print(f"✅ Fixed: {fix['file']}")

    return "🐞 Bug fix applied successfully!"
