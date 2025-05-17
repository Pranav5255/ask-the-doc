import torch
torch.__path__ = []
import streamlit as st
from utils import extract_texts
from rag_chain import get_answer

st.set_page_config(page_title="Ask the Docs", layout="wide")
st.title(" Ask the Docs – Mini RAG App")

tab1, tab2, tab3 = st.tabs(["🧾 Ask", "📜 History", "ℹ️ About"])

if "history" not in st.session_state:
    st.session_state.history = []

with tab1:
    uploaded_files = st.file_uploader(
        "Upload one or more .pdf or .txt files", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    question = st.text_input("Ask a question about the document(s):")

    if uploaded_files and question:
        with st.spinner("Processing..."):
            full_text = extract_texts(uploaded_files)
            answer = get_answer(full_text, question)
            st.success(answer)
            st.session_state.history.append((question, answer))

with tab2:
    st.subheader("Previous Questions & Answers")
    if not st.session_state.history:
        st.info("No history yet.")
    else:
        for q, a in reversed(st.session_state.history):
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
            st.markdown("---")

with tab3:
    st.markdown("""
    ### 🤖 Ask the Docs – Mini RAG Web App  
    Upload `.pdf` or `.txt` files and ask questions about them.  
    The app uses:
    - LangChain for document chunking and QA
    - FAISS for vector search
    - Gemini API for response generation  
    
    """)
