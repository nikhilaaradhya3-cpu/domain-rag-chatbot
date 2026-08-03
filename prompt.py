from langchain_core.prompts import PromptTemplate

PROMPT_TEMPLATE = """You are a document question-answering assistant.
Answer only from the supplied context. If the answer is not available, say:
"I could not find this information in the uploaded documents." Do not invent facts.

Context:
{context}

Question:
{question}

Answer:"""

QA_PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)