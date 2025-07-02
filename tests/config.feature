Feature: Configuration Management

  As a developer using the Symbol library
  I want to manage application configurations
  So that I can customize behavior and persist settings

  Scenario: Default configuration file path determination
    Given the XDG_CONFIG_HOME environment variable is set to a temporary path
    When a Config instance is created without specifying a file path
    Then the Config instance's file path should be the expected default path within XDG_CONFIG_HOME

  Scenario: Loading and saving configuration values
    Given a temporary configuration file path
    And a Config instance initialized with this path
    When a key-value pair is set (e.g., 'test_key': 'test_value')
    And another key-value pair is set using the `set` method (e.g., 'another_key': 123)
    And the configuration is saved
    Then the configuration file should exist
    And the content of the file should match the saved key-value pairs in TOML format
    When a new Config instance is created with the same file path
    Then it should load the previously saved values
    And the keys should be accessible via dictionary-like access and `get` method
    And existing keys should be reported as present
    And non-existent keys should be reported as absent

  Scenario: Setting and getting configuration values
    Given a Config instance
    When a value is set for a key using the `set` method
    Then the value should be retrievable using both `get` method and dictionary-like access
    When the value for the same key is updated using dictionary-like assignment
    Then the updated value should be retrievable using both `get` method and dictionary-like access
    When attempting to get a non-existent key with a default value
    Then the default value should be returned
