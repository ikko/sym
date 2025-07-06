import typer
from pathlib import Path

app = typer.Typer(help="Justify .txt files to fixed-width alignment using monospaced logic.")


def justify_line(line: str, width: int) -> str:
    words = line.strip().split()
    if not words:
        return ""
    if len(words) == 1:
        return words[0].ljust(width)

    total_spaces = width - sum(len(word) for word in words)
    space_slots = len(words) - 1
    min_space, extra = divmod(total_spaces, space_slots)

    justified = ""
    for i, word in enumerate(words[:-1]):
        justified += word + " " * (min_space + (1 if i < extra else 0))
    justified += words[-1]
    return justified


def justify_file(file_path: Path, width: int) -> Path:
    justified_lines = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                justified_lines.append(justify_line(line, width))
            else:
                justified_lines.append("")

    output_path = file_path.with_name(f"{file_path.stem}.justified{file_path.suffix}")
    with output_path.open("w", encoding="utf-8") as f:
        for line in justified_lines:
            f.write(line + "\n")

    return output_path


@app.command()
def justify(
    path: Path = typer.Argument(..., help="Path to a .txt file or a directory containing .txt files."),
    width: int = typer.Option(80, "--width", "-w", help="Fixed width for justification."),
):
    """Justifies one or more .txt files with full left-right alignment."""
    if not path.exists():
        typer.echo(f"❌ Path not found: {path}")
        raise typer.Exit(code=1)

    files = [path] if path.is_file() else list(path.glob("*.txt"))

    if not files:
        typer.echo(f"⚠️ No .txt files found in: {path}")
        raise typer.Exit(code=0)

    for file in files:
        output = justify_file(file, width)
        typer.echo(f"✅ Justified: {file.name} → {output.name}")


if __name__ == "__main__":
    app()
