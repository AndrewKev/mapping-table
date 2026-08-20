# Spec: Preserve Oracle DBLINK in Database Usage Mapping

Status: Approved dan diimplementasikan

## Objective

Mempertahankan nama Oracle DBLINK ketika analyzer memetakan physical table/view
dari SQL. Saat source SQL menggunakan `@mpromo`, laporan harus menampilkan
DBLINK dalam uppercase sebagai bagian dari identitas object:

```text
MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO
```

Perubahan ini diperlukan agar laporan mapping tidak kehilangan lokasi database
remote pada controller seperti `QuotationMerchandisingController.cs`.

## Confirmed Intent

- Format physical object: `SCHEMA.TABLE@DBLINK`.
- Nama DBLINK dinormalisasi menjadi uppercase.
- Object tanpa DBLINK tetap menghasilkan format lama: `SCHEMA.TABLE`.
- DBLINK berlaku pada physical table/view di `Direct Read`, `Direct Write`,
  subquery, dan physical reads pada `CTE / Logical Relations`.
- Nama logical CTE tetap hanya nama CTE dan tidak diberi suffix DBLINK.
- Nama Oracle function/procedure pada `Calls` tidak diberi suffix DBLINK.

## Functional Requirements

1. SQL object parser harus mengenali DBLINK pada object tanpa schema maupun
   dengan schema, misalnya `TABLE_NAME@mpromo` dan
   `MCGDATA.TABLE_NAME@mpromo`.
2. DBLINK harus dipertahankan sampai model physical object dan renderer Markdown.
3. Schema, table, dan DBLINK harus dinormalisasi uppercase pada output.
4. Physical object yang sama dengan DBLINK berbeda harus tetap menjadi object
   yang berbeda dari object tanpa DBLINK atau DBLINK lain.
5. Existing object tanpa DBLINK, EF mapping, DML classification, CTE relation,
   dan custom Oracle Calls tidak boleh berubah perilakunya.
6. Output `QuotationMerchandising.md` harus memuat
   `MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO` ketika source SQL menggunakan
   `HO_MEKANISME_NOMINAL_T@mpromo`.

## Real Controller Test Samples

Regression/integration test harus mengambil source dari controller berikut:

- `IMMD.Web/Areas/Transaction/Controllers/QuotationMerchandisingController.cs`
  sebagai sample DBLINK `@mpromo`, terutama query pada sekitar baris 1032 dan
  `HO_MEKANISME_NOMINAL_T@mpromo` pada sekitar baris 1255.
- `IMMD.Web/Areas/Transaction/Controllers/ApprovalTradingTermController.cs`
  sebagai sample DBLINK `@HODB`, terutama query pada sekitar baris 602 dan
  1256.

Test juga boleh memakai sample SQL eksplisit untuk menguji parser secara unit,
tetapi acceptance `HO_MEKANISME_NOMINAL_T@MPROMO` harus dibuktikan dari query
nyata pada controller.

## Acceptance Criteria

- [x] `TABLE_NAME@mpromo` dipetakan sebagai `MCGDATA.TABLE_NAME@MPROMO`.
- [x] `MCGDATA.TABLE_NAME@mpromo` dipetakan sebagai
      `MCGDATA.TABLE_NAME@MPROMO`.
- [x] Table tanpa DBLINK tetap dipetakan sebagai `MCGDATA.TABLE_NAME`.
- [x] DBLINK muncul pada `Direct Read`, `Direct Write`, dan physical reads CTE
      sesuai source SQL.
- [x] DBLINK tidak muncul pada nama logical CTE atau custom function/procedure
      pada `Calls`.
- [x] Dua DBLINK berbeda tidak bergabung menjadi satu physical object.
- [x] Mapping `QuotationMerchandising` memuat
      `MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO`.
- [x] Seluruh regression test lulus.

## Commands

Focused tests:

```bash
python3 -B -m unittest mapping.tests.test_sql_objects mapping.tests.test_rendering mapping.tests.test_dblink_preservation
```

Full regression:

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
```

Generate the affected report:

```bash
python3 -B mapping/extract_db_usage.py \
  --controller "IMMD.Web/Areas/Transaction/Controllers/QuotationMerchandisingController.cs" \
  --data-root "IMMD.Data" \
  --edmx "IMMD.Data/DbModel.edmx" \
  --output "mapping/output/QuotationMerchandising.md" \
  --name "QuotationMerchandising" \
  --url "/Transaction/QuotationMerchandising" \
  --id "QuotationMerchandising" \
  --strict
```

## Project Structure

- `mapping/extract_db_usage.py` — SQL parser, physical object model, and Markdown renderer.
- `mapping/tests/` — unit, integration, and rendering regression tests.
- `mapping/output/QuotationMerchandising.md` — generated acceptance artifact.
- `mapping/SPEC-dblink-preservation.md` — this specification.

## Code Style and Output Contract

Physical object identity must retain the optional DBLINK separately from the
schema and table name so equality and sorting remain deterministic:

```python
PhysicalObject("MCGDATA", "HO_MEKANISME_NOMINAL_T", dblink="MPROMO").label
# "MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO"
```

The renderer must continue emitting one object per Markdown list item. No
additional section or alternate DBLINK notation is introduced.

## Testing Strategy

- Unit tests cover SQL token parsing and normalization for qualified and
  unqualified DBLINK syntax.
- Model/rendering tests cover object identity, output labels, and CTE physical
  reads.
- Integration/CLI verification regenerates `QuotationMerchandising.md` and
  asserts the exact `@MPROMO` output.
- Existing full regression tests guard object classification, CTE handling,
  EF mapping, and custom Oracle Calls.

## Boundaries

- Always: Keep changes inside `mapping`, preserve project code markers in
  modified Python blocks, and run focused plus full regression tests.
- Ask first: Schema/EDMX changes, new dependencies, CLI contract changes, or
  changing the meaning of `Calls`.
- Never: Add DBLINK to C# method names, Oracle function/procedure names, logical
  CTE names, secrets, or unrelated existing output changes.

## Success Criteria

The mapping tool preserves and renders Oracle DBLINK identity without changing
the existing classification behavior for objects that do not use DBLINK.

## Open Questions

None. The output format, uppercase normalization, affected sections, and
out-of-scope `Calls` behavior were explicitly confirmed.
