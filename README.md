# Domain-Specific RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from uploaded PDF documents — such as course notes, company policies, manuals, or training material — grounded strictly in the content of those documents.

## Features

- Upload one or more PDF files
- Automatic text extraction, chunking, and embedding
- Fast semantic search using FAISS
- Grounded answers generated via Groq's Llama 3.3 70B model
- Every answer cites its source document and page number
- Refuses to answer when the information isn't in the uploaded documents

## Architecture

   ![Architecture Diagram](docs/architecture.png)

   
## Architecture

Upload PDFs → Extract text (pypdf) → Chunk text (LangChain splitter) → Generate embeddings (all-MiniLM-L6-v2) → Store in FAISS → Retrieve top-k relevant chunks per question → Send context + question to LLM (Groq) → Display grounded answer with source citations

## Setup

1. **Clone the repository:**
````bash
   git clone https://github.com/nikhilaaradhya3-cpu/domain-rag-chatbot.git
   cd domain-rag-chatbot
````

2. **Install dependencies:**

````bash
   pip install -r requirements.txt
````

3. **Set up your API key:**
   Create a `.env` file in the project root with:

````
   GROQ_API_KEY=your_groq_api_key_here
````

4. **Run the application:**

````bash
   streamlit run app.py
````

   This will open the app in your browser at `http://localhost:8501`.

## Usage

1. In the sidebar, upload one or more PDF files.
2. Click **Process Documents** to extract, chunk, and embed the content.
3. Type a question in the chat box at the bottom.
4. The chatbot will answer using only the content of your uploaded documents, and show the source document and page number below each answer.
5. Use **Clear Chat** to reset the conversation.

## Live Demo

Try the deployed app here: [Domain-Specific RAG Chatbot](https://domain-rag-chatbot-3isqgaqdft9uqlbvmvm8ru.streamlit.app/)

## Sample Documents

The `sample_documents/` folder contains example PDFs for testing the chatbot.

## Responsible AI Note

This chatbot answers strictly from the content of uploaded documents and will state when information is not available rather than inventing an answer. Users should verify high-stakes information independently. API keys are never committed to the repository.

````

Save it, then commit and push:
````

git add README.md
git commit -m "Add README with setup and usage instructions"
git push

````

Let me know once that's pushed, and we'll move to #2 — sample PDF documents.
