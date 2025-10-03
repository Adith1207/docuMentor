from src.models import Models

# Prompt template for generating comments
COMMENT_PROMPT_TEMPLATE = """
You are a helpful assistant that adds Python docstrings and inline comments.
- Keep the original code structure intact.
- Add a short module-level description if missing.
- Add concise docstrings for functions and classes.
- Add short inline comments for non-trivial lines.
- IMPORTANT: Return ONLY the modified Python code inside a ```python code block.
- Do NOT include any explanations or instructions outside the code block.

Code:
```python
{code}
"""
def generate_comment(code_snippet: str, max_tokens: int = 512) -> str:
    """Generate commented Python code from a given snippet."""
    tokenizer, model = Models.generator()
    prompt = COMMENT_PROMPT_TEMPLATE.format(code=code_snippet)

    # Prepare input
    inputs = tokenizer(prompt, return_tensors='pt', truncation=True).to(model.device)

    # Generate output
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode text
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only Python code block
    result = ""
    if "```python" in text:
        s = text.split("```python")[-1]
        if "```" in s:
            s = s.split("```")[0]
        result = s.strip()
    else:
        # Fallback: keep only Python-like lines
        lines = text.splitlines()
        result = "\n".join(
            line for line in lines
            if line.strip().startswith(("def", "class", "#", "\"\"\"", "import", "from"))
            or line.strip() == "" or line.startswith("    ")
        ).strip()

    # Final safeguard
    if not result:
        result = code_snippet  # fallback to original code if model fails

    return result
