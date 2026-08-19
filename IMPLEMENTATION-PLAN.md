# Implementation Plan: Perbaikan extract_db_usage.py

Status: Complete — implementation and verification finished

## Overview

Plan ini memecah SPEC-extract-db-usage-improvement.md menjadi task kecil yang dapat
dikerjakan dan diverifikasi secara terpisah. Semua artifact plan dan task ditempatkan
di folder mapping sesuai scope yang telah disepakati. File root extract_db_usage.py
tidak disentuh; implementation target tetap mapping/extract_db_usage.py.

Tidak ada external tracker. Task list berada di mapping/TASKS.md.

## Architecture decisions

- Physical object disimpan dengan identity schema + name + kind sehingga schema kedua
  tidak hilang.
- CTE disimpan sebagai logical relation terpisah dari physical object. CTE tidak
  otomatis menjadi Direct Read atau Direct Write.
- DML diproses per statement: target adalah write, source/subquery/CTE adalah read.
- EDMX diparse menggunakan xml.etree.ElementTree dan tidak bergantung pada urutan
  attribute atau prefix namespace.
- Source C# dan SQL diproses melalui lexical masking/tokenization sebelum regex atau
  extraction yang lebih spesifik.
- Existing Markdown sections Direct Read, Direct Write, dan Calls dipertahankan;
  CTE / Logical Relations ditambahkan sebagai section terpisah.
- Standard library Python digunakan tanpa dependency baru.
- Dynamic SQL yang tidak dapat dibuktikan secara statis menghasilkan diagnostic,
  bukan data yang dikarang dan bukan silent omission.
- Strict mode hanya gagal untuk input/configuration fatal; unsupported dynamic pattern
  tetap dilaporkan sebagai diagnostic agar mode normal masih berguna.

## Dependency graph

    T001 test harness
      └── T002 canonical identity
            ├── T003 schema-preserving usage/render primitives
            ├── T004 CTE model
            ├── T005 EDMX mapping
            └── T006 C# lexical mask
                  └── T007 class/method ownership
                        └── T008 static call graph
    T006 ── T009 C# SQL literal extraction
              └── T010 SQL lexical scanner
                    └── T011 physical object extraction
                          ├── T012 DML read/write classification
                          ├── T013 CTE dependency graph
                          └── T014 function/procedure extraction
    T007 + T012 ── T015 EF read/write detection
    T008 + T013 + T015 ── T016 analyzer orchestration
    T003 + T004 + T014 + T016 ── T017 Markdown renderer
    T005 + T006 + T016 + T017 ── T018 diagnostics and strict CLI
    T008 + T016 ── T019 performance and dead-code cleanup
    T017 + T018 + all extraction tasks ── T020 integration/golden fixture
    T020 ── T021 final regression review

## Implementation phases

### Phase 1: Foundation and contract

Tasks T001–T004 establish the test harness, canonical physical identity, schema
preservation, and CTE data model.

### Phase 2: Metadata and source indexing

Tasks T005–T008 improve EDMX parsing, C# masking, method ownership, and call graph
resolution.

### Phase 3: SQL and CTE extraction

Tasks T009–T014 implement token-aware SQL extraction, statement-level DML semantics,
CTE dependencies, and qualified calls.

### Phase 4: Integration, reporting, and operational behavior

Tasks T015–T019 connect EF/call graph behavior, render CTE output, expose diagnostics,
and reduce scan cost.

### Phase 5: Regression acceptance

Tasks T020–T021 validate the complete analyzer through fixtures and the full focused
test command.

## Checkpoints

### Checkpoint A: Contract

After T001–T004:

- [ ] unittest discovery runs successfully.
- [ ] Multi-schema identity and CTE model tests pass.
- [ ] No output code has collapsed schema or treated CTE as physical object.

### Checkpoint B: Source and metadata

After T005–T008:

- [ ] EDMX fixtures pass with reordered attributes and namespace prefixes.
- [ ] Comment/string masking and multi-class ownership tests pass.
- [ ] Unresolved static calls are represented as diagnostics.

### Checkpoint C: SQL

After T010–T014:

- [ ] SELECT, INSERT ... SELECT, UPDATE, DELETE, MERGE, WITH, and CTE fixtures pass.
- [ ] DML target/source semantics are correct.
- [ ] Qualified functions/procedures and unresolved dynamic calls are covered.

### Checkpoint D: Integration

After T015–T019:

- [ ] Controller/data-layer integration passes.
- [ ] Markdown sections remain backward-compatible.
- [ ] Missing-input and strict-mode behavior is visible and deterministic.

### Checkpoint E: Complete

After T020–T021:

- [ ] Full focused Python test suite passes.
- [ ] Golden output contains physical reads, writes, calls, and CTE relations.
- [ ] No .NET build/run was required or executed.
- [ ] Human review is complete before modifying the source root or shipping.

## Parallelization

Safe to parallelize after T002:

- T005 EDMX parser and tests.
- T006/T007 source masking and ownership tests.
- Documentation/fixture preparation for T020.

Must remain sequential:

- T002 before any consumer of the canonical model.
- T006 before T010.
- T011 before T012 and T013.
- T008, T013, and T015 before T016.
- T017/T018 before T020.

Because most production behavior is in one Python file, parallel implementation of
tasks that edit mapping/extract_db_usage.py should be coordinated or serialized to
avoid conflicting edits.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Regex replacement creates false positives/negatives | High | Add lexical masking and table-driven regression tests before integration |
| CTE names collide with physical tables | High | Keep separate logical/physical namespaces in T004/T013 |
| DML source tables are classified as write | High | Test target/source pairs in T012 before renderer integration |
| EDMX variations break schema mapping | Medium | Namespace-tolerant XML fixtures in T005 |
| Large generated C# files slow indexing | Medium | T019 excludes generated files by default and measures a representative fixture |
| Dynamic SQL cannot be resolved | Medium | T014/T018 produce explicit diagnostics and define strict-mode boundary |
| Mapping copy diverges from root source | Medium | Keep root untouched and compare baseline manually during T001/T020 |
| Markdown consumers reject new section | Medium | Preserve existing sections and make CTE section additive in T017 |

## Open questions carried from the spec

- Whether mapping/extract_db_usage.py eventually replaces the root script is deferred
  until after implementation and review.
- Dynamic OracleCommand propagation is limited initially to simple statically provable
  assignments; more advanced data flow becomes a future task.
- The CTE section remains separate and is not folded into Direct Read/Direct Write.
