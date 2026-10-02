# 📚 RAG Agent

A **Retrieval-Augmented Generation (RAG) application** that allows users to upload PDF documents and ask questions about their content.

The application uses **Streamlit** for the user interface, **LangChain/LangGraph** for the RAG and agent workflow, **Hugging Face Sentence Transformers** for local embeddings, and **Groq** for generating answers.

## 🚀 Features

- 📄 Upload one or multiple PDF documents
- 🔍 Extract text from PDF files
- ✂️ Split documents into smaller chunks
- 🤗 Generate embeddings using Hugging Face locally
- 🗄️ Store document embeddings in an in-memory vector store
- 🔎 Perform similarity search to retrieve relevant information
- 🤖 Use a LangChain agent for question answering
- ⚡ Use Groq for fast LLM responses
- 💬 Interactive chat interface using Streamlit
- 🔐 API key stored securely using environment variables

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **LangChain**
- **LangGraph**
- **Hugging Face Sentence Transformers**
- **Groq**
- **PyPDF**
- **InMemoryVectorStore**

## 📂 Project Structure

```text
rag-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── doc_files/
    └── .gitkeep
```

### File Description

| File / Folder | Description |
|---|---|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `.env` | Stores the Groq API key |
| `.gitignore` | Prevents sensitive/unnecessary files from being pushed |
| `doc_files/` | Stores uploaded PDF documents |
| `README.md` | Project documentation |

## 🔄 How It Works

```text
             PDF Upload
                  │
                  ▼
        ┌──────────────────┐
        │  PyPDF Loader    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Text Splitter    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │ Hugging Face Embeddings  │
        │ all-MiniLM-L6-v2         │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │ InMemory Vector Store    │
        └────────────┬─────────────┘
                     │
                     ▼
              User Question
                     │
                     ▼
        ┌──────────────────────────┐
        │ Similarity Search        │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │ Retrieved Context        │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │ LangChain Agent + Groq   │
        └────────────┬─────────────┘
                     │
                     ▼
                  Answer
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd rag-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

This project uses **Groq** for the LLM.

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not upload the `.env` file to GitHub.

The `.gitignore` file already excludes it.

## ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

## 📌 Important Notes

- Uploaded PDFs are stored temporarily in the `doc_files` directory.
- The vector database uses `InMemoryVectorStore`.
- The vector store is recreated when the application processes documents.
- The Hugging Face embedding model is downloaded the first time it is used.
- Keep your API keys private.
- Do not commit `.env` or PDF files to GitHub.

## 👨‍💻 Author

**Tirth Hirpara**
