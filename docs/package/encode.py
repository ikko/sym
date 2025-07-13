import os
import base64
import re

def encode_image_to_base64(image_path):
    """Encodes an image file to base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def replace_mermaid_with_image(md_file_path, image_paths):
    """Replaces Mermaid diagram blocks with base64 encoded images."""
    # Read the markdown file
    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
    
    # Find all mermaid code blocks and replace them with base64 images
    for i, image_path in enumerate(image_paths, start=1):
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)
        
        # Create markdown image format with base64 encoding
        base64_img_tag = f'![Diagram {i}](data:image/png;base64,{base64_image})'
        
        # Replace mermaid block with the base64 image tag
        md_content = re.sub(
            r"```mermaid.*?```",
            base64_img_tag,
            md_content,
            flags=re.DOTALL
        )

    # Write the modified markdown content back to the file
    with open(md_file_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    print(f"Updated {md_file_path} with base64 encoded images.")

if __name__ == "__main__":
    markdown_file = "README.md"  # Your markdown file
    image_files = ["README-1.png", "README-2.png"]  # Image files to be encoded

    replace_mermaid_with_image(markdown_file, image_files)
