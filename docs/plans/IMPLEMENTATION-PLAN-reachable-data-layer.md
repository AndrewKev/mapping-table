# Implementation Plan: Controller-Reachable Data-Layer Read/Write Mapping

Status: Completed

Spec: `mapping/docs/specs/SPEC-reachable-data-layer-read-write.md`

Task list: `mapping/docs/tasks/TASKS-reachable-data-layer.md`

Tracker: Tidak ada; task list dikelola sebagai Markdown di folder `mapping/`.

## Overview

Plan ini menerjemahkan spec controller-reachable read/write menjadi perubahan
terukur pada analyzer. Fokus utama adalah membuat instance call seperti
`getData.Updated()`, `obj.inserted()`, dan `getData.Delete()` dapat dihubungkan
ke class data-layer dan body method yang benar, tanpa memasukkan seluruh method
`IMMD.Data` ke dalam laporan.

Hasil akhir harus mempertahankan perilaku read yang sudah berjalan, menambahkan
write yang reachable melalui instance call, dan tetap menjaga `Calls`, CTE,
schema identity, diagnostic, serta output deterministic.

## Architecture decisions

1. **Controller reachability menjadi batas laporan.** Method data-layer hanya
   diproses jika ditemukan melalui controller atau nested call dari method yang
   sudah reachable.
2. **Instance call memakai type provenance konservatif.** Receiver dipetakan dari
   deklarasi type, constructor, return dari known data-layer static call, atau
   `this` pada class yang sedang di-index. Receiver yang tidak terbukti tidak
   boleh menghasilkan write spekulatif.
3. **Klasifikasi read/write tetap berbasis body.** Nama `Updated`, `Inserted`, atau
   `Delete` tidak cukup; body harus memuat raw SQL DML atau pola EF write.
4. **Mesin klasifikasi yang ada digunakan kembali.** Body instance method yang
   berhasil di-resolve masuk ke jalur `add_raw_text`, sehingga raw SQL, EF,
   EDMX, CTE, dan Oracle Calls tetap memiliki satu sumber perilaku.
5. **Physical object dapat memiliki dua peran.** Object yang reachable sebagai
   read dan write dicetak pada kedua section tanpa duplicate di masing-masing
   section.
6. **Production source read-only.** Controller, data-layer, EDMX, dan database
   tidak diubah; perubahan hanya berada di `mapping/`.

## Dependency graph

```text
T001 Reproduction contract/tests
  └── T002 Receiver/type provenance
        └── T003 Instance call resolution and nested traversal
              └── T004 Reachable read/write integration
                    └── T005 MarginIGR integration/golden output
                          └── T006 Full regression and acceptance review
```

## Implementation phases

### Phase 1 — Reproduction and provenance

- T001 membuat test yang membuktikan `IGR_MARGIN_DC` harus read dan write.
- T002 menyiapkan provenance receiver secara konservatif.

### Checkpoint: Phase 1

- Test reproduksi tersedia dan menunjukkan gap sebelum implementasi.
- Static read path yang sudah ada tidak berubah.
- Tidak ada production source di luar `mapping/` yang disentuh.

### Phase 2 — Instance call graph

- T003 menghubungkan instance receiver ke method data-layer dan mengikuti nested
  call chain dengan cycle protection.

### Phase 3 — Classification integration

- T004 memastikan body method yang baru reachable diproses sebagai read/write,
  termasuk EF mapping dan raw SQL.
- T005 memverifikasi output controller MarginIGR secara end-to-end.

### Checkpoint: Phase 3

- `MCGDATA.IGR_MARGIN_DC` muncul pada `Direct Read` dan `Direct Write`.
- Method yang tidak reachable atau hanya bernama write tidak menambah object.
- C# methods tetap tidak masuk `Calls`.

### Phase 4 — Final acceptance

- T006 menjalankan focused test, seluruh regression suite, syntax check, dan CLI
  verification tanpa build/run .NET.

## Verification commands

```bash
python3 -B -m unittest mapping.tests.test_reachable_data_layer
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
python3 -B -c "from pathlib import Path; compile(Path('mapping/extract_db_usage.py').read_text(encoding='utf-8'), 'mapping/extract_db_usage.py', 'exec')"
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

`mapping/output/MarginIGR.md` adalah generated verification output; status
penyimpanannya direview bersama perubahan implementasi.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Receiver `var` tidak memiliki type eksplisit | High | Gunakan return class dari known static call; jika tidak terbukti, diagnostic. |
| Instance method memiliki overload | Medium | Pertahankan class + method key dan pilih body yang dapat di-resolve; jangan silent merge tanpa alasan. |
| `this.Updated()` terlewat di body data-layer | Medium | Simpan owner class pada context traversal dan uji wrapper/self call. |
| Method bernama write tetapi tidak melakukan DML | Medium | Klasifikasi berdasarkan body, bukan nama method. |
| Method reachable memiliki read dan write | Low | Simpan kedua set secara independen; izinkan object tampil di kedua section. |
| Nested call cycle | Medium | Gunakan visited key stabil untuk menghentikan traversal berulang. |
| Output existing berubah karena write baru terdeteksi | Medium | Review golden/output diff dan jalankan seluruh regression suite. |

## Open questions

- `mapping/output/MarginIGR.md` disimpan sebagai artifact hasil verifikasi di
  folder `mapping/`.

## Definition of done

- Semua task T001–T006 memenuhi acceptance criteria.
- Focused dan full regression test lulus.
- `MarginIGR` menampilkan `IGR_MARGIN_DC` di `Direct Read` dan `Direct Write`.
- Tidak ada perubahan pada controller, data-layer, EDMX, file root, atau database.
- Tidak ada build/run .NET yang dijalankan.
