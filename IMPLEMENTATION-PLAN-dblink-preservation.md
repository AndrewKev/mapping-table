# Implementation Plan: Preserve Oracle DBLINK in Mapping

Status: Completed

## Overview

Memperluas extractor SQL agar optional Oracle DBLINK dipertahankan dari token
SQL sampai `PhysicalObject.label`, lalu memverifikasi hasilnya memakai source
nyata `QuotationMerchandisingController.cs` dan
`ApprovalTradingTermController.cs`.

## Architecture Decisions

1. DBLINK disimpan sebagai field terpisah pada `PhysicalObject`, bukan
   digabungkan ke `name`, agar identity/equality untuk table yang sama pada
   DBLINK berbeda tetap deterministik.
2. `_read_qualified_identifier()` mengembalikan optional DBLINK dari syntax
   `object@link` atau `schema.object@link`; seluruh consumer parser meneruskan
   nilai tersebut.
3. `DatabaseCall` tidak diubah. DBLINK hanya berlaku pada physical table/view,
   bukan Oracle function/procedure di section `Calls`.
4. EF/EDMX object tetap tidak diberi DBLINK karena metadata tersebut tidak
   menyatakan DBLINK. Raw SQL pada controller tetap menjadi evidence terpisah
   dan harus mempertahankan DBLINK yang tertulis di source.

## Task List

### Phase 1: Parser and model contract

- T001 — Capture DBLINK in SQL object identifiers.
- T002 — Preserve DBLINK in physical object identity and rendering.

### Checkpoint: Parser contract

- T003 — Add focused parser/model/rendering regression tests.
- T004 — Add real-controller integration samples and acceptance assertions.

### Checkpoint: End-to-end output

- T005 — Regenerate `QuotationMerchandising.md` and verify exact labels.
- T006 — Run full regression and review scope/diff.

## Dependency Graph

```text
T001 → T002 → T003 → T004 → T005 → T006
```

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Existing tuple consumers assume three identifier values | High | Update all parser consumers together and run full tests. |
| DBLINK is lost in CTE physical reads | High | Assert DBLINK on `CteRelation.physical_reads`. |
| Same table on two DBLINKs collapses into one set item | High | Include DBLINK in frozen object identity and test distinct values. |
| `@` appears in non-DBLINK SQL text | Medium | Only accept `@` followed by a valid identifier after a parsed source object. |
| EF entity has no DBLINK source evidence | Medium | Keep EF behavior unchanged and use explicit SQL sample for the reported case. |

## Verification Checkpoints

- After T003: focused unit/model/rendering tests pass.
- After T004: both real controller samples expose expected DBLINK labels.
- After T006: full regression, output acceptance, and whitespace checks pass.

## Scope Boundary

Only `mapping` parser/tests/spec/output artifacts are in scope. No controller,
data-layer, EDMX, dependency, or unrelated generated output changes are
authorized.
