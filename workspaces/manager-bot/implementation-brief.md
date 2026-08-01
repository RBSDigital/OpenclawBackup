# DataViews Clone Implementation Brief

## Purpose
Build a fast internal prototype of a metadata-driven schema explorer inspired by `dataviews.io`.

The app should render data models in React Flow, let users search and inspect tables/fields, and generate conservative starter joins or query skeletons from selected nodes.

Primary ecosystems:
- Salesforce Marketing Cloud
- Shopify
- Microsoft Fabric

## Product Definition
This is not a generic diagram editor.

It is a curated schema explorer with three jobs:
1. Help people find the right table or field fast.
2. Help people understand relationships without opening external docs.
3. Help people copy a useful starting query or join path with minimal friction.

## MVP Scope
### In scope
- Load metadata from local JSON files
- Render a graph in React Flow
- Search tables, aliases, and fields
- Select one or more tables
- Inspect field metadata in a side panel
- Highlight relationships on hover and selection
- Copy table names, field names, and query snippets
- Generate a starter SQL skeleton from selected tables
- Support separate metadata packs for SFMC, Shopify, and Fabric

### Out of scope
- Live data connections
- Query execution
- Metadata editing
- Authentication
- Multi-tenant sync
- Permissions management
- Heavy analytics or reporting

## Suggested Repo Structure
```txt
src/
  app/
    App.tsx
    layout/
    state/
  components/
    ecosystem-switcher/
    field-inspector/
    graph-canvas/
    metadata-loader/
    query-builder/
    schema-search/
    table-node/
    relationship-edge/
    empty-state/
  data/
    ecosystems/
      sfmc.json
      shopify.json
      fabric.json
  lib/
    metadata/
    graph/
    search/
    query/
    clipboard/
    layout/
  styles/
  types/
    metadata.ts
    graph.ts
    query.ts
```

## Canonical Metadata Schema
Normalize every ecosystem into one internal model.

### Ecosystem
```ts
type EcosystemId = "sfmc" | "shopify" | "fabric";

interface Ecosystem {
  id: EcosystemId;
  label: string;
  accentColor?: string;
  description?: string;
  tables: TableMetadata[];
}
```

### Table
```ts
interface TableMetadata {
  id: string;
  label: string;
  ecosystem: EcosystemId;
  category?: string;
  description?: string;
  aliases?: string[];
  tags?: string[];
  docsUrl?: string;
  examples?: string[];
  fields: FieldMetadata[];
  relationships?: RelationshipMetadata[];
}
```

### Field
```ts
interface FieldMetadata {
  name: string;
  label?: string;
  type?: string;
  description?: string;
  nullable?: boolean;
  required?: boolean;
  primaryKey?: boolean;
  unique?: boolean;
  aliases?: string[];
  examples?: string[];
  foreignKeys?: ForeignKeyMetadata[];
}

interface ForeignKeyMetadata {
  tableId: string;
  field: string;
}
```

### Relationship
```ts
interface RelationshipMetadata {
  from?: string;
  to: string;
  cardinality?: "one-to-one" | "one-to-many" | "many-to-one" | "many-to-many";
  confidence?: "explicit" | "derived" | "heuristic";
  join: JoinClause[];
  notes?: string;
}

interface JoinClause {
  left: string;
  right: string;
}
```

## Metadata File Contract
Each ecosystem should ship as a standalone JSON file so the app can swap packs without code changes.

Example top-level shape:

```json
{
  "ecosystems": [
    {
      "id": "sfmc",
      "label": "Salesforce Marketing Cloud",
      "description": "Curated SFMC system views and relationships",
      "tables": []
    }
  ]
}
```

## Data Normalization Rules
- Preserve the source table name as `id`
- Derive human-friendly labels only when the source lacks them
- Keep aliases, synonyms, and docs links if present
- Prefer explicit relationships over inferred ones
- Mark inferred joins as `confidence: "heuristic"`
- Never silently invent a join key

## UI Layout
### Top Bar
- Global search input
- Ecosystem selector
- View mode switch
- Copy/export actions

### Left Rail
- Ecosystem summary
- Filters
- Table list
- Favorites or pinned tables

### Main Canvas
- React Flow graph
- Table nodes
- Relationship edges
- Hover highlights
- Auto-layout

### Right Panel
- Selected table details
- Field list
- Relationship metadata
- Copyable names
- Suggested joins

## Interaction Model
### Search
- Match against table name, aliases, tags, field names, and field aliases
- Jump focus to the best match
- Highlight all visible matches in the graph

### Selection
- Single-click selects a table
- Multi-select builds a working set for query generation
- Selection should be persistent until cleared

### Hover
- Hovering a node highlights adjacent nodes and edges
- Hovering a field emphasizes related tables and keys
- Hover feedback should be immediate and lightweight

### Copy
- Copy table name
- Copy qualified field name
- Copy starter query
- Copy join snippets

### Query Generation
Start with conservative SQL:
- `SELECT` selected fields or `*`
- `FROM` the primary selected table
- `JOIN` only explicit or highly confident relationships
- Add inline comments when a join is heuristic or ambiguous

If a path is unclear, output a warning instead of forcing a guess.

## React Flow Model
### Node Types
- `tableCompact`
- `tableExpanded`
- `tableGroup`

### Edge Types
- `explicitJoin`
- `derivedJoin`
- `highlightLink`

### Layout Rules
- Compact nodes by default
- Expand the selected table
- Keep related nodes near one another
- Minimize edge crossings
- Prefer deterministic layout so screenshots remain stable

## Ecosystem Packs
### SFMC Pack
Recommended categories:
- tracking
- subscriber
- journey
- automation
- sms
- send logs

Recommended emphasis:
- send/journey relationships
- system view naming conventions
- read-only reference behavior

### Shopify Pack
Recommended categories:
- orders
- order_items
- customers
- products
- variants
- fulfillments
- inventory

Recommended emphasis:
- order-to-line-item relationships
- customer-to-order paths
- practical commerce reporting joins

### Fabric Pack
Recommended categories:
- lakehouse
- warehouse
- semantic_model
- notebook
- pipeline

Recommended emphasis:
- lineage
- view/table relationships
- semantic model connectivity

## Component Contracts
### `MetadataLoader`
Responsibilities:
- Load JSON packs
- Validate the schema
- Normalize ecosystem data
- Surface load errors clearly

Props:
- `sourceUrl` or `sourceData`
- `onLoaded`
- `onError`

### `SchemaSearch`
Responsibilities:
- Query local metadata index
- Rank table and field matches
- Return quick navigation targets

Props:
- `query`
- `items`
- `onSelectResult`

### `GraphCanvas`
Responsibilities:
- Render nodes and edges in React Flow
- Apply layout
- Manage viewport and selection

Props:
- `tables`
- `relationships`
- `selectedIds`
- `hoveredId`

### `TableNode`
Responsibilities:
- Show table name, category, and field count
- Expand/collapse field preview
- Surface copy affordances

Props:
- `table`
- `expanded`
- `selected`
- `highlighted`

### `FieldInspector`
Responsibilities:
- Render full field metadata for the selected table
- Show foreign keys and docs links
- Offer copy actions

Props:
- `table`
- `relatedTables`

### `QueryBuilder`
Responsibilities:
- Build a starter SQL skeleton
- Display warnings for heuristic joins
- Copy generated text

Props:
- `selection`
- `metadata`

### `RelationshipEdge`
Responsibilities:
- Visually encode join confidence
- Distinguish explicit vs inferred edges

Props:
- `data`
- `highlighted`

## State Model
Keep the first version simple and local.

Track:
- active ecosystem
- loaded ecosystem packs
- search query
- selected table IDs
- hovered table or field
- expanded table IDs
- highlighted relationship IDs
- copied status
- current layout
- query draft

## Performance Goals
- Local search should feel instantaneous
- Initial render should stay smooth with a medium-size metadata set
- Layout should be computed once per metadata load, not every interaction
- Large tables should be virtualized or truncated in preview

## Accessibility Goals
- Keyboard focus for search and table navigation
- Clear selected and hovered states
- Sufficient contrast for edge highlighting
- Copy buttons with visible labels, not icon-only ambiguity

## Build Plan
### Phase 1: Data and Skeleton
- Define the schema types
- Add JSON packs
- Build the metadata loader
- Render a basic graph from one ecosystem

### Phase 2: Interaction
- Add search
- Add table selection
- Add field inspector
- Add copy actions

### Phase 3: Query Help
- Add multi-select
- Generate query skeletons
- Add join confidence messaging

### Phase 4: Ecosystem Expansion
- Add SFMC pack
- Add Shopify pack
- Add Fabric pack
- Tune categories and relationship hints

## Acceptance Criteria
The prototype is ready when:
- a metadata JSON pack renders without manual transformation
- tables are searchable by name and field
- the graph updates on selection and hover
- the inspector shows field-level detail
- copy actions work for names and query snippets
- at least one starter query can be generated from a selection
- SFMC, Shopify, and Fabric data can each load through the same contract

## Implementation Principles
- Be conservative with inference
- Prefer clarity over cleverness
- Treat metadata as the product
- Make the first screen useful within seconds
- Keep the code modular enough to swap in better metadata later

## Deliverable
Ship a usable internal prototype that proves the interaction model quickly, then harden the metadata packs and relationship graph once the core experience feels right.
