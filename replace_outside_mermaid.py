import re
from pathlib import Path

MERMAID_START_RE = re.compile(r"^\s*```mermaid\s*$")
MERMAID_END_RE = re.compile(r"^\s*```\s*$")

def replace_outside_mermaid(text: str) -> str:
    lines = text.splitlines(keepends=True)
    output_lines = []
    inside_mermaid = False

    for line in lines:
        if MERMAID_START_RE.match(line):
            inside_mermaid = True
            output_lines.append(line)
            continue
        if inside_mermaid:
            output_lines.append(line)
            if MERMAID_END_RE.match(line):
                inside_mermaid = False
            continue

        # Replace only outside mermaid blocks
        replaced_line = line.replace("#40;", "(").replace("#41;", ")")
        output_lines.append(replaced_line)

    return ''.join(output_lines)

def process_file(path: Path):
    try:
        original_text = path.read_text(encoding='utf-8')
        updated_text = replace_outside_mermaid(original_text)
        if updated_text != original_text:
            path.write_text(updated_text, encoding='utf-8')
            print(f"✅ Updated: {path}")
        else:
            print(f"⏭️  No changes: {path}")
    except Exception as e:
        print(f"❌ Failed to process {path}: {e}")

def recurse_and_process(root: Path, extensions={".md", ".html", ".txt"}):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in extensions:
            process_file(path)

if __name__ == "__main__":
    import sys
    root_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(f"📁 Scanning directory: {root_dir}")
    recurse_and_process(root_dir)
