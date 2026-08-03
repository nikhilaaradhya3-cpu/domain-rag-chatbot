import streamlit as st
import os
from dotenv import load_dotenv

from document_loader import process_uploaded_pdfs
from vector_store import create_and_save_vector_store, load_vector_store
from rag_pipeline import answer_question

load_dotenv()

st.set_page_config(page_title="Domain-Specific RAG Chatbot", layout="wide")

st.title("📄 Domain-Specific RAG Chatbot")
st.caption("Upload domain documents (PDFs) and ask questions grounded strictly in their content.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Document Management")
    uploaded_files = st.file_uploader(
        "Upload PDF files", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents", type="primary"):
        if uploaded_files:
            with st.spinner("Extracting text, chunking, and creating embeddings..."):
                chunks = process_uploaded_pdfs(uploaded_files)
                vector_db = create_and_save_vector_store(chunks)
                st.session_state.vector_db = vector_db
                st.success(f"Processed {len(uploaded_files)} file(s) into {len(chunks)} text chunks!")
        else:
            st.error("Please upload at least one PDF file first.")

    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Maintain Session States
if "vector_db" not in st.session_state:
    st.session_state.vector_db = load_vector_store()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.markdown("---")
            st.markdown("**📌 Sources:**")
            for src in message["sources"]:
                st.caption(f"• Document: `{src['source']}` | Page: `{src['page']}`")

# Handle User Input
if prompt := st.chat_input("Ask a question based on your uploaded PDFs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents & generating answer..."):
            answer, sources = answer_question(prompt, st.session_state.vector_db)
            st.markdown(answer)
            
            if sources:
                st.markdown("---")
                st.markdown("**📌 Sources:**")
                for src in sources:
                    st.caption(f"• Document: `{src['source']}` | Page: `{src['page']}`")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })