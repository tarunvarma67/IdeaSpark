# IdeaSpark - Your Dynamic Brainstorming Partner

IdeaSpark is a Python Command Line Interface (CLI) tool that leverages Large Language Models (LLMs) to help you brainstorm and generate structured ideas for any concept. It acts as your personal AI strategist, breaking down vague concepts into actionable angles like target users, business models, technologies, and ethical considerations.

## Features

-   **Structured Brainstorming:** Generates 5 distinct angles for any concept.
-   **Key Categories:** Covers Target Users, Core Problem Solved, Potential Business Models/Monetization, Key Technologies/Features, and Ethical/Societal Considerations.
-   **LLM-Powered:** Utilizes powerful LLM APIs (e.g., Google Gemini) for intelligent idea generation.
-   **CLI Interface:** Easy to use directly from your terminal.

## How to Use

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/Arjun-1410/IdeaSpark-tool.git](https://github.com/Arjun-1410/IdeaSpark-tool.git) # REPLACE with your actual repo URL
    cd IdeaSpark-tool
    ```
2.  **Set up your API Key:**
    * Obtain a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Set it as an environment variable named `GOOGLE_API_KEY` (CRITICAL for security):
        * **Windows (Admin Command Prompt):** `setx GOOGLE_API_KEY "YOUR_ACTUAL_API_KEY_HERE"`
        * **Linux/macOS (add to ~/.bashrc or ~/.zshrc):** `export GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"`
        * **Remember to close and reopen your terminal after setting `setx`!**
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows (Command Prompt):
    .\venv\Scripts\activate.bat
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    ```
4.  **Install dependencies:**
    ```bash
    pip install requests
    ```
5.  **Run the tool:**
    ```bash
    python ideaspark.py
    ```
    Follow the prompts to enter your concept.

## Example Interaction