# ideaspark.py
# A dynamic brainstorming partner using Google Gemini Large Language Models.
# Generates structured brainstorming angles for a given concept.
# Created by Arjun
# Date: 30-07-2025
print("--- SCRIPT STARTING ---")
import os        # To access environment variables
import json      # To work with JSON data
import requests  # To make HTTP requests to the Gemini API
import sys       # To exit the script gracefully

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")


if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not found.")
    print("Please ensure you have set it permanently using 'setx GOOGLE_API_KEY \"YOUR_KEY_HERE\"' in an Administrator Command Prompt,")
    print("and then closed and reopened your terminal/VS Code.")
    sys.exit(1)

# Google Gemini API endpoint for generateContent
LLM_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def get_llm_response(prompt_text):
    """
    Sends a prompt to the Google Gemini LLM API and returns the generated structured data.
    It requests the LLM to output JSON based on a predefined schema.
    """
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "idea": {"type": "STRING", "description": "The original concept provided by the user"},
            "angles": {
                "type": "ARRAY",
                "description": "A list of distinct brainstorming angles for the concept",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "category": {"type": "STRING", "description": "The name of the brainstorming category (e.g., Target Users, Business Models)"},
                        "points": {
                            "type": "ARRAY",
                            "description": "3-5 specific bullet points for this category",
                            "items": {"type": "STRING"}
                        }
                    },
                    "required": ["category", "points"]
                }
            }
        },
        "required": ["idea", "angles"]
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        api_result = response.json()

        if api_result.get("candidates") and api_result["candidates"][0].get("content") and \
           api_result["candidates"][0]["content"].get("parts") and \
           api_result["candidates"][0]["content"]["parts"][0].get("text"):
            llm_response_json_string = api_result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(llm_response_json_string)
        else:
            if api_result.get("promptFeedback") and api_result["promptFeedback"].get("blockReason"):
                print(f"LLM blocked prompt due to: {api_result['promptFeedback']['blockReason']}")
                if api_result["promptFeedback"].get("safetyRatings"):
                    for rating in api_result["promptFeedback"]["safetyRatings"]:
                        print(f"  {rating['category']}: {rating['probability']}")
            else:
                print("Error: Unexpected or empty LLM response format.")
                print(json.dumps(api_result, indent=2))
            return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: Could not parse LLM's JSON response. Error: {e}")
        # Ensure llm_response_json_string is defined before trying to print it
        print(f"Raw LLM response string (might be incomplete/invalid JSON):\n{locals().get('llm_response_json_string', 'N/A')}")
        return None

# --- Main function definition ---
def main(): # This line should be at the same indentation level as the imports and helper functions
    """
    Main function to run the IdeaSpark brainstorming tool.
    Prompts user for a concept and displays structured brainstorming angles.
    """
    print("\n--- IdeaSpark: Your Dynamic Brainstorming Partner ---")
    print("Enter a vague concept, and I'll generate structured brainstorming angles for you.")
    print("Type 'exit' to quit.")

    while True:
        concept = input("\nEnter your concept (e.g., 'AI for fitness', 'sustainable tech'): ").strip()

        if concept.lower() == 'exit':
            print("Exiting IdeaSpark. Happy ideating!")
            break
        if not concept:
            print("Please enter a concept to brainstorm.")
            continue

        prompt = f"""
        You are an expert startup ideator and business strategist.
        Your task is to take the user's vague concept and generate 5 distinct, structured brainstorming angles.
        For each angle, provide 3-5 specific, actionable points.
        The angles should cover the following categories:
        - Target Users/Audience
        - Core Problem Solved
        - Potential Business Models/Monetization
        - Key Technologies/Features
        - Ethical/Societal Considerations

        Concept to brainstorm: "{concept}"
        """

        print("\nBrainstorming... Please wait a moment. (This may take 10-30 seconds)")
        brainstorm_result = get_llm_response(prompt)

        if brainstorm_result:
            print("\n" + "="*30 + " BRAINSTORMING RESULTS " + "="*30)
            print(f"Original Concept: {brainstorm_result.get('idea', concept)}")
            print("="*80)

            for angle in brainstorm_result.get('angles', []):
                category = angle.get('category', 'Unknown Category')
                points = angle.get('points', [])
                print(f"\n--- {category.upper()} ---")
                if points:
                    for point in points:
                        print(f"  - {point}")
                else:
                    print("  (No specific points generated for this category)")
            print("\n" + "="*80)
        else:
            print("Failed to get a valid brainstorming response from the LLM. Please check your API key, network, or try a different concept.")

# --- Standard Python entry point ---
if __name__ == "__main__": # This line should be at the very beginning of the file, not indented.
    main() # This call to main() should be indented by 4 spaces relative to the 'if' line.