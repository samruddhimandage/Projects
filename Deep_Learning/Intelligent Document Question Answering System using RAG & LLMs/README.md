# Intelligent Document Question Answering System using RAG & LLMs

## Overview
A PDF question-answering application using Retrieval-Augmented Generation (RAG).
It extracts PDF text, splits it into overlapping chunks, creates semantic embeddings
with Sentence Transformers, stores/searches vectors using FAISS, and sends retrieved
context to an Ollama-hosted Llama 3.2 model. A Streamlit interface supports PDF
upload and interactive questions.

## Technology stack
- Python
- Streamlit
- PyMuPDF (PDF text extraction)
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS CPU (vector similarity search)
- Ollama
- Llama 3.2:1b
- NumPy

## Project structure
```text
Intelligent_Document_QA_RAG/
├── documents/             # Uploaded PDF documents
├── vectorstore/           # Generated FAISS index and metadata
├── app.py                 # Streamlit user interface
├── ingest.py              # PDF extraction, chunking and embedding
├── rag_pipeline.py        # Retrieval and Ollama answer generation
├── requirements.txt
└── README.md
```

## Prerequisites
1. Python 3.10 or 3.11 recommended (use a version supported by your packages).
2. Internet connection for the first Sentence Transformers model download.
3. Ollama installed and running locally.
4. Enough RAM/disk for the embedding model and PDF files.

## Windows setup
Open VS Code terminal in the project folder:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Install and start Ollama
Install Ollama from https://ollama.com/download

Then in a terminal:

```powershell
ollama pull llama3.2:1b
ollama run llama3.2:1b
```

Keep Ollama running. If `ollama run` opens an interactive prompt, you can exit
that prompt after the model has downloaded; the Ollama background service should
remain available. If the service is not running, start Ollama from the desktop app
or run `ollama serve` in a separate terminal.

## Run the application
From the project folder:

```powershell
streamlit run app.py
```

1. Open the local Streamlit URL shown in the terminal.
2. Upload one or more text-based PDF documents in the sidebar.
3. Click **Build / Update Knowledge Base**.
4. Enter a question and click **Get Answer**.
5. Expand retrieved source passages to inspect document/page evidence.

## Optional command-line ingestion
Place PDF files in `documents/`, then run:

```powershell
python ingest.py
```

## How it works
1. PyMuPDF extracts text page by page.
2. Text is split into 1,000-character chunks with 150-character overlap.
3. Sentence Transformers creates normalized embeddings.
4. FAISS `IndexFlatIP` stores vectors and performs similarity retrieval.
5. The top four matching chunks are supplied as context to Ollama.
6. Llama 3.2 generates an answer constrained to the retrieved context.
7. Streamlit displays the answer and source filename/page references.

## Important limitations
- This version extracts embedded text from PDFs. Scanned/image-only PDFs need OCR,
  which is not included.
- FAISS uses an in-memory flat index persisted to disk; it is suitable for a small
  local project, not a distributed production vector database.
- The app rebuilds the vector index from all PDFs currently in `documents/` when
  the knowledge base button is clicked.
- LLM answers can still be incorrect. Check source passages and original documents.
- The configured Ollama model is `llama3.2:1b`; change `OLLAMA_MODEL` in
  `rag_pipeline.py` if you have installed another local model.

## Troubleshooting
- **No PDFs found:** upload PDFs through Streamlit or copy them into `documents/`.
- **Ollama connection error:** open the Ollama app or start `ollama serve`.
- **Model not found:** run `ollama pull llama3.2:1b`.
- **FAISS install error:** confirm your Python version and install `faiss-cpu`
  in the active virtual environment.
- **No text extracted:** the PDF may be scanned; OCR is needed for scanned pages.
