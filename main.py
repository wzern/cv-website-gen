from ollama import chat
from ollama import ChatResponse
from modules.parser import extract_text_from_cv
from modules.extractor import extract_cv_data

cvs = extract_text_from_cv()
for filename, cv_text in cvs.items():
    print(f"--- {filename} ---")
    cv_data = extract_cv_data(cv_text)
    print(cv_data)