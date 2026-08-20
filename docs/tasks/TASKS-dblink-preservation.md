# Tasks: Preserve Oracle DBLINK in Mapping

Status: Completed

Implementation result: T001–T006 selesai. DBLINK dipertahankan pada physical
objects, sample controller nyata lulus, output QuotationMerchandising berhasil
diregenerasi, dan 68 regression tests lulus.

## T001 — Capture DBLINK in SQL object identifiers

**Description:** Extend token-aware source identifier parsing to recognize
`object@dblink` and `schema.object@dblink`, normalize the DBLINK to uppercase,
and pass it through read/write/CTE source extraction.

**Acceptance criteria:**

- [x] Qualified and unqualified DBLINK syntax is parsed without changing
  existing no-DBLINK syntax.
- [x] Invalid/non-identifier text after `@` is not treated as a DBLINK.
- [x] Existing source alias and CTE detection remain functional.

**Verification:** Focused parser tests fail before implementation and pass after.

**Dependencies:** None.

**Files likely touched:** `mapping/extract_db_usage.py`, parser tests.

**Estimated scope:** Small.

## T002 — Preserve DBLINK in physical object identity and rendering

**Description:** Add optional DBLINK identity to `PhysicalObject`, propagate it
through `DbUsage`, CTE physical reads, sorted rendering, and Markdown labels.

**Acceptance criteria:**

- [x] Output label is `SCHEMA.TABLE@DBLINK` when DBLINK exists.
- [x] Output label remains `SCHEMA.TABLE` without DBLINK.
- [x] Same table on no DBLINK and different DBLINKs remains distinct.
- [x] `DatabaseCall` and `Calls` output are unchanged.

**Verification:** Model and rendering tests cover labels, equality, and CTE reads.

**Dependencies:** T001.

**Files likely touched:** `mapping/extract_db_usage.py`, model/rendering tests.

**Estimated scope:** Medium.

## T003 — Add focused regression tests

**Description:** Add tests for SQL parser, physical object identity, CTE reads,
rendering, and uppercase DBLINK normalization.

**Acceptance criteria:**

- [x] Test covers `TABLE@mpromo` and `SCHEMA.TABLE@mpromo`.
- [x] Test covers CTE physical reads with DBLINK.
- [x] Test covers multiple DBLINKs as distinct objects.
- [x] Test covers no DBLINK backward compatibility.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_sql_objects mapping.tests.test_rendering mapping.tests.test_dblink_preservation
```

**Dependencies:** T002.

**Files likely touched:** `mapping/tests/test_dblink_preservation.py`, existing focused tests if needed.

**Estimated scope:** Small.

## T004 — Verify real controller samples

**Description:** Use actual source from QuotationMerchandising and
ApprovalTradingTerm controllers for integration coverage, including the
reported `HO_MEKANISME_NOMINAL_T@mpromo` query.

**Acceptance criteria:**

- [x] Quotation controller sample yields `@MPROMO` objects.
- [x] Approval controller sample yields `@HODB` objects.
- [x] Quotation controller nominal table sample yields
  `MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO`.

**Verification:** Integration test reads the real controller files and asserts
the normalized physical object labels.

**Dependencies:** T003.

**Files likely touched:** `mapping/tests/test_dblink_preservation.py`.

**Estimated scope:** Small.

## T005 — Regenerate affected output

**Description:** Run the mapping CLI for QuotationMerchandising and update the
generated report with DBLINK-qualified physical objects.

**Acceptance criteria:**

- [x] `QuotationMerchandising.md` contains DBLINK-qualified objects where source
  SQL contains DBLINK.
- [x] No function/procedure call receives a DBLINK suffix.

**Verification:** Run the strict CLI command from the spec and assert output
sections.

**Dependencies:** T004.

**Files likely touched:** `mapping/output/QuotationMerchandising.md`.

**Estimated scope:** Small.

## T006 — Full verification and scope review

**Description:** Run all Python regression tests, inspect diff/whitespace, and
confirm unrelated changes remain untouched.

**Acceptance criteria:**

- [x] Full test suite passes.
- [x] Staged/final diff contains only in-scope files when commit is requested.
- [x] `output/UnggahTagPerDc.md` remains excluded.

**Verification:**

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
rtk git -C mapping diff --check
```

**Dependencies:** T005.

**Files likely touched:** None beyond verification artifacts.

**Estimated scope:** Small.

## Checkpoint

- [x] T001–T006 completed.
- [x] Acceptance output verified.
- [x] No .NET build/run performed, per repository instruction.
