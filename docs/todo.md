# To-Do List: Enhanced .to_ascii and New .from_ascii

## Phase 1: Plan and Setup
- [x] Create `docs/plan.md`
- [x] Create `docs/todo.md`

## Phase 2: Enhance `.to_ascii`
- [x] Modify `GraphTraversal.__init__` to accept `traverse_mode`, `family_mode`, `graph_mode`.
- [x] Refactor `GraphTraversal.traverse` to implement DFS/BFS for family and general relations.
- [x] Update `GraphTraversal.to_ascii` to format output with relations as explicit `Source --relation_type--> Target` lines.
- [x] Update `Symbol.to_ascii` to pass new parameters.

## Phase 3: Implement `.from_ascii`
- [x] Implement `Symbol.from_ascii` class method based on the new `to_ascii` relation format.
- [x] Implement parsing logic for symbol identification and hierarchy.
- [x] Implement parsing logic for relationship reconstruction.

## Phase 4: Testing
- [ ] Write unit tests for enhanced `.to_ascii`.
- [ ] Write unit tests for new `.from_ascii`.
- [ ] Write roundtrip tests (`to_ascii` -> `from_ascii`).

## Phase 5: Refinement (Future Iterations)
- [ ] Add error handling for malformed ASCII input in `.from_ascii`.
- [ ] Consider performance optimizations for large graphs.
