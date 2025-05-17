from PyPDF2 import PdfReader

def extract_texts(files):
    combined_text = ""
    for file in files:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = file.read().decode("utf-8")
        combined_text += f"\n--- {file.name} ---\n{text}\n"
    return combined_text
