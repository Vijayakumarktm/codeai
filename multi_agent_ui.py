from fileinput import filename
import os
import json
from langchain_ollama import OllamaLLM
from setup_react_app import setup_react_app

# ====== Setup ======
llm = OllamaLLM(model="llama3.1")

# ====== Folder Setup ======
react_app_path = os.path.join(os.getcwd(), "react-ai-app")
setup_react_app()

# ====== Agent Definitions ======
def project_manager_agent(idea):
    prompt = f"""
        You are an expert **Product Manager and Technical Architect**.

        Your task is to analyze the following project idea and break it down into **well-structured screens** needed for implementation in a React.js web app.

        ---

        ### 🎯 Project Idea:
        "{idea.strip()}"

        ---

        ### 🧠 Your Responsibilities:
        1. Understand the user's idea and its end goal.
        2. Identify the **core features** required.
        3. For each feature, define the **UI screens** needed.
        4. Provide a clean list of **screen/component names** (use short, readable names like `Login`, `Dashboard`, `Profile`).
        5. Output in structured JSON format as shown below.

        ---

        ### 📦 Output Format (JSON Only):

        ```json
        {{
        "features": ["Feature 1", "Feature 2", "..."],
        "screens": ["Screen1", "Screen2", "..."]
        }}

        ✅ Do not include explanations, markdown, or formatting — only return the JSON.

        Respond like a real PM designing the app before handing off to developers.
        """
    return llm.invoke(prompt).strip()

def clean_code_blocks(text):
    """
    Safely remove triple backtick code fences from LLM output.
    Handles ```js, ```jsx, or ``` alone at the start.
    """
    lines = text.strip().splitlines()

    # Remove the first line if it's a code fence
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]

    # Remove the last line if it's a closing fence
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()

def ui_agent(screen_name):
    prompt = f"""
        You are a senior frontend engineer building production-ready React.js applications.

        Your task is to write a clean, modular, and well-documented **React functional component** for the screen: **"{screen_name}"**.

        ### Requirements:
        - Use **Tailwind CSS** for styling.
        - Ensure the UI is **visually appealing, responsive**, and follows **modern design principles**.
        - Include **form elements** (if applicable, e.g., Login or Signup) with proper **validation and error handling**.
        - Implement a **submit handler** with appropriate placeholder logic (e.g., console log or API call).
        - Follow **production-level best practices**, including:
        - Clear separation of concerns
        - Descriptive naming
        - Accessibility (labels, aria-* if needed)
        - Minimal and meaningful comments

        ### Output:
        - Only return the full code for the React component.
        - Do **not** include explanations or markdown formatting.
        - Component should be **ready to use in a modern React app**.

        Ensure code quality, reusability, and visual polish as if shipping to production.
        """

    return llm.invoke(prompt).strip()

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


# ====== Main Execution ======

if __name__ == "__main__":
    

    project_idea = input("💡 Enter your project idea (e.g., CRM for freelancers): ").strip()

    if not project_idea:
        print("⚠️ Project idea is required. Exiting.")
        exit(1)

    # Step 1: Project Manager Agent
    print("\n🧑‍💼 Project Manager analyzing the idea...\n")
    raw_response = clean_code_blocks(project_manager_agent(project_idea))
    print("📝 Project Manager output:", raw_response)

    # Step 2: Parse JSON safely
    try:
        features_and_screens = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON. Output from agent:")
        print(raw_response)
        raise e

    if not features_and_screens.get("screens"):
        print("⚠️ No screens extracted from project manager agent.")
        exit(1)

    screens = features_and_screens["screens"]
    print("📝 Screens identified by Project Manager:", ", ".join(screens))
        
    results = {}

    for screen in screens:
        print(f"\n🚀 Generating for: {screen} Screen")
        

        # Step 1: UI Agent
        component = clean_code_blocks(ui_agent(screen))
        component_path = os.path.join(react_app_path, "src/components", f"{screen}.jsx")
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, "w") as f:
            f.write(component)
        print(f"✅ UI Component saved: {component_path}")
        print("✅ UI Component done.")

        # Step 2: Review Agent
        review = review_agent(component)
        print("🔍 Code reviewed.")

        # Step 3: Test Agent
        tests = clean_code_blocks(test_case_agent(screen, component))
        test_path = os.path.join("src/tests", f"{screen}.test.js")
        os.makedirs(os.path.dirname(test_path), exist_ok=True)
        with open(test_path, "w") as f:
            f.write(tests)
        print(f"🧪 Test cases saved: {test_path}")
        print("🧪 Test cases written.")

        # Step 4: QA Agent
        qa_feedback = qa_agent(tests, component)
        qa_path = os.path.join("qa", f"{screen}_qa_review.txt")
        os.makedirs(os.path.dirname(qa_path), exist_ok=True)
        with open(qa_path, "w") as f:
            f.write(qa_feedback)
        print(f"🔬 QA feedback saved: {qa_path}")
        print("🔬 QA validation done.")


    print("\n📁 All done! Check 'multi_agent_ui_output.txt' for full results.")
