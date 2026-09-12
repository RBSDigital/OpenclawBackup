# BAT example diagrams: compatibility audit

**Audit date:** 11 September 2026  
**Workbook:** `BAT_example_diagrams.drawio`  
**Target editor:** diagrams.net / draw.io

## Result

**PASS: no compatibility defects were identified by the native-file audit.**

- 106 diagram pages detected.
- 106 unique page identifiers.
- Every page contains a valid `mxGraphModel` and root cell structure.
- No duplicate cell identifiers within any page.
- No empty diagram labels.
- Every page contains BAT blue `#0E2B63`, BAT gold `#FAB41E` and the specified `Segoe UI` font token.
- No gradient or shadow styles detected.
- Orthogonal connectors and standard draw.io `mxCell`/`mxGeometry` structures are used throughout.
- The workbook remains editable as native draw.io XML.

## Live UI check

The managed Chromium runtime could not be started in this environment. It still reports `libatk-1.0.so.0` as unavailable, so a live import-and-render check in the diagrams.net UI could not be completed. This is an environment limitation, not a detected workbook defect.

## Rework decision

No diagrams required recreation after the native-file audit. The existing workbook is structurally compatible with diagrams.net and has been retained unchanged. A live visual check should be run when the browser runtime exposes the required library.

## Evidence basis

BAT examples use the official BAT context supplied by:

- https://www.bat.com/who-we-are
- https://www.bat.com/who-we-are/at-a-glance
- https://www.bat.com/strategy-and-purpose
- https://www.bat.com/brands-and-innovation
