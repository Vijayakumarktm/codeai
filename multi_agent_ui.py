from fileinput import filename
import os
import json
from setup_react_app import setup_react_app
from utils.clean_code_blocks import clean_code_blocks
from agents.project_manager_agent import project_manager_agent
from agents.ui_ux_designer_agent import ui_ux_designer_agent
from agents.ui_agent import ui_agent

# ====== Folder Setup ======
react_app_path = os.path.join(os.getcwd(), "react-ai-app")
setup_react_app()

# ====== Main Execution ======

if __name__ == "__main__":

    project_idea = input("💡 Enter your project idea (e.g., CRM for freelancers): ").strip()

    if not project_idea:
        print("⚠️ Project idea is required. Exiting.")
        exit(1)

    # Step 1: Project Manager Agent
    print("\n🧑‍💼 Project Manager analyzing the idea...\n")
    raw_features = clean_code_blocks(project_manager_agent(project_idea))
    print("📝 Project Manager output:", raw_features)

    # Step 2: Parse JSON safely
    try:
        features_data = json.loads(raw_features)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON. Output from agent:")
        print(raw_features)
        raise e

    print(f"\n🎨 UI/UX Designer working on: {features_data}")
    raw_screens = clean_code_blocks(ui_ux_designer_agent(features_data))
    print("📝 UI/UX Designer output:", raw_screens)

    try:
        screens_data = json.loads(raw_screens)
        print("\n📝 Screens Data:", json.dumps(screens_data, indent=2))
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON for feature: {features_data}")
        raise e

    for screen in screens_data["screens"]:
        print(f"\n🚀 Generating for: {screen['name']} Screen")

        # Step 1: UI Agent
        component = clean_code_blocks(ui_agent(screen))
        component_path = os.path.join(react_app_path, "src/components", f"{screen['name']}.jsx")
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, "w") as f:
            f.write(component)
        print(f"✅ UI Component saved: {component_path}")
        print("✅ UI Component done.")

        # # Step 2: Review Agent
        # review = review_agent(component)
        # print("🔍 Code reviewed.", review)

        # Step 3: Test Agent
        # tests = clean_code_blocks(test_case_agent(screen, component))
        # test_path = os.path.join("src/tests", f"{screen}.test.js")
        # os.makedirs(os.path.dirname(test_path), exist_ok=True)
        # with open(test_path, "w") as f:
        #     f.write(tests)
        # print(f"🧪 Test cases saved: {test_path}")
        # print("🧪 Test cases written.")

        # Step 4: QA Agent
        # qa_feedback = qa_agent(tests, component)
        # qa_path = os.path.join("qa", f"{screen}_qa_review.txt")
        # os.makedirs(os.path.dirname(qa_path), exist_ok=True)
        # with open(qa_path, "w") as f:
        #     f.write(qa_feedback)
        # print(f"🔬 QA feedback saved: {qa_path}")
        # print("🔬 QA validation done.")


    print("\n📁 All done!")
