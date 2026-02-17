import json
import sys
import webbrowser
from pathlib import Path

from modules.parser import extract_links_from_cv
from modules.extractor import extract_cv_data
from modules.generator import get_user_preferences, generate_html, save_site

# ── HELPERS ───────────────────────────────────────────────────────────────────

def pick_cv_file() -> tuple[str, str]:
    """
    Find PDFs in the cv/ folder.
    If there's only one, use it automatically.
    If there are multiple, ask the user to pick.
    Returns (filename, cv_text).
    """
    cvs = extract_links_from_cv()

    if not cvs:
        print("✘  No PDF files found in the cv/ folder.")
        print("   Add a CV PDF to cv/ and run again.")
        sys.exit(1)

    if len(cvs) == 1:
        filename, cv_payload = next(iter(cvs.items()))
        print(f"✔  Found CV: {filename}")
        return filename, cv_payload

    # Multiple CVs — let user pick
    print("\n┌─ MULTIPLE CVs FOUND ──────────────────")
    files = list(cvs.items())
    for i, (name, _) in enumerate(files, 1):
        print(f"│  [{i}] {name}")
    choice = input("└─ Choose a CV: ").strip()

    try:
        idx = int(choice) - 1
        filename, text = files[idx]
        return filename, text
    except (ValueError, IndexError):
        print("✘  Invalid choice.")
        sys.exit(1)

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════╗")
    print("║       CV → PORTFOLIO GENERATOR       ║")
    print("╚══════════════════════════════════════╝")

    # Step 1 — Pick CV
    filename, cv_payload = pick_cv_file()

    cv_text, cv_links = cv_payload["text"], cv_payload["links"]

    # Step 2 — Extract structured data
    print("\n⟳  Extracting CV data...")
    try:
        cv_data = extract_cv_data(cv_text, cv_links)
    except Exception as e:
        print(f"✘  Failed to extract CV data: {e}")
        print("   Try running again — LLM output can occasionally be malformed.")
        sys.exit(1)

    name = cv_data.get("personal", {}).get("name", "portfolio")
    print(f"✔  Extracted data for: {name}")

    # Optional: save the extracted JSON for inspection
    json_out = Path("output") / f"{name.lower().replace(' ', '_')}_data.json"
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(cv_data, indent=2), encoding="utf-8")
    print(f"✔  CV data saved to: {json_out}")

    # Step 3 — Get user preferences
    theme, accent = get_user_preferences()
    print(f"\n✔  Theme: {theme}  |  Accent: {accent}")

    # Step 4 — Generate HTML
    try:
        html = generate_html(cv_data, theme, accent)
    except ValueError as e:
        print(f"✘  {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✘  HTML generation failed: {e}")
        sys.exit(1)

    # Step 5 — Save site
    output_dir = save_site(html, name)
    index_path = output_dir / "index.html"

    print(f"\n✔  Site saved to: {output_dir}")
    print(f"✔  Open in browser: {index_path}")

    # Step 6 — Offer to open in browser
    open_choice = input("\n   Open in browser now? [Y/n]: ").strip().lower() or "y"
    if open_choice == "y":
        webbrowser.open(index_path.resolve().as_uri())
        print("✔  Opened!")

    print("\n✨  Done!\n")

if __name__ == "__main__":
    main()