# Task Breakdown: Controller-Reachable Data-Layer Read/Write Mapping

Status: Completed

Plan: `mapping/IMPLEMENTATION-PLAN-reachable-data-layer.md`

Spec: `mapping/SPEC-reachable-data-layer-read-write.md`

Tracker: Tidak ada; checklist ini adalah task target.

Implementation result: T001–T006 selesai. Focused test, full regression, syntax
check, dan verifikasi production `MarginIGR` telah lulus.

## Working rules

- Kerjakan task berurutan sesuai dependency.
- Tulis regression test sebelum implementasi behavior terkait.
- Setiap task harus meninggalkan source dalam keadaan dapat diuji.
- Semua perubahan kode di `mapping/extract_db_usage.py` memakai project marker
  `IPRO Revisi Header Laporan Trading Term`.
- Jangan mengubah controller, data-layer, EDMX, database, atau root
  `extract_db_usage.py`.
- Jangan menjalankan `dotnet build`, `dotnet run`, atau command build/run .NET.

## Phase 1 — Reproduction and provenance

### T001 — Tambahkan reproduction contract untuk reachable read/write

**Description:** Buat focused test/fixture yang memodelkan controller memanggil
`GetByID()` lalu instance `Updated()`, serta wrapper yang memanggil `inserted()` dan
`Delete()`. Test harus membuktikan bahwa read dan write dipisahkan berdasarkan
body method dan reachability.

**Acceptance criteria:**

- [x] Test memverifikasi `IGR_MARGIN_DC` expected pada `Direct Read` dan
      `Direct Write`.
- [x] Test mencakup method write yang tidak dipanggil dan method bernama `Updated`
      tanpa DML/EF write; keduanya tidak menghasilkan false write.
- [x] Test dapat berjalan tanpa database dan gagal pada behavior instance write
      yang belum diimplementasikan.

**Verification:**

```bash
python3 -B -m unittest \
  mapping.tests.test_reachable_data_layer
```

**Dependencies:** None

**Files likely touched:**

- `mapping/tests/test_reachable_data_layer.py`
- `mapping/fixtures/` (fixture minimal bila diperlukan)

**Estimated scope:** S

### T002 — Bangun receiver/type provenance konservatif

**Description:** Tambahkan representasi internal untuk menghubungkan variable
receiver dengan class data-layer dari explicit declaration, constructor, known
static call return, dan `this` context.

**Acceptance criteria:**

- [x] `var getData = IGR_MARGIN_DC.GetByID(...)` dapat dipetakan ke
      `IGR_MARGIN_DC`.
- [x] `IGR_MARGIN_DC obj = new IGR_MARGIN_DC()` dan `this` pada class data-layer
      dapat dipetakan.
- [x] Receiver yang tidak dapat dibuktikan tidak dipetakan secara spekulatif dan
      menghasilkan diagnostic atau fallback yang terdokumentasi.

**Verification:**

```bash
python3 -B -m unittest \
  mapping.tests.test_reachable_data_layer.ReceiverProvenanceTests
```

**Dependencies:** T001

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_reachable_data_layer.py`

**Estimated scope:** M

## Checkpoint: After T001–T002

- [x] Reproduction test tersedia.
- [x] Receiver yang dikenal dapat dipetakan.
- [x] Static read regression tetap lulus.
- [x] Review hasil sebelum melanjutkan instance call graph.

## Phase 2 — Instance call graph

### T003 — Resolve instance method dan nested call chain

**Description:** Perluas traversal data-layer agar instance call yang receiver-nya
telah dipetakan dapat menemukan body method pada class yang benar, termasuk
wrapper method dan self-call `this.Method()`.

**Acceptance criteria:**

- [x] `getData.Updated()`, `obj.inserted()`, dan `getData.Delete()` masuk queue
      dengan class `IGR_MARGIN_DC` yang benar.
- [x] Call chain `controller -> wrapper -> instance write method` ditelusuri sampai
      body write ditemukan.
- [x] `visited` mencegah loop dan unresolved instance call menghasilkan diagnostic
      tanpa mengarang object.

**Verification:**

```bash
python3 -B -m unittest \
  mapping.tests.test_reachable_data_layer.InstanceCallGraphTests
```

**Dependencies:** T002

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_reachable_data_layer.py`

**Estimated scope:** M

### T004 — Integrasikan body instance ke klasifikasi read/write

**Description:** Pastikan body method yang berhasil di-resolve diproses oleh jalur
klasifikasi yang sama dengan static method, sehingga EF mapping, raw SQL DML, read,
write, schema, dan dual-role object tetap konsisten.

**Acceptance criteria:**

- [x] `UpdateSave<IGR_MARGIN_DC>()`, `InsertSave<IGR_MARGIN_DC>()`, dan
      `Delete<IGR_MARGIN_DC>()` menghasilkan physical `Direct Write` melalui EDMX.
- [x] `CurrentDataContext.CurrentContext.IGR_MARGIN_DC` dan raw SQL `SELECT` pada
      method reachable menghasilkan `Direct Read`.
- [x] Object yang read dan write muncul pada kedua section tanpa duplicate.

**Verification:**

```bash
python3 -B -m unittest \
  mapping.tests.test_reachable_data_layer.ReachableClassificationTests
```

**Dependencies:** T003

**Files likely touched:**

- `mapping/extract_db_usage.py`
- `mapping/tests/test_reachable_data_layer.py`

**Estimated scope:** M

## Checkpoint: After T003–T004

- [x] Instance call graph berhasil menemukan body method.
- [x] Read/write classification sudah memakai physical EDMX mapping.
- [x] C# method tidak masuk `Calls`.
- [x] Review hasil sebelum verifikasi controller real.

## Phase 3 — MarginIGR integration and acceptance

### T005 — Verifikasi MarginIGR dan generated output

**Description:** Jalankan analyzer pada `MarginIGRController` dengan `IMMD.Data`
dan EDMX production sebagai input read-only. Simpan atau review generated output
sesuai keputusan artifact.

**Acceptance criteria:**

- [x] `MCGDATA.IGR_MARGIN_DC` tercetak di `Direct Read` melalui `GetByID()`.
- [x] `MCGDATA.IGR_MARGIN_DC` tercetak di `Direct Write` melalui `Updated()`;
      jalur `inserted()` dan `Delete()` yang dipanggil juga terdeteksi.
- [x] Tidak ada C# method `GetByID`, `Updated`, `inserted`, atau `Delete` di
      `Calls`.

**Verification:**

```bash
python3 -B mapping/extract_db_usage.py \
  --controller "IMMD.Web/Areas/Transaction/Controllers/MarginIGRController.cs" \
  --data-root "IMMD.Data" \
  --edmx "IMMD.Data/DbModel.edmx" \
  --output "mapping/output/MarginIGR.md" \
  --name "MarginIGR" \
  --url "/Transaction/MarginIGR" \
  --id "MarginIGR" \
  --strict
```

**Dependencies:** T004

**Files likely touched:**

- `mapping/tests/test_reachable_data_layer.py`
- `mapping/output/MarginIGR.md`

**Estimated scope:** S

## Phase 4 — Final regression

### T006 — Jalankan regression suite dan final acceptance review

**Description:** Jalankan focused test, seluruh test discovery, syntax check, dan
review output untuk memastikan perubahan instance call tidak merusak behavior
existing.

**Acceptance criteria:**

- [x] Focused test dan seluruh test discovery lulus.
- [x] Syntax check `mapping/extract_db_usage.py` lulus.
- [x] CTE, schema identity, Oracle Calls, dynamic diagnostics, dan false-positive
      protection tetap lulus.

**Verification:**

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
python3 -B -c "from pathlib import Path; compile(Path('mapping/extract_db_usage.py').read_text(encoding='utf-8'), 'mapping/extract_db_usage.py', 'exec')"
```

**Dependencies:** T005

**Files likely touched:**

- `mapping/tests/test_reachable_data_layer.py`
- `mapping/output/MarginIGR.md`

**Estimated scope:** S

## Checkpoint: Complete

- [x] T001–T006 selesai.
- [x] Semua acceptance criteria spec terpenuhi.
- [x] Output `MarginIGR` direview.
- [x] Tidak ada build/run .NET.
- [x] Siap untuk review implementasi.
