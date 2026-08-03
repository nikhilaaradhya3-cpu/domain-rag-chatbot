import os
import tempfile
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_uploaded_pdfs(uploaded_files):
    """
    Extracts text from uploaded PDF files, preserves page metadata,
    and splits the content into chunks.
    """
    documents = []

    for uploaded_file in uploaded_files:
        # Save file temporarily to extract text via pypdf
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            reader = PdfReader(temp_path)
            for page_idx, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():  # Skip empty pages
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": uploaded_file.name,
                            "page": page_idx + 1
                        }
                    )
                    documents.append(doc)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Chunking: 800 characters with 120 character overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)