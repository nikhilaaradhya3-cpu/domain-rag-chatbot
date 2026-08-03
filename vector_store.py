import os
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_DIR = "vector_store/saved_index"

def get_embedding_model():
    """Loads all-MiniLM-L6-v2 using FastEmbed to bypass PyTorch dependencies."""
    return FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_and_save_vector_store(chunks, save_path=INDEX_DIR):
    """Creates FAISS vector database and saves it locally."""
    embeddings = get_embedding_model()
    vector_db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(save_path, exist_ok=True)
    vector_db.save_local(save_path)
    return vector_db

def load_vector_store(save_path=INDEX_DIR):
    """Loads existing FAISS vector database from disk."""
    embeddings = get_embedding_model()
    if os.path.exists(save_path) and os.path.exists(os.path.join(save_path, "index.faiss")):
        return FAISS.load_local(
            save_path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    return None