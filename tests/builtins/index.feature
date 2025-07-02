Feature: Symbol Indexing Functionality

  As a developer managing indexed Symbol data
  I want to efficiently insert Symbols and traverse the index
  So that I can perform quick lookups and ordered operations

  Scenario: SymbolIndex insertion
    Given an empty SymbolIndex
    When a Symbol is inserted with a given weight
    Then the Symbol should be present in the index
    And the index structure should remain valid

  Scenario: SymbolIndex traversal
    Given a SymbolIndex with a simple tree structure
    When the index is traversed in-order
    Then the Symbols should be yielded in the correct sorted order
