import os
from huggingface_hub import InferenceClient
from .prompt_templates import get_comment_prompt

hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
client = InferenceClient(token=hf_token)

def generate_comment(code_snippet: str) -> str:
    prompt = get_comment_prompt(code_snippet)

    # Example using google/flan-t5-base or any text2text model
    model_id = "google/flan-t5-base"

    response = client.text_generation(
        model=model_id,
        inputs=prompt,
        parameters={"max_new_tokens": 512, "temperature": 0.2}
    )
    return response[0]['generated_text'].strip()

def comment_file(file_path: str) -> None:
    with open(file_path, "r") as f:
        original_code = f.read()

    commented_code = generate_comment(original_code)

    output_path = file_path.replace(".py", "_commented.py")
    with open(output_path, "w") as f:
        f.write(commented_code)

    print(f"[✅] Commented file saved to: {output_path}")
