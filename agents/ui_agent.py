from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5-coder")

def ui_agent(screen):
    prompt = f"""
    You are a **senior frontend engineer** building production-ready React.js applications.

    Below is the JSON describing a single UI screen for the app:
    {screen}

    ---
    ### Task:
    - Generate a **React.js functional component** for this screen using **Tailwind CSS** for styling.
    - Follow the given description, elements, design details, and interactions exactly.
    - Ensure **responsive design** for desktop and mobile.
    - Implement form validation where applicable.
    - Add accessibility features (aria-labels, semantic HTML).
    - Keep code **clean, modular, and well-documented**.
    - Should not use other packages for Tailwindcss. Only use Tailwind CSS classes.
    - Use only fontawesome icons in the screens
       Example: import {{ FontAwesomeIcon }} from '@fortawesome/react-fontawesome';
                import {{ faUser, faLock }} from '@fortawesome/free-solid-svg-icons';
                <FontAwesomeIcon icon={{faUser}} />
                <FontAwesomeIcon icon={{faLock}} />

    ---
    ### Output:
    - Return only the **full React component code** for this screen.
    - Important: Do not include explanations or markdown formatting.
    - Component should be **ready to paste into a React project** and work with the shared design system.
    """
    return llm.invoke(prompt).strip()