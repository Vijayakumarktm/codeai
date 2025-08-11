from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def qa_agent(test_cases, component_code):
    prompt = f"""
        You are a senior QA reviewer responsible for validating the quality and completeness of test coverage for production-level React components.

        Review the following:

        ### 🧩 Component:
        {component_code}

        ### 🧪 Test Cases:
        {test_cases}

        ### Your Responsibilities:
        - Evaluate whether the provided test cases **fully cover** the component’s logic and functionality.
        - Check if the tests validate:
        - Rendering of all elements and UI states
        - Input field changes and interactions
        - All validation rules (e.g., required, email format, etc.)
        - Submit logic and handling
        - Any **edge cases** or unusual flows
        - Accessibility aspects (e.g., labels, ARIA roles)

        ### Output Guidelines:
        - ❗ List any **missing test scenarios** or **logic not covered**.
        - 🛠 Point out any **incorrect or ineffective tests**.
        - ✅ If coverage is good, confirm it and suggest any minor improvements.
        - Use **bullet points** for clarity.
        - Do **not rewrite code** — only review and give feedback.
        - Be precise and focus on **production-quality test reliability**.

        Assume this code is part of a real-world, user-facing application used by thousands of people.
        """

    return llm.invoke(prompt).strip()
