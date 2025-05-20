import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "false"

import tempfile
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Load Environment Variables ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env file")

# --- Embeddings and Vector Store ---
def create_vector_store(text_chunks):
    """Creates a FAISS vector store from text chunks using HuggingFace embeddings."""
    print("Using HuggingFace Embeddings (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    if not text_chunks:
        print("No text chunks to process for vector store.")
        return None
    try:
        print(f"Creating FAISS vector store with {len(text_chunks)} text chunks.")
        vector_store = FAISS.from_documents(text_chunks, embeddings)
        print("FAISS vector store created successfully.")
        return vector_store
    except Exception as e:
        print(f"Error creating FAISS vector store: {e}")
        raise

# --- QA Chain Setup ---
def setup_qa_chain(vector_store):
    """Sets up the RAG chain using Gemini LLM."""
    if not vector_store:
        return None

    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-pro-latest",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )
        print("Using Gemini LLM (gemini-flash).")
    except Exception as e:
        print(f"Could not initialize Gemini LLM: {e}. Check your API key and internet connection.")
        return None

    prompt_template = """You are an AI assistant for answering questions about the provided document.
Use only the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Be concise and informative.

Context:
{context}

Question: {question}

Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={'k': 3}),
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    return qa_chain

# --- Main QA Logic ---
def get_answer(text, question):
    """Processes text, creates a vector store, sets up the QA chain, and gets the answer."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in text_chunks]

    vectorstore = create_vector_store(docs)
    if vectorstore is None:
        return "Could not create vector store."

    qa_chain = setup_qa_chain(vectorstore)
    if qa_chain is None:
        return "Could not initialize the QA chain. Ensure you have a valid Gemini API key and internet connection."

    try:
        result = qa_chain.invoke({"query": question})
        return result['result']
    except Exception as e:
        print(f"Error during QA chain execution: {e}")
        return "An error occurred while trying to answer the question."

# --- Test Runner ---
if __name__ == '__main__':
    sample_text = """
    The quick brown fox jumps over the lazy dog.
    This is a sample document with some information.
    Langchain is a framework for developing applications powered by language models.
    It can be used for question answering, text summarization, and more.
    """
    sample_question = "What is Langchain used for?"
    answer = get_answer(sample_text, sample_question)
    print(f"Question: {sample_question}")
    print(f"Answer: {answer}")

    sample_question_2 = "What does the fox do?"
    answer_2 = get_answer(sample_text, sample_question_2)
    print(f"\nQuestion: {sample_question_2}")
    print(f"Answer: {answer_2}")

