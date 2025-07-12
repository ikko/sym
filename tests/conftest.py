import sys
import os
import pytest
from symb import Symbol
from symb.builtin import apply_builtins
from symb.builtin.avl_tree import AVLTree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

@pytest.fixture(scope='session', autouse=True)
def apply_builtins_for_session():
    apply_builtins()

@pytest.fixture(autouse=True)
def setup_and_teardown(request):

    # Store original _numbered and _pool, and clear them for predictable testing
    original_numbered = Symbol._numbered.traverse_inorder()
    original_pool = dict(Symbol._pool)

    # Clear for predictable testing
    Symbol._numbered = AVLTree() # Reinitialize AVLTree
    Symbol._pool.clear()
    Symbol._auto_counter = 0
    Symbol._read_cursor = 0.0
    Symbol._write_cursor = 0.0

    # If the test function has a specific set of symbs to use, add them
    if hasattr(request, 'param'):
        for sym in request.param:
            # Assuming sym has a ._position attribute for its weight
            Symbol(sym.name, sym.origin) # Re-create symb to ensure it's added to the new AVLTree and pool

    yield

    # Restore original _numbered and _pool after each test
    Symbol._numbered = AVLTree() # Reinitialize AVLTree
    for sym in original_numbered:
        Symbol(sym.name, sym.origin) # Re-create symb to ensure it's added to the new AVLTree and pool
    Symbol._pool.update(original_pool)
    # Reset auto_counter, read_cursor, write_cursor based on original_numbered if needed
    # For now, assuming they will be correctly managed by Symbol.__new__ upon re-creation

@pytest.fixture(scope='function')
def symb_fixture():
    Symbol._pool.clear() # Ensure a clean slate for the fixture

    # Define a set of core bioinformatics terms for nodes
    core_nodes = [
        "Gene", "Protein", "Metabolite", "Pathway", "Disease", "Drug",
        "Cell", "Tissue", "Organism", "SNP", "Transcription Factor",
        "Enzyme", "Reaction", "Chromosome", "Phenotype", "Experiment",
        "Data Set", "Algorithm", "Network", "Interaction", "Regulation",
        "Expression", "Mutation", "Binding", "Activation", "Inhibition",
        "Sequence", "Structure", "Function", "Ontology", "Annotation"
    ]

    # Create Symbol instances for core nodes
    symbols = {name: Symbol(name) for name in core_nodes}

    # Establish parent-child relationships (tree-like structure)
    symbols["Gene"].append(symbols["Protein"])
    symbols["Protein"].append(symbols["Enzyme"])
    symbols["Enzyme"].append(symbols["Reaction"])
    symbols["Reaction"].append(symbols["Metabolite"])
    symbols["Gene"].append(symbols["Transcription Factor"])
    symbols["Transcription Factor"].append(symbols["Regulation"])
    symbols["Regulation"].append(symbols["Expression"])
    symbols["Protein"].append(symbols["Structure"])
    symbols["Structure"].append(symbols["Function"])
    symbols["Gene"].append(symbols["SNP"])
    symbols["SNP"].append(symbols["Disease"])
    symbols["Disease"].append(symbols["Phenotype"])
    symbols["Drug"].append(symbols["Disease"])
    symbols["Cell"].append(symbols["Tissue"])
    symbols["Tissue"].append(symbols["Organism"])
    symbols["Experiment"].append(symbols["Data Set"])
    symbols["Data Set"].append(symbols["Algorithm"])
    symbols["Algorithm"].append(symbols["Network"])
    symbols["Network"].append(symbols["Interaction"])
    symbols["Interaction"].append(symbols["Binding"])
    symbols["Binding"].append(symbols["Activation"])
    symbols["Activation"].append(symbols["Inhibition"])
    symbols["Sequence"].append(symbols["Gene"])
    symbols["Ontology"].append(symbols["Annotation"])

    # Establish custom relationships (graph-like structure)
    symbols["Protein"].relate(symbols["Drug"], how="targets")
    symbols["Gene"].relate(symbols["Disease"], how="associated_with")
    symbols["Metabolite"].relate(symbols["Pathway"], how="participates_in")
    symbols["Pathway"].relate(symbols["Regulation"], how="regulated_by")
    symbols["Protein"].relate(symbols["Protein"], how="interacts_with") # Self-loop for PPI
    symbols["Gene"].relate(symbols["Gene"], how="co_expresses_with")
    symbols["Drug"].relate(symbols["Enzyme"], how="inhibits")
    symbols["Disease"].relate(symbols["Organism"], how="affects")
    symbols["Experiment"].relate(symbols["Phenotype"], how="measures")
    symbols["Algorithm"].relate(symbols["Network"], how="analyzes")
    symbols["Network"].relate(symbols["Interaction"], how="contains")
    symbols["Ontology"].relate(symbols["Gene"], how="annotates")
    symbols["Annotation"].relate(symbols["Protein"], how="describes")
    symbols["Chromosome"].relate(symbols["Gene"], how="contains")
    symbols["SNP"].relate(symbols["Gene"], how="located_in")
    symbols["Cell"].relate(symbols["Protein"], how="expresses")
    symbols["Tissue"].relate(symbols["Cell"], how="composed_of")
    symbols["Organism"].relate(symbols["Tissue"], how="has_tissue")
    symbols["Sequence"].relate(symbols["Structure"], how="determines")
    symbols["Function"].relate(symbols["Protein"], how="performed_by")

    # Add some more complex relationships or cycles
    symbols["Disease"].relate(symbols["Drug"], how="treated_by") # Bidirectional
    symbols["Drug"].relate(symbols["Disease"], how="treats")

    # Ensure at least 30 nodes are interconnected
    # The current setup creates 30 unique symbols and establishes many connections.
    # The exact number of interconnections will depend on the append/relate calls.
    # We can verify the total number of symbols created by checking Symbol._pool
    assert len(Symbol._pool) >= 30, "Fixture did not create at least 30 unique symbols."
    print(f"DEBUG: symb_fixture created {len(Symbol._pool)} symbols in pool.")
    if "Gene" in symbols:
        gene_root = symbols["Gene"]
        reachable_from_gene = gene_root.graph()
        print(f"DEBUG: {len(reachable_from_gene)} symbols reachable from 'Gene'.")

    yield symbols

    # Clean up after the fixture if necessary (though setup_and_teardown handles most of it)
    Symbol._pool.clear()
