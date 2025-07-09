Feature: Symbol Mixinability

  As a developer extending the Symbol class
  I want to dynamically add and manage functionality
  So that I can create flexible and modular symbic systems

  Scenario: Freezing and unfreezing Symbol class state
    Given the Symbol class is initially not frozen
    When the Symbol class is frozen
    Then the Symbol class should be reported as frozen
    And subsequent attempts to freeze the Symbol class should not change its frozen state

  Scenario: Registering and applying a basic mixin
    Given a simple mixin function defined
    When the mixin function is registered to the Symbol class with a new method name
    Then the registration should be successful
    And instances of Symbol should have the new method
    And calling the new method on a Symbol instance should return the expected result

  Scenario: Overwriting an existing mixin
    Given an existing mixin registered to the Symbol class
    And a new mixin function intended to overwrite the existing method
    When the new mixin function is registered with the same method name
    Then the registration should be successful
    And calling the method on a Symbol instance should now return the result from the new mixin
