# cv-website-gen

A command-line tool that takes a PDF CV and generates a personal portfolio website from it. You drop a CV in, pick a colour scheme, and get a self-contained HTML/CSS site out.

Built as a learning project to get hands-on with [Ollama](https://ollama.com) and local LLM inference in Python. The code was largely vibe-coded with Claude — not to produce something production-ready, but to explore what local LLMs are actually good at and where they fall over.

---

## How it works

1. **Parse** — extracts raw text and hyperlinks from the PDF using `pdfplumber`
2. **Extract** — sends the text to a local Ollama model (`mistral:7b`) which returns structured JSON
3. **Render** — the JSON is rendered into a complete HTML site using a Jinja2 template
4. **Output** — the site is saved to `output/{name}/` with `index.html` and `style.css`

The LLM is only used for the extraction step. HTML generation is handled entirely by the Jinja2 template, which turned out to be far more reliable than asking an LLM to write the HTML directly.

---

## Requirements

- [Ollama](https://ollama.com) installed and running locally
- `mistral:7b` pulled: `ollama pull mistral:7b`
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management

---

## Setup

```bash
git clone https://github.com/yourusername/cv-website-gen
cd cv-website-gen
uv sync
```

---

## Usage

Drop your CV PDF into the `cv/` folder, then run:

```bash
uv run main.py
```

You'll be prompted to choose a light or dark theme and an accent colour. The generated site lands in `output/{your-name}/`.

An intermediate JSON file is also saved to `output/` so you can inspect what the extractor pulled out — useful if something looks wrong in the final site.

---

## Project structure

```
cv-website-gen/
├── cv/                         # put your CV PDF here
├── modules/
│   ├── parser.py               # PDF text and hyperlink extraction
│   ├── extractor.py            # Ollama JSON extraction
│   └── generator.py           # Jinja2 rendering and file output
├── prompts/
│   └── extraction_prompt.txt  # system prompt for mistral:7b
├── template/
│   ├── style.css               # master stylesheet
│   └── portfolio.html.jinja2  # HTML template
├── output/                     # generated sites appear here
├── main.py
├── pyproject.toml
└── uv.lock
```

---

## Design

The generated site uses a monospace font stack (JetBrains Mono), a vertical timeline layout for experience and education, and CSS custom properties for theming. Light/dark mode and accent colour are chosen at runtime and injected into the HTML at render time — no JavaScript frameworks, no build step.

---

## Motivation

The goal was to learn how to work with Ollama's Python library, understand where local LLMs are useful in a real pipeline, and figure out how to get consistent structured output from a small model. The CV generator was just a good excuse — something with a tangible visual output that touches real problems like prompt engineering, JSON validation, and PDF parsing.

`mistral:7b` was chosen for the extraction step after testing several models. It handles structured JSON output more reliably than same-size alternatives at this task.

---

## Known limitations

- Date normalisation from PDFs is imperfect — the extractor occasionally produces `Jan2024` instead of `01/2024`
- LinkedIn and GitHub links must be proper hyperlinks in the PDF to be extracted correctly. Plain text handles like `github.com/user` may be missed
- Only PDF input is supported currently

---

## Dependencies

- [ollama](https://github.com/ollama/ollama-python) — Python client for Ollama
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text and annotation extraction
- [jinja2](https://jinja.palletsprojects.com/) — HTML templating
