import typer
import re
from pathlib import Path

# Define the function with typer arguments
def process_links(input_md: str = typer.Option("../../README.md", help="Input Markdown file path"),
                  output_md: str = typer.Option("README-linked.md", help="Output Markdown file path"),
                  repo: str = typer.Option("https://github.com/ikko/symb/blob/master/", help="Base repository URL")):
    # Read the input file
    input_path = Path(input_md)
    output_path = Path(output_md)

    # Check if input file exists
    if not input_path.exists():
        print(f"Error: The input file {input_md} does not exist.")
        raise typer.Exit(code=1)

    with open(input_path, "r") as file:
        content = file.read()

    # Prepend the repo URL to all links that do not already have "http"
    transformed_content = re.sub(r'(?<=\]\()(?!http)([^)]+)', lambda m: repo + m.group(1), content)

    # Save the transformed content to the output file
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the output directory exists
    with open(output_path, "w") as file:
        file.write(transformed_content)

    print(f"Processed content saved to {output_md}")

if __name__ == "__main__":
    typer.run(process_links)
