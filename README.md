# 🧠 Ask the Doc

**Ask the Doc** is a lightweight web app that allows users to upload documents (PDF or TXT), ask questions related to their content, and get instant answers using Retrieval-Augmented Generation (RAG).

## 🚀 Features

-  Upload support for PDF and TXT files
-  Ask questions directly from the uploaded document
-  Uses RAG (Retrieval-Augmented Generation) for precise answers
-  Streamlit-based frontend for interactive UI
-  Fast, local document processing

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Python (FastAPI)
- **Document Parsing:** PyMuPDF for PDFs, native handling for TXT
- **Embedding & Retrieval:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **LLM:** Gemini-2.0-Flash
- **Vector Store:** FAISS

## 📂 Project Structure

```plaintext
ask-the-docs/
├── rag_chain.py         # LLM Logic
├── utils.py             # Utility functions
├── main.py              # Streamlit app
├── requirements.txt     # Python dependencies
├── Dockerfile
├── README.md
```


## ⚙️ Setup Instructions

### Application Initialisation and Deployment

```bash

python -m venv venv
source venv/bin/activate  # For Linux/macOS
# .\venv\Scripts\activate  # For Windows
pip install -r requirements.txt
streamlit run app.py
```

Disclaimer: I have used Gemini-2.0-Flash model to analyse the documents. But it has a limit on the no. of pages it can handle at a time. 

I have created the Dockerfile such that it can be deployed on an AWS EC2 instance. So keep in mind that while creating the Dockerfile, it should be Linux compatible as Windows files can cause deployment failures.

I have also successfully automated the deployment tasks right from uploading the Docker Image to the AWS Elastic Container Registry to Deployment from Amazon Elastic Container Service Fargate!!

Here's how I did that:

