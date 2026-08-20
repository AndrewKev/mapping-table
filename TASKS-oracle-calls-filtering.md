# Task Breakdown: Oracle Calls Filtering

Status: Completed

Plan: `mapping/IMPLEMENTATION-PLAN-oracle-calls-filtering.md`

Spec: `mapping/SPEC-oracle-calls-filtering.md`

Tracker: Tidak ada; checklist ini dikelola sebagai Markdown di folder `mapping/`.

Implementation result: T001–T006 selesai. Focused test, full regression, syntax
check, dan verifikasi production `ProposalHargaJualIndomaret` telah lulus.

## Working rules

- Kerjakan task berurutan sesuai dependency.
- Tulis regression test sebelum mengubah behavior.
- Semua perubahan kode di `mapping/extract_db_usage.py` memakai project marker
  `IPRO Revisi Header Laporan Trading Term`.
- Jangan mengubah controller, data-layer, EDMX, database, atau root
  `extract_db_usage.py`.
- Jangan menjalankan `dotnet build`, `dotnet run`, atau command build/run .NET.

## Phase 1 — Reproduction and filter contracts

### T001 — Tambahkan reproduction tests untuk false positive Calls

**Description:** Buat focused tests untuk SQL yang mengandung old-style outer
join, Oracle built-in, custom function, dan custom procedure. Test harus RED
sebelum filter diimplementasikan.

**Acceptance criteria:**

- [x] `C.KD_TIPE(+)` dan `D.FTKODE(+)` terbukti bukan Calls.
- [x] `LISTAGG` dan `LENGTHB` terbukti bukan Calls.
- [x] Custom function/procedure tetap diharapkan masuk Calls.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering
```

**Dependencies:** None

**Files likely touched:**

- `mapping/tests/test_oracle_calls_filtering.py`

**Estimated scope:** S

### T002 — Implementasikan detector old-style outer join operand

**Description:** Tambahkan helper yang mengenali identifier/column operand yang
langsung diikuti `(+)`, dengan dukungan case-insensitive dan optional whitespace.

**Acceptance criteria:**

- [x] `ALIAS.COLUMN(+)` dan `ALIAS.COLUMN (+)` tidak menjadi candidate function.
- [x] Candidate function custom pada SQL yang sama tidak terfilter.
- [x] Helper tidak mengubah table/read/write extraction.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering.OuterJoinTests
```

**Dependencies:** T001

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_oracle_calls_filtering.py`

**Estimated scope:** S

### T003 — Lengkapi registry Oracle built-in dan package bawaan

**Description:** Perluas registry built-in secara terpusat untuk `LISTAGG`,
`LENGTHB`, function umum, serta namespace/package Oracle bawaan yang disepakati.

**Acceptance criteria:**

- [x] Registry case-insensitive dan mencakup `LISTAGG` serta `LENGTHB`.
- [x] Built-in qualified seperti `SYS.*` dan `DBMS_*.*` tidak dianggap custom.
- [x] Nama yang tidak ada di registry tetap diperlakukan sebagai custom.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering.BuiltinTests
```

**Dependencies:** T001

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_oracle_calls_filtering.py`

**Estimated scope:** S

## Checkpoint: After T001–T003

- [x] Reproduction tests tersedia.
- [x] Outer join detector dan built-in registry memiliki unit coverage.
- [x] Custom function/procedure contract tetap terwakili.
- [x] Belum ada production source di luar `mapping/` yang berubah.

## Phase 2 — Integration

### T004 — Integrasikan filtering ke Oracle Calls extraction

**Description:** Terapkan kedua filter pada candidate function sebelum
`DbUsage.add_call()` dan pastikan procedure path serta custom qualified name tetap
berfungsi.

**Acceptance criteria:**

- [x] SQL function extraction tidak menambahkan outer join operand atau built-in.
- [x] Custom function qualified/unqualified tetap masuk Calls.
- [x] Custom procedure literal tetap masuk Calls.
- [x] C# method, Direct Read/Write, dan CTE behavior tidak berubah.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering.CallIntegrationTests
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
```

**Dependencies:** T002, T003

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_oracle_calls_filtering.py`

**Estimated scope:** M

## Checkpoint: After T004

- [x] Semua focused Call integration tests lulus.
- [x] Existing CTE, schema, SQL object, dan DML regression lulus.
- [x] Perubahan hanya memengaruhi candidate Calls filtering.

## Phase 3 — Production verification

### T005 — Regenerasi dan review ProposalHargaJualIndomaret

**Description:** Jalankan analyzer terhadap controller, `IMMD.Data`, dan EDMX
production lalu review section `Calls` pada artifact output.

**Acceptance criteria:**

- [x] `C.KD_TIPE`, `D.FTKODE`, `MCGDATA.LENGTHB`, dan `MCGDATA.LISTAGG` tidak ada
      di `Calls`.
- [x] Custom Oracle call yang valid tetap tercetak.
- [x] Direct Read, Direct Write, dan CTE tidak berubah secara tidak diharapkan.

**Verification:**

```bash
python3 -B mapping/extract_db_usage.py \
  --controller "IMMD.Web/Areas/Transaction/Controllers/ProposalHargaJualIndomaretController.cs" \
  --data-root "IMMD.Data" \
  --edmx "IMMD.Data/DbModel.edmx" \
  --output "mapping/output/ProposalHargaJualIndomaret.md" \
  --name "ProposalHargaJualIndomaret" \
  --url "/Transaction/ProposalHargaJualIndomaret" \
  --id "ProposalHargaJualIndomaret" \
  --strict
```

**Dependencies:** T004

**Files likely touched:**

- `mapping/output/ProposalHargaJualIndomaret.md`

**Estimated scope:** S

### T006 — Jalankan final regression dan syntax review

**Description:** Jalankan focused test, full discovery, syntax check, dan
acceptance assertion terhadap artifact production.

**Acceptance criteria:**

- [x] Focused dan full test suite lulus.
- [x] Syntax check `mapping/extract_db_usage.py` lulus.
- [x] Acceptance assertions output lulus.
- [x] Tidak ada build/run .NET.

**Verification:**

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
python3 -B -c "from pathlib import Path; compile(Path('mapping/extract_db_usage.py').read_text(encoding='utf-8'), 'mapping/extract_db_usage.py', 'exec')"
```

**Dependencies:** T005

**Files likely touched:**

- `mapping/tests/test_oracle_calls_filtering.py`
- `mapping/output/ProposalHargaJualIndomaret.md`

**Estimated scope:** S

## Checkpoint: Complete

- [x] T001–T006 selesai.
- [x] Semua acceptance criteria spec terpenuhi.
- [x] Custom Oracle Calls tetap terdeteksi.
- [x] False positive outer join dan built-in hilang.
- [x] Siap untuk review implementasi.
