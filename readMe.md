# docuMentor 🧠📄

**docuMentor** is an AI-powered tool that brings together **LocalRQA** and **CodeScribe** into a unified system. It allows users to upload documents, ask questions, and receive accurate answers locally using Retrieval-Augmented Generation (RAG). Additionally, it supports automatic Python code commenting, helping developers understand and document their code with ease.

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
- Node.js & npm/yarn (for frontend)
- CUDA-enabled GPU (optional, for model training)
- Git

### Clone the Repository

```bash
git clone https://github.com/Adith1207/docuMentor.git
cd docuMentor
pip install -r requirements.txt
```

### Backend setup
```bash
cd backend
pip install -r requirements.txt
```

### frontend setup

```bash
cd ../frontend
npm install # or yarn install
npm run dev # start development server
```


## ⚡ Usage

### SnapShots:

![Alt text](./Sample_Img/WhatsApp%20Image%202025-10-04%20at%209.49.32%20AM.jpeg)
![Alt text](./Sample_Img/WhatsApp%20Image%202025-10-04%20at%209.49.33%20AM.jpeg)
![Alt text](<./Sample_Img/WhatsApp%20Image%202025-10-04%20at%209.49.34%20AM%20(1).jpeg>)
![Alt text](./Sample_Img/WhatsApp%20Image%202025-10-04%20at%209.49.34%20AM.jpeg)

### 1. LocalRQA: Ask Questions on Documents

- Supports PDF, TXT, HTML
- Returns answer and source passage

### 2. CodeScribe: Comment Python Code

- Automatically adds function-level and inline comments
- Optionally supports batch commenting for multiple files

## 🤝 Contributing

We welcome contributions! You can:

- Report issues or bugs
- Suggest new features
- Contribute to additional language support
- Improve evaluation scripts

## 📜 License

docuMentor is licensed under the MIT License — free for academic and commercial
