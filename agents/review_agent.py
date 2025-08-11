from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def review_agent(component_code):
    prompt = f"""
        You are a senior frontend code reviewer at a high-performing tech company.

        Your task is to perform a **focused, high-quality code review** of the following **React.js functional component**:

        ---
        {component_code}
        ---

        ### Review Guidelines:
        - Identify **areas of improvement only** — do **not** rewrite the full code.
        - Focus on:
        - **Code readability** (naming, structure, clarity)
        - **Best practices** (React patterns, hooks usage, logic separation)
        - **Tailwind CSS usage** (class clarity, responsiveness, consistency)
        - **Form validation and UX** (if applicable)
        - **Accessibility** and semantic HTML
        - **Performance optimization** (e.g., unnecessary re-renders, memoization)
        - Keep suggestions **clear, concise, and actionable**.
        - Use bullet points for multiple suggestions.

        ### Output Instructions:
        - Provide only the **review feedback**.
        - Do **not** include summaries, introductions, or rewrite the entire code.

        Review the component as if it is being prepared for a **production release** and will be used in a large-scale product.
        """
   
    return llm.invoke(prompt).strip()