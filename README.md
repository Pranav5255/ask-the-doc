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
├── .github/workflows    # Automate Docker build, push and deploy
├── rag_chain.py         # LLM Logic
├── utils.py             # Utility functions
├── main.py              # Streamlit app
├── requirements.txt     # Python dependencies
├── Dockerfile
```


## ⚙️ Setup Instructions

### Local Development

```bash

python -m venv venv
source venv/bin/activate  # For Linux/macOS
# .\venv\Scripts\activate  # For Windows
pip install -r requirements.txt
streamlit run app.py
```

Disclaimer: I have used Gemini-2.0-Flash model to analyse the documents. But it has a limit on the no. of pages it can handle at a time. 

I have created the Dockerfile such that it can be deployed on an AWS EC2 instance or via AWS ECS Fargate Service. So keep in mind that while creating the Dockerfile, it should be Linux compatible as Windows files can cause deployment failures.

I have also successfully automated the deployment tasks right from uploading the Docker Image to the AWS Elastic Container Registry to Deployment from Amazon Elastic Container Service Fargate!!

## 📦 Docker and CI/CD Deployment (AWS ECS + ECR)
This project includes a GitHub Actions CI/CD pipeline that:

- Runs tests and linting
- Builds and pushes the Docker image to AWS Elastic Container Registry (ECR)
- Deploys the container to Amazon Elastic Container Service (ECS) using Fargate

### 🧰 Prerequisites
- AWS ECR Repository (```ask-the-doc-repo```)
- ECS Cluster (```ask-the-doc-cluster```)
- ECS Service (```ask-the-doc-task-service```)
- ECS Task Definition (```ask-the-doc-task```)
- Secrets configured in GitHub:
  - ```AWS_ACCESS_KEY_ID```
  - ```AWS_SECRET_ACCESS_KEY```

### 🔄 GitHub Actions Workflow
The GitHub Actions workflow aws-ecr-push.yml contains three jobs:

#### 🧪 ```test```
- Sets up Python 3.11
- Installs dependencies
- Runs ```flake8``` linting and ```pytest``` (if configured)

#### 🛠️ ```build-and-push```
- Builds the Docker image using ```Buildx```
- Tags the image with latest and Git SHA
- Pushes the image to AWS ECR

#### 🚀 ```deploy-to-ecs```
- Downloads the current ECS task definition
- Renders a new task definition with the updated image
- Deploys it to ECS using ```aws-actions/amazon-ecs-deploy-task-definition```

### 🔄 Trigger Conditions
The pipeline triggers on:
- Pushes to ```main``` branch
- Pull requests to ```main```
- Manual trigger via GitHub UI (```workflow_dispatch```)
  

## ✅ Result
After pushing to ```main```, GitHub Actions will:
- Test and lint your code
- Build and push the Docker image to ECR
- Deploy the updated image to ECS
- Automatically update the ECS service and wait for stability

