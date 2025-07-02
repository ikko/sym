Feature: Symbol Visual Functionality

  As a developer visualizing Symbol graphs
  I want to generate Mermaid diagrams from Symbol structures
  So that I can easily represent and understand complex relationships

  Scenario: Generating a Mermaid diagram for a simple Symbol graph
    Given a simple Symbol graph structure
    When `to_mmd` is called on the root Symbol
    Then a valid Mermaid diagram string representing the graph should be returned
