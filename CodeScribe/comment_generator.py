# comment_generator.py

import os
from .prompt_templates import get_comment_prompt


# Option 1: Using OpenAI (or switch to HuggingFace later)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure it's set in your environment

def generate_comment(code_snippet):
    """
    Sends code to LLM with prompt and returns commented code.
    """
    prompt = get_comment_prompt(code_snippet)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use your own local model if needed
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def comment_file(file_path):
    """
    Reads a .py file, adds comments, saves new file.
    """
    with open(file_path, "r") as f:
        original_code = f.read()

    commented_code = generate_comment(original_code)

    output_path = file_path.replace(".py", "_commented.py")
    with open(output_path, "w") as f:
        f.write(commented_code)

    print(f"[✅] Commented file saved to: {output_path}")
