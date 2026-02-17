import json
from ollama import chat, ChatResponse
from pathlib import Path

EXTRACTION_SYSTEM_PROMPT = Path("prompts/extraction_prompt.txt").read_text(encoding="utf-8")

def extract_cv_data(cv_text: str, links: list[str] = []) -> dict:
    """Send CV text to Ollama and return structured JSON data"""

    links_str = "\n".join(links) if links else "None found"
    
    response: ChatResponse = chat(model='mistral:7b', messages=[
        {
            'role': 'system',
            'content': EXTRACTION_SYSTEM_PROMPT,
        },
        {
            'role': 'user',
            'content': f'Parse the following CV and return the JSON.\n\nCV TEXT:\n{cv_text}\n\nHYPERLINKS FOUND IN DOCUMENT:\n{links_str}',
        },
    ])

    raw = response.message.content.strip()

    # Safety net in case the model wraps in code fences anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw)