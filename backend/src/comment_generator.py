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
def _extract_python_code(text: str) -> str:
    """Extract only the Python code block from the model's output."""
    if "```python" in text:
        s = text.split("```python", 1)[1]
        if "```" in s:
            s = s.split("```", 1)[0]
        return s.strip()
    return text.strip()


def generate_comment(code_snippet: str, max_tokens: int = 512) -> str:
    """Generate commented Python code from a given snippet using Gemini only."""
    prompt = COMMENT_PROMPT_TEMPLATE.format(code=code_snippet)

    try:
        text = Models.generate_gemini(prompt, max_tokens)
        result = _extract_python_code(text)
        if result:
            return result
        return text.strip() or code_snippet
    except Exception as e:
        print(f"[CommentGenerator] Gemini failed: {e}")
        # Fallback: return original code if Gemini not available
        return code_snippet
