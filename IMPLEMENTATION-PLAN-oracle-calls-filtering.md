# Implementation Plan: Oracle Calls Filtering

Status: Completed

Spec: `mapping/SPEC-oracle-calls-filtering.md`

Task list: `mapping/TASKS-oracle-calls-filtering.md`

Tracker: Tidak ada; task list dikelola sebagai Markdown di folder `mapping/`.

## Overview

Plan ini memperbaiki ekstraksi Oracle `Calls` pada analyzer dengan dua filter
semantik: old-style outer join operand `ALIAS.COLUMN(+)` dan Oracle built-in
function/package. Function serta procedure Oracle custom tetap dipertahankan.

## Architecture decisions

1. **Filter pada boundary candidate function.** Kandidat dibersihkan sebelum
   `DbUsage.add_call()` agar filter berlaku konsisten pada SQL literal dan tidak
   mengubah klasifikasi table/read/write.
2. **Outer join memakai helper struktural.** Pola `(+)` dideteksi sebagai suffix
   operand kolom, bukan melalui daftar nama function.
3. **Built-in memakai registry terpusat.** Nama dinormalisasi case-insensitive;
   registry mencakup nama built-in dan package/prefix bawaan Oracle.
4. **Unknown tetap custom.** Function yang tidak cocok dengan outer join atau
   registry built-in tetap masuk `Calls`, sehingga custom function tidak hilang.
5. **Procedure path dipertahankan.** Filtering tidak menghapus procedure custom
   dari literal `OracleCommand` dan tidak mengubah C# call graph.

## Dependency graph

```text
T001 Reproduction tests
  ├── T002 Outer-join candidate filter
  └── T003 Built-in registry/filter
          └── T004 Integrate candidate filtering
                  └── T005 ProposalHargaJualIndomaret output
                          └── T006 Full regression and review
```

## Implementation phases

### Phase 1 — Reproduction and filter contracts

- T001 membuat focused tests yang gagal pada `C.KD_TIPE`, `D.FTKODE`,
  `LISTAGG`, dan `LENGTHB`, tetapi lulus untuk custom calls.
- T002 dan T003 menambahkan helper/filter contract secara terpisah agar sumber
  false positive dan daftar built-in dapat diverifikasi independen.

### Checkpoint: Phase 1

- Reproduction test tersedia dan gagal pada behavior existing.
- Expected custom function/procedure contract terdokumentasi.
- Belum ada perubahan pada controller, data-layer, EDMX, atau output production.

### Phase 2 — Integration

- T004 menghubungkan filter ke `extract_functions_from_sql()` dan jalur procedure
  yang relevan tanpa mengubah `Direct Read`, `Direct Write`, atau CTE.

### Checkpoint: Phase 2

- Unit test outer join dan built-in lulus.
- Custom Oracle function/procedure tetap lulus.
- Existing calls, CTE, schema, dan DML regression lulus.

### Phase 3 — Production verification

- T005 menjalankan analyzer pada `ProposalHargaJualIndomaretController.cs`,
  `IMMD.Data`, dan EDMX production.
- T006 menjalankan focused test, full test discovery, syntax check, dan review
  artifact output.

### Checkpoint: Complete

- `C.KD_TIPE`, `D.FTKODE`, `MCGDATA.LENGTHB`, dan `MCGDATA.LISTAGG` tidak ada di
  section `Calls`.
- Custom Oracle calls tetap ada.
- Semua acceptance criteria spec terpenuhi.

## Verification commands

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
python3 -B -c "from pathlib import Path; compile(Path('mapping/extract_db_usage.py').read_text(encoding='utf-8'), 'mapping/extract_db_usage.py', 'exec')"
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

Tidak menjalankan `dotnet build`, `dotnet run`, atau command build/run .NET.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Built-in registry terlalu sempit | High | Tambahkan daftar representative built-in dan package prefix; unknown tetap custom. |
| Custom function bernama sama dengan built-in | Medium | Ikuti registry Oracle secara eksplisit dan dokumentasikan collision sebagai trade-off. |
| Regex outer join menangkap function valid | High | Batasi filter pada pola identifier/column yang langsung berakhir `(+)`; uji custom function berdampingan. |
| Procedure custom ikut terfilter | Medium | Tambahkan regression test khusus literal `OracleCommand`. |
| Existing output berubah di luar Calls | Medium | Jalankan full regression dan bandingkan section read/write/CTE. |

## Scope boundaries

- In scope: `mapping/extract_db_usage.py`, focused tests, spec/plan/task docs, dan
  generated `ProposalHargaJualIndomaret.md`.
- Out of scope: controller C#, data-layer C#, EDMX, database, root
  `extract_db_usage.py`, dan perubahan format laporan selain isi `Calls`.

## Definition of done

- Semua task T001–T006 selesai.
- Focused test, full regression, syntax check, dan production verification lulus.
- False positive outer join dan built-in hilang dari `Calls`.
- Custom Oracle function/procedure tetap terdeteksi.
- Tidak ada build/run .NET.
