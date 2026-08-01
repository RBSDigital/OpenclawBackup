# Agent Spec: DataViews Clone Prototype

## Mission
Build a fast internal prototype inspired by `dataviews.io`: a visual schema explorer for marketing and commerce data that helps users understand tables, fields, relationships, and queryable join paths at a glance.

The prototype must be driven by metadata JSON and rendered with React Flow. It should feel like a practical schema map, not a generic diagram editor.

Primary target ecosystems:
- Salesforce Marketing Cloud
- Shopify
- Microsoft Fabric

## Product Goal
Help analysts and builders:
- search for tables and fields
- see how entities relate
- inspect field-level metadata
- copy table names, field names, and join snippets quickly
- generate a starter query or join skeleton from the selected graph

This is an internal tool first. Optimize for clarity and speed over polish.

## Reference Product Shape
The source app presents a visual guide to SFMC Data Views with:
- table and field exploration
- relationship awareness across tables
- hover-driven field context
- search across fields
- quick copy/paste of names
- query generation from selected tables

Use that interaction model as the baseline, but do not clone the design literally.

## Non-Goals
- No live connection to customer data
- No query execution
- No editing of source metadata
- No authentication, permissions, or tenant sync in v1
- No complex analytics or charting

## Core UX
### Main Layout
- Left sidebar: ecosystem selector, search, filters, table list, favorites
- Center canvas: React Flow graph with tables as nodes and relationships as edges
- Right inspector: selected table, fields, descriptions, example joins, copy actions
- Top bar: global search, ecosystem toggle, view mode toggle, export/copy buttons

### Primary Interactions
- Search by table name, alias, field name, or synonym
- Click a table to select it
- Hover a field or edge to highlight related tables and matching fields
- Click a field to copy its qualified name
- Click a table to copy its canonical name
- Multi-select tables to generate a starter query/join draft
- Filter by source system, domain, object type, or relationship type
- Show empty-state messaging that explains how to start

### Important Behaviors
- Search should be fuzzy and instant on local metadata
- The canvas should auto-layout cleanly from JSON metadata
- Selected nodes should expand their field list in the inspector
- Related nodes should be visually emphasized on hover and selection
- If a join path is uncertain, show a caution badge instead of guessing

## Data Model
### Input Format
The app consumes one or more metadata JSON files.

Standardize each ecosystem into the same internal shape:

```json
{
  "ecosystems": [
    {
      "id": "sfmc",
      "label": "Salesforce Marketing Cloud",
      "tables": [
        {
          "id": "_Sent",
          "label": "_Sent",
          "category": "tracking",
          "description": "Email send tracking",
          "tags": ["email", "tracking", "sfmc"],
          "fields": [
            {
              "name": "JobID",
              "type": "Number",
              "required": false,
              "description": "Send job identifier",
              "primaryKey": false,
              "foreignKeys": [
                { "tableId": "_Job", "field": "JobID" }
              ]
            }
          ],
          "relationships": [
            {
              "to": "_Job",
              "type": "many-to-one",
              "join": [
                { "left": "JobID", "right": "JobID" }
              ],
              "confidence": "explicit"
            }
          ]
        }
      ]
    }
  ]
}
```

### Canonical Metadata Fields
Every table should support:
- `id`
- `label`
- `ecosystem`
- `category`
- `description`
- `tags`
- `aliases`
- `fields[]`
- `relationships[]`
- `docsUrl` if available
- `examples[]` if available

Every field should support:
- `name`
- `type`
- `description`
- `nullable`
- `primaryKey`
- `unique`
- `foreignKeys[]`
- `aliases[]`
- `examples[]`

Every relationship should support:
- `from`
- `to`
- `join[]`
- `cardinality`
- `confidence`
- `notes`

## Ecosystem-Specific Guidance
### SFMC
Model the familiar system views and related objects users actually query:
- tracking views
- subscriber-related views
- journey and automation views
- send-log style structures

Treat system data views as read-only reference objects. Surface notes about retention and query context where relevant.

### Shopify
Model store analytics and commerce objects:
- orders
- order line items
- customers
- products
- variants
- fulfillment and inventory objects
- discounts and transactions if the metadata includes them

Show practical relationships, especially order-to-line-item and customer-to-order paths.

### Fabric
Model lakehouse, warehouse, and semantic-layer objects:
- tables
- views
- notebooks or pipelines if represented in metadata
- semantic model entities if available

Prefer a clean relationship graph and make lineage obvious when metadata includes it.

## Graph Rules
- Use React Flow nodes for tables or objects
- Use edges for explicit relationships only
- Use grouped subgraphs or visual sections for ecosystem domains
- Auto-layout should avoid edge crossings where possible
- Large tables should collapse to a compact node until expanded
- Field lists should truncate with a “show more” affordance

## Query Helper
Provide a lightweight query assistant that can:
- list selected tables
- suggest likely join order
- output a starter `SELECT ... FROM ... JOIN ...` skeleton
- copy the result to clipboard

Do not promise perfect SQL generation. Keep join inference conservative and explain uncertainty.

## Visual Design
- Make the app feel technical and polished
- Use a restrained palette with one strong accent color per ecosystem
- Distinguish ecosystems by color, but keep the graph readable in monochrome
- Use clear typography and compact density
- Highlight search matches and relationship paths with strong contrast

## Component Breakdown
- `MetadataLoader`
- `EcosystemSwitcher`
- `SchemaSearch`
- `GraphCanvas`
- `TableNode`
- `RelationshipEdge`
- `FieldInspector`
- `QueryBuilder`
- `CopyActions`
- `EmptyState`

## State Management
Keep state local unless it becomes painful.

Track:
- active ecosystem
- loaded metadata
- search query
- selected tables
- hovered field
- highlighted paths
- expanded nodes
- copied state
- graph layout state

## Acceptance Criteria
The prototype is done when:
- a JSON file can be loaded and rendered as a graph
- users can search tables and fields
- users can inspect a table and see its fields
- users can hover a field and see related tables highlighted
- users can multi-select tables and copy a starter query
- SFMC, Shopify, and Fabric metadata can each be loaded without code changes
- the UI is usable on a laptop without horizontal chaos

## Implementation Notes
- Use React Flow for graph rendering
- Use a local metadata JSON source as the only data dependency for v1
- Add a thin adapter layer so each ecosystem can ship its own JSON file
- Prefer deterministic layout over fancy animation
- Cache parsed metadata in memory and local storage for fast reloads
- Add keyboard shortcuts for search focus, copy, and node expansion

## Suggested Build Order
1. Define the canonical metadata schema
2. Build the loader and adapter for one ecosystem
3. Render table nodes in React Flow
4. Add search and selection
5. Add field inspector and copy actions
6. Add join path highlighting
7. Add starter query generation
8. Add SFMC, Shopify, and Fabric metadata packs

## Deliverable
Ship a working internal prototype that proves the concept, then iterate on metadata quality and relationship completeness before spending time on visual polish.
