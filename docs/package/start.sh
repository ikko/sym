#!/usr/bin/env python3
#
# uses https://github.com/mermaid-js/mermaid-cli
#
# Usage:
# ------
# Installation
# $ npm install -g @mermaid-js/mermaid-cli
#
# Convert Mermaid mmd Diagram File To SVG
# $ mmdc -i input.mmd -o output.svg
# $ mmdc -i input.mmd -o output.png -t dark -b transparent
# $ mmdc -i readme.template.md -o readme.md
# ^^^^^^ using this last one

set -e
set -x

# replace relative links with absolute links pointing to the repository
python update.py --input-md "../../README.md" --output-md "README-linked.md" --repo "https://github.com/ikko/symb/blob/master/"

# replace mermaid diagrams with rendered SVG images
# mmdc -i README-linked.md -o README.md -b transparent   # <- does not look good on dark theme
mmdc -i README-linked.md -o README.md -e png
echo "Generated README.md"
