Feature: Symbol Path Functionality

  As a developer navigating Symbol graphs
  I want to find paths between Symbols and match Symbols based on predicates
  So that I can analyze relationships and extract relevant subgraphs

  Scenario: Finding a path between two Symbols
    Given a Symbol graph with a defined path between a source and a target Symbol
    When `path_to` is called from the source Symbol to the target Symbol
    Then a list of Symbols representing the path should be returned

  Scenario: Matching Symbols based on a predicate
    Given a Symbol graph with various Symbols
    When `match` is called with a predicate that identifies specific Symbols
    And a traversal strategy (e.g., DFS or BFS)
    Then an iterator yielding only the Symbols that match the predicate should be returned in the specified traversal order
