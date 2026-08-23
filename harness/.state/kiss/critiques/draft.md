# Critique — draft

## summarize
The draft asserts that "machine sections" divide an app into six testable stations (UI, State, Persistence, Sharing, Agent, Community) and that representations move freely while bindings change only on explicit commit. The closing sentence promises a "quiet interface and an inspectable system," but the summary of *why* quiet + inspectable matters is compressed into one clause.

## structure
The single paragraph overloads four distinct claims: (1) the six-station division, (2) independent testability, (3) the representation/binding split, (4) the quiet+inspectable outcome. Each claim deserves its own beat. Suggested shape: open with the core rule (representation vs. binding), then name the six stations, then close with the payoff. The current order leads with taxonomy and buries the actual thesis at the end.

## keyphrases
- "machine-sections pattern"
- "representations move freely while bindings only change on explicit commit"
- "independently testable"
- "quiet interface and inspectable system"
