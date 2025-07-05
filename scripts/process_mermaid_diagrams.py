import re
import os

def process_mermaid_diagram_content(diagram_text):
    # 1. Replace "[]" with "()"
    processed_text = diagram_text.replace("[]", "()")
    # 2. Replace parentheses with their HTML entity codes
    processed_text = processed_text.replace("(", "#40").replace(")", "#41")
    return processed_text

def process_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    modified_content = content
    changes_made = False

    if file_path.endswith('.md'):
        # Regex to find mermaid blocks: ```mermaid\n...\n```
        # re.DOTALL allows . to match newlines
        def replace_mermaid_block(match):
            nonlocal changes_made
            diagram_content = match.group(2) # Content inside the mermaid block
            processed_diagram_content = process_mermaid_diagram_content(diagram_content)
            if processed_diagram_content != diagram_content:
                changes_made = True
            return f"{match.group(1)}{processed_diagram_content}{match.group(3)}"

        modified_content = re.sub(r'(```mermaid\n)(.*?)(```)', replace_mermaid_block, content, flags=re.DOTALL)

    elif file_path.endswith('.mmd'):
        processed_content = process_mermaid_diagram_content(content)
        if processed_content != content:
            modified_content = processed_content
            changes_made = True
    else:
        print(f"Skipping unsupported file type: {file_path}")
        return

    if changes_made:
        with open(file_path, 'w') as f:
            f.write(modified_content)
        print(f"Processed and updated: {file_path}")
    else:
        print(f"No changes needed for: {file_path}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python process_mermaid_diagrams.py <file1.md> <file2.mmd> ...")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        process_file(file_path)
