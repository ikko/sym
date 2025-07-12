# Implementation Plan: Serialization and Deserialization

This plan outlines the implementation of `from_mmd`, `to_yaml`, `from_yaml`, `to_json`, `from_json`, `to_toml`, and `from_toml` methods for the `Symbol` class, along with their respective testing strategies.

## 1. `from_mmd` Implementation

- **Location:** `symb/core/symb.py` (as a classmethod `Symbol.from_mmd`)
- **Approach:**
    - Use the 'mermaid-parser' python package to parse the Mermaid diagram string.
    - Identify nodes and their names.
    - Identify relationships (edges) and their types (`how`).
    - Create `Symbol` instances for each unique node.
    - Establish relationships between `Symbol` instances based on the parsed edges.
    - Handle different node shapes (though `to_mmd` currently only exports default shape, `from_mmd` should be robust).
    - Return the root `Symbol` of the reconstructed graph.
- **Challenges:** Parsing Mermaid can be complex. Focus on the core `graph LR` and `graph TD` syntax with simple node and edge definitions. Edge cases like subgraphs, styling, and complex node definitions will be out of scope for initial implementation.

## 2. `symb_fixture` for Testing

- **Location:** `tests/conftest.py`
- **Approach:**
    - Create a `pytest` fixture that generates a `Symbol` graph with at least 30 interconnected nodes, all with meaningful names from the field of bio informatics (analyze this for expressions and their meaning, save the result of the analysis to docs/bio.md .
    - Ensure a variety of relationships (parent-child, custom `how` relations) are present, use the bioinfo field to chose expressions from.
    - This fixture will be used across all serialization/deserialization tests.

## 3. `to_yaml` / `from_yaml` Implementation

- **Location:** `symb/core/symb.py`
- **Approach:**
    - **`to_yaml`:**
        - Traverse the `Symbol` graph.
        - Convert `Symbol` objects and their relationships into a Python dictionary/list structure suitable for YAML serialization.
        - Use `PyYAML` to dump the structure to a YAML string.
        - Ensure sequences are always exported in the expanded form (`- item1\n- item2`).
    - **`from_yaml`:**
        - Use `PyYAML` to load the YAML string into a Python dictionary/list structure.
        - Reconstruct the `Symbol` graph from this structure.
        - Handle both expanded and compact sequence formats during import.

## 4. `to_json` / `from_json` Implementation

- **Location:** `symb/core/symb.py`
- **Approach:**
    - **`to_json`:**
        - Leverage `orjson` for efficient serialization.
        - Convert `Symbol` objects and their relationships into a JSON-compatible dictionary/list structure.
    - **`from_json`:**
        - Use `orjson` to load the JSON string.
        - Reconstruct the `Symbol` graph.

## 5. `to_toml` / `from_toml` Implementation

- **Location:** `symb/core/symb.py`
- **Approach:**
    - **`to_toml`:**
        - Convert `Symbol` objects and relationships into a TOML-compatible structure.
        - Use the `toml` library to dump to a TOML string.
    - **`from_toml`:**
        - Use the `toml` library to load the TOML string.
        - Reconstruct the `Symbol` graph.

## 6. Testing Strategy (for all serialization methods)

- **Round-trip test:**
    1.  Generate a `Symbol` graph using `symb_fixture`.
    2.  Serialize the graph to a string (e.g., `temp_test.mmd`, `temp_test.yaml`).
    3.  Restart Python session (conceptually, for isolation).
    4.  Deserialize the string back into a new `Symbol` graph.
    5.  Compare the original graph and the reconstructed graph for structural and relational equality.
    6.  Compare the original serialized string with a re-serialized string from the reconstructed graph for byte-identical content.
- **Focus:** Happy path testing only. Edge cases (malformed input, complex structures not explicitly handled by `to_mmd`'s current output) are out of scope.
