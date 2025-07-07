import re
from pathlib import Path
import sys

# Regular expressions to identify Mermaid blocks
MERMAID_START_RE = re.compile(r"^\s*```mermaid\s*$")
MERMAID_END_RE = re.compile(r"^\s*```\s*$")

# Color schemes for different diagram types
COLOR_SCHEMES = {
    "validation": {
        "default": "#193370",  # Dark blue
        "process": "#2a4d9e",  # Medium blue
        "decision": "#4169e1",  # Royal blue
        "result": "#6495ed",   # Cornflower blue
        "text_color": "#FFFFFF"  # White text for dark backgrounds
    },
    "feature_flagging": {
        "default": "#0ffbe5",  # Bright teal
        "process": "#0ce6d2",  # Medium teal
        "decision": "#09c2b1",  # Darker teal
        "result": "#07a396",   # Deep teal
        "text_color": "#000000"  # Black text for light backgrounds
    },
    "inventory": {
        "default": "#bfc876",  # Olive green
        "process": "#a8b069",  # Medium olive
        "decision": "#91995c",  # Darker olive
        "result": "#7a824e",   # Deep olive
        "text_color": "#000000"  # Black text for light backgrounds
    }
}

def enhance_mermaid_diagram(diagram_text):
    """Apply consistent styling to a Mermaid diagram."""
    
    # Determine which color scheme to use based on content
    if "validate_mixin_callable" in diagram_text:
        scheme = COLOR_SCHEMES["validation"]
    elif "Dynamic Feature Flagging" in diagram_text:
        scheme = COLOR_SCHEMES["feature_flagging"]
    elif "Inventory Management" in diagram_text:
        scheme = COLOR_SCHEMES["inventory"]
    else:
        scheme = COLOR_SCHEMES["validation"]  # Default
    
    # Process nodes to add styling
    lines = diagram_text.split('\n')
    output_lines = []
    
    for line in lines:
        # Skip existing style lines to avoid duplication
        if line.strip().startswith("style "):
            continue
        
        # Add the line to output
        output_lines.append(line)
        
        # Check if this is a node definition line
        node_match = re.search(r'^\s*([A-Z])\s*\[', line)
        if node_match:
            node_id = node_match.group(1)
            
            # Determine node type and apply appropriate color
            if "{" in line:  # Decision node
                color = scheme["decision"]
            elif "--" in line:  # Process/flow line
                continue  # Skip styling for flow lines
            else:  # Regular node
                color = scheme["default"]
            
            # Add style line
            style_line = f"    style {node_id} fill:{color},stroke:#333,stroke-width:2px,color:{scheme['text_color']};"
            output_lines.append(style_line)
    
    return '\n'.join(output_lines)

def process_file(file_path):
    """Process a markdown file to enhance all Mermaid diagrams."""
    try:
        path = Path(file_path)
        content = path.read_text(encoding='utf-8')
        
        lines = content.split('\n')
        output_lines = []
        
        in_mermaid = False
        mermaid_block = []
        
        for line in lines:
            if not in_mermaid:
                output_lines.append(line)
                if MERMAID_START_RE.match(line):
                    in_mermaid = True
                    mermaid_block = [line]
            else:
                mermaid_block.append(line)
                if MERMAID_END_RE.match(line):
                    in_mermaid = False
                    # Process the collected mermaid block
                    enhanced_mermaid = enhance_mermaid_diagram('\n'.join(mermaid_block[1:-1]))
                    output_lines[-1] = mermaid_block[0]  # Start marker
                    output_lines.append(enhanced_mermaid)
                    output_lines.append(line)  # End marker
                    mermaid_block = []
        
        # Write the modified content back to the file
        modified_content = '\n'.join(output_lines)
        if content != modified_content:
            path.write_text(modified_content, encoding='utf-8')
            print(f"✅ Enhanced Mermaid diagrams in: {file_path}")
        else:
            print(f"⏭️ No changes needed for: {file_path}")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python enhance_mermaid_diagrams.py <markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    process_file(file_path)
