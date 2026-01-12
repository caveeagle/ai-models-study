
# pip install langchain-community langchain-core langchain-google-genai
# pip install faiss-cpu

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

import secret_config

############################################

# -------------------------
# Load document
# -------------------------

text_file = 'becode_rules.txt'

with open(text_file, "r", encoding="utf-8") as f:
    text = f.read()

# -------------------------
# Split into chunks
# -------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_text(text)

# -------------------------
# Embeddings (Gemini)
# -------------------------

API_KEY = secret_config.API_KEY

if not API_KEY or not API_KEY.strip():
    raise ValueError("API_KEY is empty or not set")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=API_KEY
)

# -------------------------
# Vector store (cosine)
# -------------------------
db = FAISS.from_texts(chunks, embeddings)

# -------------------------
# Retriever
# -------------------------

TOP_K = 5

retriever = db.as_retriever(search_kwargs={"k": TOP_K})

# -------------------------
# Gemini LLM
# -------------------------

TEMPERATURE = 0.2  # true value = 0.2


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=API_KEY,
    temperature=TEMPERATURE,
    max_output_tokens=500
)

# -------------------------
# Query
# -------------------------
query = "What happens if I miss a BeCode deadline?"

docs = retriever.invoke(query)

context = "\n\n".join(d.page_content for d in docs)

prompt = f"""
Use only the rules below.

{context}

Question:
{query}
"""

print(llm.invoke(prompt).content)



print('Job finished')
