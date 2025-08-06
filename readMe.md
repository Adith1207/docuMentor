# docuMentor 🧠📄

**douMentor** is an AI-powered tool that brings together **LocalRQA** and **CodeScribe** into a unified system. It allows users to upload documents, ask questions, and receive accurate answers locally using Retrieval-Augmented Generation (RAG). Additionally, it supports automatic Python code commenting, helping developers understand and document their code with ease.

---

## 🚀 Key Features

- ✅ **Local Question Answering (LocalRQA):** Ask questions on uploaded documents and receive contextually relevant answers using open-source LLMs — all locally.
- 🧠 **LLM-Powered Code Commenting (CodeScribe):** Automatically generates detailed comments for Python files, improving code readability and maintainability.
- 🔐 **Privacy-first:** No cloud dependencies. Everything runs locally.

---

## 📚 Project Modules

### 1. LocalRQA: Local Retrieval-Augmented QA

Based on the paper:  
**"LocalRQA: From Generating Data to Locally Training, Testing, and Deploying Retrieval-Augmented QA Systems"**  
📎 [ACL Anthology](https://aclanthology.org/2024.acl-demos.14/) | [arXiv PDF](https://arxiv.org/pdf/2403.00982.pdf)

- Generates synthetic ⟨question, answer, passage⟩ triples from your documents
- Trains local retriever and generator models (e.g., ColBERTv2, LLaMA)
- Evaluates performance via automated metrics
- Fully deployable QA pipeline that works on PDFs, TXT, or HTML

### 2. CodeScribe: AI-based Code Commenter

Inspired by the tool described in:  
**"Leveraging Large Language Models for Code Translation and Software Development in Scientific Computing"**  
📎 [arXiv Link](https://arxiv.org/abs/2410.24119)

- Annotates Python files with function-level comments
- Uses custom prompt templates to maintain context
- Can be extended to other languages in future

---

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- CUDA-enabled GPU (recommended for training)
- Git, pip

### Clone the Repository

```bash
git clone https://github.com/Adith1207/docuMentor.git
cd docuMentor
pip install -r requirements.txt
```
