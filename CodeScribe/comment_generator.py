import os
from huggingface_hub import InferenceClient
from .prompt_templates import get_comment_prompt

hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
client = InferenceClient(token=hf_token)

def generate_comment(code_snippet: str) -> str:
    prompt = get_comment_prompt(code_snippet)

    model_id = "facebook/opt-1.3b"  # An open source code generation model available on HF inference API


    response = client.text_generation(prompt, model=model_id)

    return response[0]['generated_text'].strip()

def comment_file(file_path: str) -> None:
    with open(file_path, "r") as f:
        original_code = f.read()

    commented_code = generate_comment(original_code)

    output_path = file_path.replace(".py", "_commented.py")
    with open(output_path, "w") as f:
        f.write(commented_code)

    print(f"[✅] Commented file saved to: {output_path}")
