"""
PDF ingestion pipeline:
PDF files -> text extraction -> overlapping chunks -> SentenceTransformer
embeddings -> FAISS vector index.

Run manually: python ingest.py
Or call ingest_documents() from app.py after uploading PDFs.
"""

from pathlib import Path
import json
import re

import faiss
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
DOCUMENTS_DIR = ROOT / "documents"
VECTORSTORE_DIR = ROOT / "vectorstore"
INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def extract_pdf_pages(pdf_path: Path):
    """Return non-empty page text with one-based page numbers."""
    pages = []
    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text")
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                pages.append({"text": text, "page": page_number})
    return pages


def split_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping character chunks, preferring word boundaries."""
    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")

    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start + int(chunk_size * 0.6):
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        start = max(end - overlap, start + 1)

    return chunks


def ingest_documents():
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {DOCUMENTS_DIR}. Upload or copy PDF files there first."
        )

    records = []
    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        for page_data in extract_pdf_pages(pdf_path):
            for chunk_number, chunk in enumerate(split_text(page_data["text"]), start=1):
                records.append({
                    "text": chunk,
                    "source": pdf_path.name,
                    "page": page_data["page"],
                    "chunk": chunk_number
                })

    if not records:
        raise ValueError(
            "No extractable text was found. If your PDF contains scanned images, "
            "OCR is required; this starter version extracts embedded PDF text."
        )

    print(f"Creating embeddings for {len(records)} chunks...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [record["text"] for record in records]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))
    METADATA_PATH.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\nIngestion completed successfully.")
    print(f"PDF files processed : {len(pdf_files)}")
    print(f"Text chunks created : {len(records)}")
    print(f"FAISS index saved   : {INDEX_PATH}")
    print(f"Metadata saved      : {METADATA_PATH}")
    return len(records)


if __name__ == "__main__":
    ingest_documents()
