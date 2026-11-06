"""
Streamlit interface for PDF-based RAG question answering.

Run: streamlit run app.py
"""

from pathlib import Path
import streamlit as st

from ingest import ingest_documents, DOCUMENTS_DIR, INDEX_PATH, METADATA_PATH
from rag_pipeline import RAGPipeline, OLLAMA_MODEL

st.set_page_config(
    page_title="Intelligent Document QA | RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Intelligent Document Question Answering")
st.caption("Upload PDF documents and ask questions using RAG, FAISS, Sentence Transformers and Ollama.")

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

with st.sidebar:
    st.header("1. Upload PDF documents")
    uploaded_files = st.file_uploader(
        "Choose one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Build / Update Knowledge Base", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one PDF file.")
        else:
            saved_count = 0
            for uploaded_file in uploaded_files:
                safe_name = Path(uploaded_file.name).name
                destination = DOCUMENTS_DIR / safe_name
                destination.write_bytes(uploaded_file.getbuffer())
                saved_count += 1

            try:
                with st.spinner("Extracting PDF text, creating chunks and building FAISS index..."):
                    chunk_count = ingest_documents()
                st.success(f"Knowledge base created. {saved_count} PDF(s), {chunk_count} chunks indexed.")
                st.session_state.pop("rag_pipeline", None)
            except Exception as exc:
                st.error(f"Knowledge-base creation failed: {exc}")

    st.divider()
    st.caption(f"LLM: {OLLAMA_MODEL}")
    st.caption("Make sure Ollama is installed and the model has been pulled locally.")

if INDEX_PATH.exists() and METADATA_PATH.exists():
    st.success("Knowledge base is ready.")
else:
    st.info("Upload PDF documents in the sidebar and build the knowledge base to begin.")

st.header("2. Ask a question")
question = st.text_area(
    "Enter your question about the uploaded documents",
    placeholder="Example: What are the main objectives described in the document?",
    height=100
)

if st.button("Get Answer", type="primary", disabled=not (INDEX_PATH.exists() and METADATA_PATH.exists())):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching documents and generating an answer..."):
                if "rag_pipeline" not in st.session_state:
                    st.session_state.rag_pipeline = RAGPipeline()
                answer, sources = st.session_state.rag_pipeline.answer(question)

            st.subheader("Answer")
            st.write(answer)

            with st.expander("View retrieved source passages"):
                for i, source in enumerate(sources, start=1):
                    st.markdown(
                        f"**{i}. {source['source']} — page {source['page']} "
                        f"(similarity: {source['score']:.3f})**"
                    )
                    st.write(source["text"])
                    st.divider()

        except Exception as exc:
            st.error(
                f"Could not generate an answer: {exc}\n\n"
                "Check that Ollama is running and that the configured model is installed."
            )

st.caption("Answers are generated from retrieved document passages. Verify important information against the original PDF.")
