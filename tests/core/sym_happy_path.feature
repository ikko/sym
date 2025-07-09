Feature: Symbol Happy Path Functionality

  As a developer using the Symbol library
  I want to ensure core Symbol functionalities work as expected
  So that I can build reliable symic systems

  Scenario: Symbol creation and interning
    Given a sym name "test_sym_1"
    When a Symbol is created with "test_sym_1"
    Then an instance of Symbol is returned
    And the sym's name is "test_sym_1"
    When another Symbol is created with the same name "test_sym_1"
    Then the same Symbol instance is returned (interning)
    When a Symbol is created with a different name "test_sym_2"
    Then a new Symbol instance is returned
    And the new sym's name is "test_sym_2"

  Scenario: Symbol equality and hashing
    Given two Symbols with the same name "equal_sym"
    And one Symbol with a different name "another_sym"
    When the two Symbols with the same name are compared for equality
    Then they should be equal
    When a Symbol with a different name is compared for equality
    Then they should not be equal
    When the hash of the two Symbols with the same name is calculated
    Then their hashes should be equal
    When the hash of a Symbol with a different name is calculated
    Then its hash should not be equal to the others

  Scenario: Symbol string representation
    Given a Symbol named "repr_sym"
    When the Symbol is converted to a string
    Then the string representation should be "repr_sym"
    When the Symbol's repr is called
    Then the repr representation should be ":repr_sym"

  Scenario: Basic graph operations (append, add)
    Given a parent Symbol and two child Symbols
    When a child Symbol is appended to the parent
    Then the child is in the parent's children list
    And the parent is in the child's parents list
    When the same child Symbol is added again to the parent
    Then the number of children remains the same (no duplicates)
    When a different child Symbol is added to the parent
    Then the new child is in the parent's children list
    And the parent is in the new child's parents list
    And the parent has two children

  Scenario: SymbolNamespace functionality
    Given a SymbolNamespace instance
    When a Symbol is accessed via attribute (e.g., "my_attribute_sym")
    Then an instance of Symbol is returned
    And the sym's name matches the attribute name
    When a Symbol is accessed via item (e.g., "my_item_sym")
    Then an instance of Symbol is returned
    And the sym's name matches the item name
    When Symbols are accessed via both attribute and item with the same name
    Then the same Symbol instance is returned (interning through namespace)
