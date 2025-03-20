# pip install -q -U google-generativeai
# pip install -q -U google-genai
# pip show google-generativeai
# pip show google-genai

import google.generativeai as genai
import os

def generate_text(api_key, model, prompt):
    """
    Generates text using the Gemini API.

    Args:
        api_key: Your Google Gemini API key.
        prompt: The text prompt to send to the API.

    Returns:
        The generated text, or None if an error occurs.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    """
    Gets API key and prompt from the user, and generates text.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    model = "gemini-2.0-flash" # 'gemini-pro' or 'gemini-ultra' if you have access.
    prompt = input("Enter your prompt: ")

    generated_text = generate_text(api_key, model, prompt)

    if generated_text:
        print("\nGenerated Text:\n")
        print(generated_text)

if __name__ == "__main__":
    main()