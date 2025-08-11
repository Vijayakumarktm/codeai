import os
import json
from setup_react_app import setup_react_app
from utils.clean_code_blocks import clean_code_blocks
from agents.project_manager_agent import project_manager_agent
from agents.ui_ux_designer_agent import ui_ux_designer_agent
from agents.ui_agent import ui_agent
from agents.ui_change_agent import ui_change_agent
from agents.bug_fix_agent import bug_fix_agent
from agents.action_classifier_agent import action_classifier_agent

# ====== Folder Setup ======
react_app_path = os.path.join(os.getcwd(), "react-ai-app")
setup_react_app()

# ====== Functions ======

def build_project(project_idea):
    """Builds initial project from scratch."""
    # Step 1: Project Manager Agent
    print("\n🧑‍💼 Project Manager analyzing the idea...\n")
    raw_features = clean_code_blocks(project_manager_agent(project_idea))
    try:
        features_data = json.loads(raw_features)
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from Project Manager Agent.")
        return None

    # Step 2: UI/UX Designer Agent
    print(f"\n🎨 UI/UX Designer working on: {features_data}")
    raw_screens = clean_code_blocks(ui_ux_designer_agent(features_data))
    print("\n📋 Screens designed by UI/UX Designer Agent:\n", raw_screens)
    try:
        screens_data = json.loads(raw_screens)
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from UI/UX Designer Agent.")
        return None

    # Step 3: Generate UI components
    for screen in screens_data["screens"]:
        print(f"\n🚀 Generating for: {screen['name']} Screen")
        component = clean_code_blocks(ui_agent(screen))
        component_path = os.path.join(react_app_path, "src/components", f"{screen['file_name']}")
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, "w") as f:
            f.write(component)
        print(f"✅ UI Component saved: {component_path}")

    print("\n📁 Initial project build complete!")
    return screens_data


def update_screen_ui(screen_name, change_desc):
    """Update a specific screen's UI."""
    file_path = os.path.join(react_app_path, "src/components", f"{screen_name}.jsx")
    if not os.path.exists(file_path):
        print("❌ Screen not found.")
        return
    with open(file_path, "r") as f:
        current_code = f.read()

    updated_code = clean_code_blocks(ui_change_agent(current_code, change_desc))
    with open(file_path, "w") as f:
        f.write(updated_code)
    print(f"✅ Updated {screen_name} successfully.")


def fix_bug(bug_desc):
    """Scan project files and fix bugs."""
    found = False
    for root, _, files in os.walk(os.path.join(react_app_path, "src")):
        for file in files:
            if file.endswith(".jsx") or file.endswith(".js"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code = f.read()

                if bug_desc.lower() in code.lower():
                    found = True
                    print(f"🐞 Found possible issue in: {file}")
                    updated_code = clean_code_blocks(bug_fix_agent(code, bug_desc))
                    with open(file_path, "w") as f:
                        f.write(updated_code)
                    print(f"✅ Fixed issue in {file}")

    if not found:
        print("⚠️ No matching issue found in the codebase.")


def interactive_session():
    """Interactive CLI session for continuous project updates."""
    while True:
        choice = input("\n🔄 Continue working? (y/n): ").strip().lower()
        if choice == "n":
            print("👋 Exiting session.")
            break
        elif choice == "y":
            desc = input("\n📝 Describe what you want to do: ").strip()
            print(f"\n🔍 Classifying action for: {desc}")
            action_type = action_classifier_agent(desc)  # Decide action

            if action_type == "ui_change":
                print(ui_change_agent(desc, react_app_path))
            elif action_type == "new_feature":
                build_project(desc)
            elif action_type == "bug_fix":
                fix_bug(desc)
            else:
                print("⚠️ Could not classify action. Try rephrasing.")
        else:
            print("⚠️ Invalid input. Enter y or n.")


# ====== Main Execution ======
if __name__ == "__main__":
    # project_idea = input("💡 Enter your project idea (e.g., CRM for freelancers): ").strip()
    # if not project_idea:
    #     print("⚠️ Project idea is required. Exiting.")
    #     exit(1)

    # screens_data = build_project(project_idea)
    # if screens_data:
        interactive_session()
