# Bioinformatics Terms and Concepts for Graph Representation

This document outlines common terms and concepts from the field of bioinformatics that are suitable for representing as nodes and edges in a graph structure, particularly for generating `Symbol` graphs for testing purposes.

## Nodes (Symbol Names)

These terms can serve as the `name` attribute for `Symbol` objects, representing various biological entities, processes, or abstract concepts.

### Biological Entities
- **Macromolecules:** Protein, Gene, RNA, DNA Fragment, Metabolite, Enzyme, Ligand, Receptor, Antibody, Antigen
- **Cellular/Organismal:** Cell, Species, Organism, Tissue, Cell Type, Virus, Bacteria, Fungi
- **Genetic Variations:** Variant, SNP (Single Nucleotide Polymorphism), Allele
- **Genomic Features:** Transcript, Exon, Intron, Chromosome, Locus, Domain, Motif, Residue

### Biological Processes and Functions
- Transcription, Translation, Replication, Metabolism, Signaling, Regulation, Interaction, Binding, Activation, Inhibition, Expression, Mutation, Evolution, Development, Differentiation, Apoptosis, Proliferation, Transport, Degradation, Synthesis, Catabolism, Anabolism

### Data and Conceptual Elements
- Sequence, Structure, Function, Network, Pathway, Ontology, Annotation, Database, Algorithm, Model, Simulation, Data Set, Experiment, Sample, Phenotype, Genotype, Epigenome, Proteome, Metabolome, Transcriptome, Interactome, Regulome, Disease, Drug

## Edges (Relationships - `how` parameter for `relate` method)

These terms can be used as the `how` parameter in `Symbol.relate(other, how='relationship_type')` to define the nature of the connection between two `Symbol` nodes.

### General Relationships
- `interacts_with`: General interaction between two entities.
- `regulates`: One entity controls the activity or expression of another.
- `activates`: One entity promotes the activity of another.
- `inhibits`: One entity suppresses the activity of another.
- `binds_to`: One entity physically attaches to another.
- `catalyzes`: An enzyme facilitates a biochemical reaction.
- `produces`: One entity results in the creation of another.
- `consumes`: One entity is used up by another process.
- `part_of`: Hierarchical relationship, one entity is a component of another.
- `has_function`: An entity performs a specific biological function.
- `associated_with`: A general association or correlation.
- `involved_in`: An entity plays a role in a process.
- `derived_from`: One entity originates from another.
- `targets`: A drug or regulatory molecule acts upon another entity.
- `expresses`: A gene leads to the production of a protein/RNA.
- `encodes`: A gene contains the genetic information for a protein/RNA.
- `mutates`: One entity undergoes a change in its genetic sequence.
- `phosphorylates`: Adds a phosphate group.
- `dephosphorylates`: Removes a phosphate group.
- `cleaves`: Breaks a bond in a molecule.
- `forms`: Creates a complex or structure.
- `degrades`: Breaks down a molecule.
- `transports`: Moves a substance across a membrane or within a system.
- `located_in`: Physical location.
- `found_in`: Presence in a sample or context.
- `similar_to`: Structural or functional resemblance.
- `homologous_to`: Evolutionary relationship indicating common ancestry.
- `orthologous_to`: Homologous genes in different species that evolved from a common ancestral gene by speciation.
- `paralogous_to`: Homologous genes within the same species that arose by gene duplication.
- `upstream_of`: Positional relationship in a pathway or sequence.
- `downstream_of`: Positional relationship in a pathway or sequence.
- `member_of`: An entity belongs to a set or group.
- `component_of`: An entity is a part of a larger system.
- `causes`: One entity leads to a disease or phenotype.
- `treats`: A drug or therapy addresses a disease.
- `prevents`: A measure stops a disease from occurring.
- `diagnoses`: A biomarker or test identifies a disease.

### Network-Specific Relationships
- **Protein-Protein Interaction (PPI) Networks:**
    - `forms_complex_with`: Proteins combine to form a stable complex.
    - `co_localizes_with`: Proteins are found in the same cellular compartment.
- **Gene Regulatory Networks:**
    - `represses`: A gene or protein reduces the expression of another.
    - `upregulates`: Increases gene expression.
    - `downregulates`: Decreases gene expression.
    - `binds_to_promoter_of`: A transcription factor binds to the promoter region of a gene.
- **Metabolic Pathways:**
    - `participates_in`: A metabolite or enzyme is part of a specific pathway.
- **Phylogenetic Trees:**
    - `shares_common_ancestor_with`: Two species or genes share a common evolutionary origin.
    - `evolved_from`: One entity is a descendant of another.
