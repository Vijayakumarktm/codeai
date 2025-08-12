import os
import subprocess

def setup_react_app():
    """
    Bootstraps a Vite-based React app with Tailwind CSS and React Router.
    """
    if not os.path.exists("react-ai-app"):
        print("🛠️ Creating new React app with Vite...")
        subprocess.run([
            "npm", "create", "vite@latest", "react-ai-app", "--", "--template", "react"
        ], input=b"\n", check=True)

    os.chdir("react-ai-app")

    print("📦 Installing dependencies...")
    subprocess.run(["npm", "install"], check=True)

    print("🎨 Installing Tailwind CSS...")
    subprocess.run([ "npm", "install", "-D", "tailwindcss", "@tailwindcss/vite", "postcss", "autoprefixer"], check=True)

    print("🧭 Installing React Router DOM...")
    subprocess.run(["npm", "install", "react-router-dom"], check=True)

    print("🎨 Installing Font Awesome React packages...")
    subprocess.run([
        "npm", "install",
        "@fortawesome/react-fontawesome",
        "@fortawesome/free-solid-svg-icons",
        "@fortawesome/fontawesome-svg-core"
    ], check=True)

    with open("vite.config.js", "w") as f:
        f.write("""\
            import { defineConfig } from 'vite'
            import react from '@vitejs/plugin-react'
            import tailwindcss from '@tailwindcss/vite'

            export default defineConfig({
            plugins: [
                react(),
                tailwindcss(),
            ],
            })
            """
        )

    # Ensure components folder
    os.makedirs("src/components", exist_ok=True)

    # Setup Tailwind in index.css (via @import)
    with open("src/index.css", "w") as f:
        f.write("""\
        @import "tailwindcss";
        """
        )   
        
    # Create Home.jsx component
    with open("src/components/Home.jsx", "w") as f:
        f.write("""\
        import React from "react";

        function Home() {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-3xl font-bold text-blue-600">Welcome to the AI UI Builder App 🚀</h1>
            </div>
        );
        }

        export default Home;
        """)

    # Update App.jsx with Router setup and default "/" route
    with open("src/App.jsx", "w") as f:
        f.write("""\
            import React from "react";
            import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
            import Home from "./components/Home";

            function App() {
            return (
                <Router>
                <Routes>
                    <Route path="/" element={<Home />} />
                </Routes>
                </Router>
            );
            }

            export default App;
            """)

    print("✅ React app initialized with Tailwind and React Router.\n")

    print("🚀 Starting the development server...\n")
    subprocess.run(["osascript", "-e", 
        f'''
        tell application "Terminal"
            do script "cd '{os.getcwd()}' && npm run dev"
        end tell
        '''
    ])
