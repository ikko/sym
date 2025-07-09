Feature: Symbol Creation and Core Properties

  As a developer using the Symbol library
  I want to reliably create and manage Symbol instances
  So that I can build consistent symbic representations

  Scenario: Symbol creation and interning
    Given a symb name "test_symb"
    When a Symbol is created with "test_symb"
    Then an instance of Symbol is returned
    And the symb's name is "test_symb"
    When another Symbol is created with the same name "test_symb"
    Then the same Symbol instance is returned (interning)
    When a Symbol is created with a case-sensitive different name "Test_Symbol"
    Then a new Symbol instance is returned
    And the new symb's name is "Test_Symbol"
    When Symbols are created with names like "123", "symb-with_dashes", and "another symb"
    Then they should retain their exact names

  Scenario: Symbol equality and hashing
    Given two Symbols with the same name "apple"
    And one Symbol with a different name "banana"
    When the two Symbols with the same name are compared for equality
    Then they should be equal
    When a Symbol with a different name is compared for equality
    Then they should not be equal
    When the hash of the two Symbols with the same name is calculated
    Then their hashes should be equal
    When the hash of a Symbol with a different name is calculated
    Then its hash should not be equal to the others
    When a Symbol is compared with non-Symbol types (e.g., string, integer)
    Then they should not be equal

  Scenario: Symbol string representation
    Given a Symbol named "test_repr"
    When the Symbol is converted to a string
    Then the string representation should be "test_repr"
    When the Symbol's repr is called
    Then the repr representation should be "Symbol('test_repr')"

  Scenario: Basic graph operations (append, add, children, parents)
    Given a parent Symbol and two child Symbols (child1, child2)
    And a grandchild Symbol
    When child1 is appended to the parent
    Then child1 is in the parent's children
    And parent is in child1's parents
    And the parent has one child
    When child1 is appended again to the parent
    Then the parent still has one child (no duplicates)
    When child2 is added to the parent
    Then child2 is in the parent's children
    And parent is in child2's parents
    And the parent has two children
    When child2 is added again to the parent
    Then the parent still has two children (no duplicates)
    When grandchild is appended to the parent, and then child1 is appended (chaining)
    Then grandchild is in the parent's children
    And parent is in grandchild's parents
    And the parent has three children (child1, child2, grandchild)
    And the children and parents properties reflect the correct relationships
    When another parent and child are created, and the child is appended to the another parent
    And the another parent is appended to child1
    Then the relationships are correctly established in the graph

  Scenario: SymbolNamespace functionality
    Given a SymbolNamespace instance
    When a Symbol is accessed via attribute (e.g., `s.my_attribute_symb`)
    Then an instance of Symbol is returned
    And its name matches the attribute name
    When a Symbol is accessed via item (e.g., `s["my_item_symb"]`)
    Then an instance of Symbol is returned
    And its name matches the item name
    When Symbols are accessed via both attribute and item with the same name
    Then the same Symbol instance is returned (interning through namespace)
    When an attempt is made to set an attribute or item on the SymbolNamespace
    Then a TypeError should be raised, indicating it is read-only
