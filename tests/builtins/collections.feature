Feature: OrderedSymbolSet Functionality

  As a developer using Symbol collections
  I want to manage unique Symbol objects while preserving insertion order
  So that I can maintain predictable data structures

  Scenario: OrderedSymbolSet creation and adding Symbols
    Given an empty OrderedSymbolSet is created
    Then its size should be 0
    When a single Symbol is added to the set
    Then its size should be 1
    And the Symbol should be present in the set
    When multiple Symbols are added to the set
    Then its size should reflect the number of unique Symbols added
    And all added Symbols should be present in the set
    When an existing Symbol is added again to the set
    Then the size of the set should not change
    Given an OrderedSymbolSet is created with initial Symbols
    Then its size should reflect the number of initial Symbols
    And all initial Symbols should be present in the set

  Scenario: OrderedSymbolSet iteration, length, and containment
    Given an OrderedSymbolSet containing Symbols "alpha", "beta", and "gamma" in that order
    When the length of the set is checked
    Then it should be 3
    When the set is iterated over
    Then the Symbols should be yielded in their insertion order
    When checking for containment of an existing Symbol
    Then it should be found in the set
    When checking for containment of a Symbol with the same name (due to interning)
    Then it should also be found in the set
    When checking for containment of a non-existent Symbol
    Then it should not be found in the set
    When a new Symbol "delta" is added to the set
    Then iterating over the set should include "delta" at the end, maintaining insertion order
