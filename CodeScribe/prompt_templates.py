# prompt_templates.py

def get_comment_prompt(code_snippet):
    """
    Builds the full prompt to give to the LLM, including the code snippet.
    """
    return f"""
You are a helpful AI assistant. Add helpful inline comments and docstrings to the following Python code. 
Keep the original structure. Add comments above each function and explain key lines.

Code:
```python
{code_snippet}

"""