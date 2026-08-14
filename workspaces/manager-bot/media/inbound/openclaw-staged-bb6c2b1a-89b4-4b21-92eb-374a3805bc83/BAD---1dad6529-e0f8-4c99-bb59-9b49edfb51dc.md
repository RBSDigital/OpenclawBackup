Create a new folder in your Google Drive called 'Business_Software_Architecture', and under that folder, create 'test_artefacts'.  Using the test_artefacts folder output the following items:

### Test 1: Diagramming & Rendering (Mermaid, PlantUML, Graphviz, Structurizr)

    Please test the diagramming tools to ensure they can write and compile files:
    1. Create a "test.mmd" with a simple Mermaid flowchart, and run `mmdc -i test.mmd -o test_mermaid.png`.
    2. Create a "test.puml" with a simple PlantUML sequence diagram, and run `plantuml test.puml` (which outputs test.png).
    3. Create a "test.dot" with a Graphviz node graph, and run `dot -Tpng test.dot -o test_graphviz.png`.
    4. Create a "test_workspace.dsl" with a Structurizr C4 model workspace, and run `structurizr export -w test_workspace.dsl -f mermaid`.

    Verify that all output files are generated successfully and show me the Mermaid export.

  ### Test 2: API Specification Linter (Spectral)

    Please verify that Spectral is working to lint an API specification:
    1. Create a dummy file named "invalid-api.yaml" containing a broken OpenAPI block (e.g., missing info or paths).
    2. Run `spectral lint invalid-api.yaml` and report the lint errors and warnings found.

  ### Test 3: Document Compilation (Pandoc)

    Please test Pandoc document compilation:
    1. Create a test markdown file "spec.md" with a heading, lists, and bold text.
    2. Compile it to a Word document using `pandoc spec.md -o spec.docx`.
    3. Verify that the "spec.docx" file was created in your workspace.

  ### Test 4: Architecture Governance (ADR-Tools)

    Please test the Architectural Decision Records (ADR) tool:
    1. Create a temporary folder "test-adrs".
    2. Run `adr init test-adrs` to initialize it.
    3. Run `adr new "Use Postgres for persistence"` to create a new decision template.
    4. Run `adr list` and verify it displays the newly created record.

  ### Test 5: Jira CLI (Jira)

    Please check that the Jira CLI works and can print its status:
    1. Run `jira version` and check if it runs.
    2. Run `jira me` or `jira issue list` (if configured) to verify connection, or check if it prompts for configuration.

  ### Test 6: Database Inspection (SchemaCrawler)

    Please check that SchemaCrawler can run its help check:
    1. Run `schemacrawler --version` to verify the launcher path is fully correct.