import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompt import QA_PROMPT

load_dotenv()

def answer_question(question, vector_db, top_k=4):
    """
    Retrieves top chunks from FAISS, constructs context, and invokes Groq LLM.
    """
    if vector_db is None:
        return "Please upload and process documents first.", []

    # Search top-k vector matches
    retriever = vector_db.as_retriever(search_kwargs={"k": top_k})
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return "I could not find this information in the uploaded documents.", []

    # Build context string with metadata citations
    context_str = ""
    sources = []
    for doc in retrieved_docs:
        source_name = doc.metadata.get("source", "Unknown Document")
        page_num = doc.metadata.get("page", "Unknown Page")
        context_str += f"[Source: {source_name}, Page: {page_num}]\n{doc.page_content}\n\n"
        sources.append({"source": source_name, "page": page_num})

    # Format Prompt
    formatted_prompt = QA_PROMPT.format(context=context_str, question=question)

    # Call Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.0
    )

    response = llm.invoke(formatted_prompt)

    # Deduplicate source list
    unique_sources = []
    seen = set()
    for s in sources:
        pair = (s["source"], s["page"])
        if pair not in seen:
            seen.add(pair)
            unique_sources.append(s)

    return response.content, unique_sources