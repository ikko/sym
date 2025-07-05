import re
from pathlib import Path

# Matches: fill:lighten(#b388ef, 30%) => captures #b388ef
FILL_LIGHTEN_RE = re.compile(
    r"fill:\s*lighten\s*\(\s*(#[a-fA-F0-9]{6})\s*,\s*\d+%\s*\)"
)

def simplify_fill_lighten(text: str) -> str:
    return FILL_LIGHTEN_RE.sub(r"fill:\1", text)

def process_file(path: Path):
    try:
        original_text = path.read_text(encoding='utf-8')
        updated_text = simplify_fill_lighten(original_text)
        if updated_text != original_text:
            path.write_text(updated_text, encoding='utf-8')
            print(f"🎨 Updated: {path}")
        else:
            print(f"✅ No changes: {path}")
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")

def recurse_and_process(root: Path, extensions={".svg", ".html", ".css", ".md", ".mmd"}):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in extensions:
            process_file(path)

if __name__ == "__main__":
    import sys
    root_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(f"🔍 Scanning for fill:lighten(...) patterns in: {root_dir}")
    recurse_and_process(root_dir)
