from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def test_case_agent(screen_name, component_code):
    prompt = f"""
        You are a professional QA engineer writing **production-level automated tests** for a React.js application.

        Your task is to write **unit and integration test cases** using **Jest** and **React Testing Library** for the following screen component: **"{screen_name}"**.

        ---
        {component_code}
        ---

        ### Test Coverage Requirements:
        - ✅ Initial rendering of the component
        - ✅ Form input interactions (e.g., typing into fields)
        - ✅ Validation errors (e.g., required fields, invalid inputs)
        - ✅ Form submission behavior (e.g., successful submit, validation blocks submit)
        - ✅ Edge cases (if any)
        - ✅ Accessibility checks (if applicable — labels, roles, etc.)

        ### Guidelines:
        - Use **`describe` / `it`** or **`test`** blocks clearly.
        - Use **semantic queries** from React Testing Library (e.g., `getByLabelText`, `getByRole`, not `getByTestId` unless necessary).
        - Mock external dependencies or handlers if required.
        - Keep tests **readable, maintainable**, and follow **AAA (Arrange-Act-Assert)** pattern.

        ### Output Instructions:
        - Return only the **test code** — no explanations, markdown, or extra text.
        - Code should be **ready to paste** into a `.test.js` file in a real project.

        Write the tests as if this code is about to be shipped in a **production app used by thousands of users**.
        """

    return llm.invoke(prompt).strip()