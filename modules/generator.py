import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ── ACCENT COLOUR PRESETS ─────────────────────────────────────────────────────

ACCENT_PRESETS = {
    "1": ("#6366f1", "Indigo"),
    "2": ("#10b981", "Emerald"),
    "3": ("#f59e0b", "Amber"),
    "4": ("#ef4444", "Red"),
    "5": ("#3b82f6", "Blue"),
    "6": ("#ec4899", "Pink"),
}

# ── USER PREFERENCES ──────────────────────────────────────────────────────────

def get_user_preferences() -> tuple[str, str]:
    """Ask the user to choose a theme and accent colour. Returns (theme, accent_hex)."""

    print("\n┌─ THEME ───────────────────────────────")
    print("│  [1] Dark")
    print("│  [2] Light")
    theme_choice = input("└─ Choose (default: 1): ").strip() or "1"
    theme = "dark" if theme_choice != "2" else "light"

    print("\n┌─ ACCENT COLOUR ───────────────────────")
    for key, (hex_val, name) in ACCENT_PRESETS.items():
        print(f"│  [{key}] {name:<10} {hex_val}")
    print("│  [c] Custom hex (e.g. #ff6b6b)")
    accent_choice = input("└─ Choose (default: 1): ").strip() or "1"

    if accent_choice.lower() == "c":
        custom = input("   Enter hex colour: ").strip()
        accent = custom if custom.startswith("#") else f"#{custom}"
    else:
        accent = ACCENT_PRESETS.get(accent_choice, ACCENT_PRESETS["1"])[0]

    return theme, accent

# ── DATA CLEANING ─────────────────────────────────────────────────────────────

def clean_cv_data(cv_data: dict) -> dict:
    """
    Sanitise common extraction issues before rendering.
    - Removes empty objects from arrays
    - Strips leading/trailing whitespace from all string fields
    """

    def clean_str(val):
        return val.strip() if isinstance(val, str) else val

    def clean_dict(d):
        return {k: clean_str(v) if isinstance(v, str) else v for k, v in d.items()}

    def is_empty_object(obj: dict) -> bool:
        """Returns True if all string values in the dict are empty."""
        return all(v == "" or v == [] for v in obj.values())

    # Clean personal fields
    cv_data["personal"] = clean_dict(cv_data.get("personal", {}))

    # Clean and filter list sections
    for section in ["experience", "education", "projects", "certifications", "languages"]:
        items = cv_data.get(section, [])
        cleaned = [clean_dict(item) for item in items if isinstance(item, dict)]
        cv_data[section] = [item for item in cleaned if not is_empty_object(item)]

    # Clean skills — remove empty strings
    cv_data["skills"] = [s.strip() for s in cv_data.get("skills", []) if s and s.strip()]

    return cv_data

# ── HTML RENDERING ────────────────────────────────────────────────────────────

def generate_html(cv_data: dict, theme: str, accent: str) -> str:
    """Render the Jinja2 template with CV data and theme settings."""

    # Clean data before rendering
    cv_data = clean_cv_data(cv_data)

    # Set up Jinja2 environment pointing at the template folder
    template_dir = Path(__file__).parent.parent / "template"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"]),
    )

    template = env.get_template("portfolio.html.jinja2")

    html = template.render(
        personal=cv_data.get("personal", {}),
        experience=cv_data.get("experience", []),
        education=cv_data.get("education", []),
        skills=cv_data.get("skills", []),
        projects=cv_data.get("projects", []),
        certifications=cv_data.get("certifications", []),
        languages=cv_data.get("languages", []),
        theme=theme,
        accent=accent,
    )

    return html

# ── FILE OUTPUT ───────────────────────────────────────────────────────────────

def save_site(html: str, name: str) -> Path:
    """
    Save the generated site to output/{name}/
    Copies style.css from template/ alongside the index.html.
    Returns the path to the output folder.
    """

    # Sanitise name for use as folder name
    safe_name = "".join(
        c if c.isalnum() or c in "-_" else "_" for c in name.lower()
    ).strip("_")
    if not safe_name:
        safe_name = "portfolio"

    output_dir = Path(__file__).parent.parent / "output" / safe_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write HTML
    html_path = output_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")

    # Copy CSS
    css_src = Path(__file__).parent.parent / "template" / "style.css"
    css_dst = output_dir / "style.css"

    if css_src.exists():
        shutil.copy2(css_src, css_dst)
    else:
        print(f"⚠  Warning: template/style.css not found at {css_src}")

    return output_dir
