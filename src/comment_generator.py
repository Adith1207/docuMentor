from src.models import Models

# Keep prompt compact and structured to fit context window
COMMENT_PROMPT_TEMPLATE = """
You are a helpful assistant that adds docstrings and inline comments to Python code. Keep original code structure. Add a short module-level description if missing, add docstrings for functions and classes, and add short inline comments for non-trivial lines.

Code:
```python
{code}
Provide only the commented code (do not add extra explanation outside code block).
"""

def generate_comment(code_snippet: str, max_tokens: int = 512) -> str:
    tokenizer, model = Models.generator()
    prompt = COMMENT_PROMPT_TEMPLATE.format(code=code_snippet)
    inputs = tokenizer(prompt, return_tensors='pt', truncation=True).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.2,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # keep only the code block returned (if model returns prompt+reply)
    if "```python" in text:
        s = text.split("```python")[-1]
        if "```" in s:
            s = s.split("```")[0]
        return s.strip()
    return text.strip()