import pytest
from symb import Symbol
import toml

# Assign the methods to Symbol for testing purposes
Symbol.to_toml = Symbol.to_toml
Symbol.from_toml = Symbol.from_toml

def compare_symbol_graphs(original_symbols_map: dict[str, Symbol], reconstructed_symbols_map: dict[str, Symbol]) -> bool:
    print(f"DEBUG: Original graph nodes: {sorted(original_symbols_map.keys())}")
    print(f"DEBUG: Reconstructed graph nodes: {sorted(reconstructed_symbols_map.keys())}")

    if len(original_symbols_map) != len(reconstructed_symbols_map):
        print(f"Node count mismatch: Original {len(original_symbols_map)}, Reconstructed {len(reconstructed_symbols_map)}")
        return False

    if set(original_symbols_map.keys()) != set(reconstructed_symbols_map.keys()):
        print(f"Node name mismatch: Original {set(original_symbols_map.keys())}, Reconstructed {set(reconstructed_symbols_map.keys())}")
        return False

    for name, orig_sym in original_symbols_map.items():
        reconstructed_sym = reconstructed_symbols_map[name]

        # Compare children
        orig_children_names = sorted([s.name for s in orig_sym.children])
        reconstructed_children_names = sorted([s.name for s in reconstructed_sym.children])
        if orig_children_names != reconstructed_children_names:
            print(f"Children mismatch for {name}: Original {orig_children_names}, Reconstructed {reconstructed_children_names}")
            return False

        # Compare relations (excluding inverse relations)
        orig_relations = {how: sorted([s.name for s in related_syms])
                          for how, related_syms in orig_sym.relations.items()
                          if not how.startswith('_inverse_')}
        reconstructed_relations = {how: sorted([s.name for s in related_syms])
                                   for how, related_syms in reconstructed_sym.relations.items()
                                   if not how.startswith('_inverse_')}
        if orig_relations != reconstructed_relations:
            print(f"Relations mismatch for {name}: Original {orig_relations}, Reconstructed {reconstructed_relations}")
            return False
    return True

def test_toml_round_trip(symb_fixture):
    # 1. Generate a Symbol graph using symb_fixture
    original_symbols = symb_fixture # This is already the dictionary of all symbols
    
    # Pick a root for serialization (any symbol will do as to_toml serializes the whole pool)
    original_root_for_serialization = next(iter(original_symbols.values()))

    print(f"DEBUG: Symbol._pool size before serialization: {len(Symbol._pool)}")

    # 2. Serialize the graph to a TOML string
    toml_string = original_root_for_serialization.to_toml()

    # 3. Deserialize the TOML string back into a new Symbol graph
    # Clear the Symbol._pool to ensure a fresh reconstruction
    Symbol._pool.clear()
    print(f"DEBUG: Symbol._pool size after clearing for deserialization: {len(Symbol._pool)}")
    reconstructed_root = Symbol.from_toml(toml_string) # This populates Symbol._pool
    reconstructed_symbols = Symbol._pool # Get the full pool of reconstructed symbols
    print(f"DEBUG: Symbol._pool size after deserialization: {len(Symbol._pool)}")

    # 4. Compare the original graph and the reconstructed graph
    assert compare_symbol_graphs(original_symbols, reconstructed_symbols), "Reconstructed graph does not match original."

    # 5. Compare the original serialized string with a re-serialized string
    # Re-serialize the reconstructed graph (using any symbol from the reconstructed pool)
    re_serialized_toml_string = next(iter(reconstructed_symbols.values())).to_toml()
    
    # Due to potential sorting differences in TOML dump, we load both and compare structures
    original_data = toml.loads(toml_string)
    re_serialized_data = toml.loads(re_serialized_toml_string)

    assert original_data == re_serialized_data, "Re-serialized TOML does not match original TOML structure."
