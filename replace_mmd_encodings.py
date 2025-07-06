import os
from pathlib import Path

def process_mermaid_blocks(root_dir: Path):
    md_files = list(root_dir.rglob("*.md"))

    for file_path in md_files:
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        is_code = False
        processed_lines = []

        for line in lines:
            stripped = line.strip()

            # Start of mermaid block
            if stripped == "```mermaid":
                is_code = True
                processed_lines.append(line)
                continue

            # End of block (only ```
            if stripped == "```":
                is_code = False
                processed_lines.append(line)
                continue

            # Line ends with ``` -> split it
            if is_code and line.rstrip().endswith("```") and line.rstrip() != "```":
                content = line.rstrip()[:-3].rstrip()
                # Replace before separating
                content = content.replace("#40", "#40;").replace("#41", "#41;")
                processed_lines.append(content + "\n")
                processed_lines.append("```\n")
                is_code = False
                continue

            # Inside mermaid block: perform replacement
            if is_code:
                line = line.replace("#40", "#40;").replace("#41", "#41;")

            processed_lines.append(line)

        # Write back to file
        with file_path.open("w", encoding="utf-8") as f:
            f.writelines(processed_lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fix #40/#41 in Mermaid code blocks inside Markdown files.")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Directory to scan recursively for .md files.")
    args = parser.parse_args()

    root_path = Path(args.path)
    if not root_path.exists() or not root_path.is_dir():
        raise ValueError(f"Invalid path: {root_path}")

    process_mermaid_blocks(root_path)
