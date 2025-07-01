import ast
import os
import argparse
from typing import Any, Optional

# A simple, placeholder LLM function. In a real scenario, this would call an actual model.
def generate_summary(code_snippet: str, name: str) -> str:
    """Generates a one-sentence summary for a piece of code."""
    prompt = f"Based on the following Python code snippet for '{name}', create a concise, 10-13 word summary of its purpose and functionality.\n\nCode:\n{code_snippet}"
    # In a real implementation, you would send this prompt to a large language model.
    # For this script, we'll return a placeholder.
    return "This function or method requires a proper docstring to explain its purpose."

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.inventory = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.inventory.append({
            'type': 'function',
            'name': node.name,
            'signature': self._get_signature(node.args),
            'return': self._get_return_annotation(node.returns),
            'docstring': ast.get_docstring(node) or generate_summary(ast.unparse(node), node.name)
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.inventory.append({
            'type': 'class',
            'name': node.name,
            'docstring': ast.get_docstring(node) or generate_summary(ast.unparse(node), node.name)
        })
        # We need to process the methods inside the class
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.inventory.append({
                    'type': 'method',
                    'class': node.name,
                    'name': item.name,
                    'signature': self._get_signature(item.args),
                    'return': self._get_return_annotation(item.returns),
                    'docstring': ast.get_docstring(item) or generate_summary(ast.unparse(item), item.name)
                })
        self.generic_visit(node)

    def _get_signature(self, args: ast.arguments) -> str:
        params = []
        # Positional and keyword arguments
        for arg in args.args:
            param_str = arg.arg
            if arg.annotation:
                param_str += f": {ast.unparse(arg.annotation)}"
            params.append(param_str)
        return f"({', '.join(params)})"

    def _get_return_annotation(self, returns: Optional[ast.AST]) -> str:
        if returns:
            return f" -> {ast.unparse(returns)}"
        return ""

def analyze_file(file_path: str) -> list[dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    tree = ast.parse(content)
    visitor = CodeVisitor()
    visitor.visit(tree)
    return visitor.inventory

def main():
    parser = argparse.ArgumentParser(description="Generate a code inventory for the Symbol project.")
    parser.add_argument('-l', '--level', type=int, default=2, help='The depth of recursion for directory traversal.')
    args = parser.parse_args()

    start_dir = os.path.join(os.path.dirname(__file__), '..', 'symbol')

    for root, dirs, files in os.walk(start_dir):
        # Prune directories based on level
        depth = root[len(start_dir):].count(os.sep)
        if depth >= args.level:
            dirs[:] = []  # Don't go deeper

        print(f"\n--- Directory: {os.path.relpath(root)} ---")

        for file in sorted(files):
            if file.endswith('.py'):
                print(f"  \n  - File: {file}")
                try:
                    inventory = analyze_file(os.path.join(root, file))
                    for item in inventory:
                        if item['type'] == 'class':
                            print(f"    - CLASS: {item['name']}")
                            print(f"      \"""{item['docstring']}\"""")
                        elif item['type'] == 'function':
                            print(f"    - FUNCTION: {item['name']}{item['signature']}{item['return']}")
                            print(f"      \"""{item['docstring']}\"""")
                        elif item['type'] == 'method':
                            print(f"    - METHOD: {item['class']}.{item['name']}{item['signature']}{item['return']}")
                            print(f"      \"""{item['docstring']}\"""")
                except Exception as e:
                    print(f"    - ERROR analyzing {file}: {repr(e)}")

if __name__ == "__main__":
    main()
