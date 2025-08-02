import gradio as gr
from rag_model import answer_query

def qa_interface(query):
    return answer_query(query)

gr.Interface(fn=qa_interface,
             inputs="text",
             outputs="text",
             title="LocalRQA: Ask Your Code/Docs",
             description="Ask questions about your `.py` or `.txt` files.").launch()
