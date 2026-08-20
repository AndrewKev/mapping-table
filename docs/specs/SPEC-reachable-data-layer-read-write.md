# Spec: Controller-Reachable Data-Layer Read/Write Mapping

Status: Approved dan diimplementasikan

Related specification: `SPEC-extract-db-usage-improvement.md`

## Objective

Memperbaiki klasifikasi `Direct Read` dan `Direct Write` berdasarkan operasi
database pada method `IMMD.Data` yang benar-benar dipanggil oleh controller.

Laporan harus membedakan antara method data-layer yang hanya tersedia di source
dan method yang reachable dari controller melalui pemanggilan langsung maupun
call chain. Physical object yang dibaca masuk `Direct Read`, sedangkan physical
object yang menjadi target write masuk `Direct Write`.

Contoh utama adalah `MarginIGRController.ubahMarginDC()`:

```csharp
var getData = IGR_MARGIN_DC.GetByID(dc_igr, dc_idm);
getData.Updated();
```

`GetByID()` membaca `IGR_MARGIN_DC`, sedangkan `Updated()` menjalankan
`UpdateSave<IGR_MARGIN_DC>()`. Hasil yang diharapkan adalah
`MCGDATA.IGR_MARGIN_DC` muncul pada `Direct Read` dan `Direct Write`.

## Problem dan current gap

Analyzer saat ini sudah menelusuri static call seperti
`IGR_MARGIN_DC.GetByID()`, sehingga operasi read dapat ditemukan. Namun pola
instance call seperti `getData.Updated()`, `obj.inserted()`, dan `getData.Delete()`
belum selalu dapat dihubungkan kembali ke class data-layer pemiliknya.

Akibatnya, `UpdateSave<IGR_MARGIN_DC>()`, `InsertSave<IGR_MARGIN_DC>()`, atau
`Delete<IGR_MARGIN_DC>()` dapat terlewat walaupun method tersebut dipanggil oleh
controller.

## Scope

### In scope

- Menentukan method data-layer yang reachable dari controller.
- Menelusuri static call dan instance call dengan type/receiver yang dapat
  dibuktikan secara statis.
- Mengikuti call chain data-layer sampai tidak ada method baru atau sampai loop
  dihentikan oleh `visited` key.
- Mengklasifikasikan raw SQL read dan DML pada method yang reachable.
- Mengklasifikasikan EF read/write pada method yang reachable.
- Memetakan entity EF ke physical schema/object melalui EDMX.
- Menampilkan physical object pada `Direct Read` dan `Direct Write` secara
  deterministic.
- Menambahkan diagnostic untuk instance call atau method body yang tidak dapat
  di-resolve.

### Out of scope

- Mengubah controller, data-layer, EDMX, atau database.
- Menentukan operasi write hanya dari nama method tanpa bukti body yang berisi
  EF write atau DML.
- Memasukkan method C# ke section `Calls`.
- Menjalankan database atau menebak dynamic SQL yang tidak dapat dibuktikan.
- Mengubah semantics CTE yang sudah ditetapkan sebagai logical relation terpisah.

## Assumptions

1. Controller adalah root analisis dan hanya operasi pada method data-layer yang
   reachable dari root yang dilaporkan.
2. Method yang hanya read dan reachable tetap masuk `Direct Read`.
3. Satu physical object boleh muncul sekaligus pada `Direct Read` dan
   `Direct Write` jika execution path yang dianalisis membaca dan menulis object
   tersebut.
4. Nama method seperti `Inserted`, `Updated`, `Deleted`, `inserted`, atau `Delete`
   bukan bukti tunggal adanya write; body method harus diperiksa.
5. Jika receiver instance dapat dipetakan ke class data-layer melalui deklarasi,
   constructor, atau return type method, instance call boleh diikuti.
6. Jika type receiver atau method body tidak dapat dibuktikan, analyzer mencatat
   diagnostic dan tidak menambahkan physical write secara spekulatif.

## Functional Requirements

### 1. Controller reachability

Analyzer harus:

- memulai traversal dari seluruh method/controller text yang menjadi entry point;
- menemukan static call `DataClass.Method()` untuk class yang terindeks di
  `IMMD.Data`;
- menemukan instance call seperti `entity.Updated()` jika type `entity` dapat
  dibuktikan;
- mengikuti pemanggilan nested dari body method yang sudah reachable;
- mencegah traversal berulang menggunakan key class + method + type context yang
  stabil;
- tidak memasukkan method yang hanya ada di `IMMD.Data` tetapi tidak reachable;
- mencatat `UNRESOLVED_METHOD` atau diagnostic khusus instance resolution jika
  method yang dipanggil tidak dapat ditemukan.

### 2. Direct Read

Method data-layer yang reachable harus menghasilkan `Direct Read` jika body-nya
memuat salah satu pola berikut:

- raw SQL `SELECT`, source `MERGE USING`, source subquery, atau source CTE;
- `CurrentDataContext.CurrentContext.<Entity>` yang digunakan untuk query/read;
- method read lain yang pada akhirnya menghasilkan pola read tersebut.

Method read tidak perlu memiliki nama khusus. Nama seperti `GetAll`, `GetByID`,
`Find`, atau nama custom hanya menjadi konteks; klasifikasi harus berasal dari
operasi yang dapat dibuktikan.

### 3. Direct Write

Method data-layer yang reachable harus menghasilkan `Direct Write` jika body-nya
memuat salah satu pola berikut:

- raw SQL target `INSERT INTO`, `UPDATE`, `DELETE FROM`, atau `MERGE INTO`;
- `InsertSave<T>()`, `UpdateSave<T>()`, atau `Delete<T>()`;
- pola EF `AddObject`, `Add`, `Remove`, atau operasi setara yang sudah didukung
  analyzer;
- nested method call yang pada akhirnya memuat salah satu pola write tersebut.

Contoh yang wajib didukung:

```text
controller.ubahMarginDC()
  -> IGR_MARGIN_DC.GetByID()
  -> getData.Updated()
  -> UpdateSave<IGR_MARGIN_DC>()
  -> Direct Write: MCGDATA.IGR_MARGIN_DC
```

Pemanggilan `Updated()` harus di-resolve berdasarkan type receiver, bukan dengan
menebak bahwa semua method bernama `Updated` pasti menulis database.

### 4. Mixed read/write behavior

Jika satu controller execution path memanggil read dan write pada physical object
yang sama, object tersebut harus dicetak pada kedua section:

```markdown
# Direct Read
- MCGDATA.IGR_MARGIN_DC

# Direct Write
- MCGDATA.IGR_MARGIN_DC
```

Duplicate entry dalam satu section tidak boleh muncul.

### 5. Calls and CTE compatibility

- C# method seperti `GetByID()` atau `Updated()` tidak boleh masuk `Calls`.
- `Calls` tetap khusus untuk Oracle custom function dan procedure yang dapat
  dibuktikan secara statis.
- CTE tetap dicetak pada `CTE / Logical Relations` sebagai logical relation.
- Physical source di dalam CTE tetap masuk `Direct Read` sesuai spec utama.

### 6. EDMX mapping

Jika EF entity berbeda dari physical store object, analyzer harus memakai mapping
EDMX untuk menentukan schema dan nama physical object. Jika mapping tidak tersedia,
analyzer menambahkan diagnostic dan tidak menyembunyikan kegagalan tersebut.

## MarginIGR acceptance scenario

Dengan input:

- Controller: `IMMD.Web/Areas/Transaction/Controllers/MarginIGRController.cs`
- Data root: `IMMD.Data`
- EDMX: `IMMD.Data/DbModel.edmx`

Analyzer harus menghasilkan minimal:

- `IGR_MARGIN_DC.GetByID()` sebagai physical read `MCGDATA.IGR_MARGIN_DC`;
- `getData.Updated()` sebagai physical write `MCGDATA.IGR_MARGIN_DC`;
- `obj.inserted()` sebagai physical write jika method tersebut dipanggil oleh
  controller;
- `getData.Delete()` sebagai physical write jika method tersebut dipanggil oleh
  controller;
- tidak memasukkan method C# tersebut ke `Calls`.

## Commands

Focused test yang akan ditambahkan:

```bash
python3 -B -m unittest \
  mapping.tests.test_reachable_data_layer
```

Regression suite:

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
```

CLI verification:

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

Verifikasi tidak menjalankan `dotnet build`, `dotnet run`, atau command build/run
aplikasi .NET.

## Project Structure

```text
mapping/
├── extract_db_usage.py                       # implementation target
├── tests/test_reachable_data_layer.py        # focused regression/integration tests
├── output/MarginIGR.md                        # generated verification output
└── SPEC-reachable-data-layer-read-write.md   # this specification
```

Source production `IMMD.Web`, `IMMD.Data`, dan EDMX dibaca sebagai input; file-file
tersebut tidak diubah oleh implementasi tool.

## Code Style

- Pertahankan pemisahan physical object, logical CTE, dan C# call graph.
- Jangan membuat daftar pengecualian berdasarkan nama controller atau table.
- Gunakan canonical `(class, method, receiver type)` untuk traversal dan deduplicate.
- Resolver yang tidak yakin harus menghasilkan diagnostic, bukan false positive.
- Perubahan kode lebih dari satu baris harus memakai project marker:

```text
# project : IPRO Revisi Header Laporan Trading Term
[code]
# end project : IPRO Revisi Header Laporan Trading Term
```

## Testing Strategy

### Unit tests

- static data-layer read yang reachable masuk `Direct Read`;
- direct instance `Updated()` yang menjalankan `UpdateSave<T>` masuk `Direct Write`;
- `inserted()` yang menjalankan `InsertSave<T>` masuk `Direct Write`;
- `Delete()` yang menjalankan `Delete<T>` masuk `Direct Write`;
- nested chain `A -> B -> Updated()` tetap terdeteksi;
- method data-layer yang tidak dipanggil controller tidak masuk report;
- method dengan nama `Updated` tetapi tanpa DML/EF write tidak otomatis menjadi write;
- physical object yang read dan write muncul pada kedua section tanpa duplicate;
- unresolved instance receiver menghasilkan diagnostic;
- C# methods tidak masuk `Calls`;
- regression CTE, schema, Oracle function/procedure, dan diagnostic tetap lulus.

### Integration/golden test

Fixture minimal harus memodelkan controller yang:

1. membaca entity melalui `GetByID()`;
2. memanggil instance `Updated()` secara langsung;
3. memanggil method wrapper yang kemudian memanggil `inserted()` atau `Delete()`;
4. memiliki method write yang tidak pernah dipanggil.

Golden output harus membuktikan bahwa hanya method write yang reachable menghasilkan
`Direct Write`, sementara read yang reachable tetap menghasilkan `Direct Read`.

## Boundaries

### Always

- Hanya proses method data-layer yang reachable dari controller.
- Pertahankan schema EDMX dan physical object identity.
- Pertahankan CTE sebagai logical relation terpisah.
- Jalankan focused test lalu seluruh regression suite.
- Tambahkan diagnostic untuk resolver yang tidak pasti.
- Tambahkan project marker pada perubahan kode.

### Ask first

- Mengubah contract section `Direct Read`, `Direct Write`, `Calls`, atau CTE.
- Mengubah format EDMX atau menambah dependency parser.
- Mengubah controller/data-layer/EDMX production source.
- Mengubah file root `extract_db_usage.py`.

### Never

- Menganggap semua method bernama `Updated`, `Inserted`, atau `Delete` sebagai
  write tanpa memeriksa body dan reachability.
- Memasukkan seluruh method `IMMD.Data` hanya karena file/class terindeks.
- Memasukkan C# method ke `Calls`.
- Menjalankan SQL atau koneksi database.
- Menjalankan build/run aplikasi .NET sesuai aturan repository.

## Success Criteria

Implementasi dianggap memenuhi spec jika:

1. `MarginIGR` menampilkan `MCGDATA.IGR_MARGIN_DC` pada `Direct Read` berdasarkan
   `GetByID()`.
2. `MarginIGR` menampilkan `MCGDATA.IGR_MARGIN_DC` pada `Direct Write` berdasarkan
   `getData.Updated()` dan `UpdateSave<IGR_MARGIN_DC>()`.
3. `inserted()` dan `Delete()` yang reachable dari controller diklasifikasikan
   sebagai write.
4. Pemanggilan melalui satu atau lebih wrapper method tetap ditelusuri.
5. Method write yang tidak reachable tidak memengaruhi laporan.
6. Method read yang reachable tetap masuk `Direct Read`.
7. Object yang memiliki read dan write muncul pada kedua section tanpa duplicate.
8. C# method tetap tidak muncul di `Calls`; Oracle function/procedure tetap muncul
   sesuai aturan existing.
9. CTE, schema identity, dynamic diagnostic, dan output deterministic tidak regresi.
10. Focused test dan seluruh regression suite lulus tanpa build/run .NET.

## Open Questions

- Jika type receiver hanya dapat diperkirakan dari flow control yang kompleks,
  apakah diagnostic cukup atau perlu data-flow analysis yang lebih dalam?
- Apakah output `mapping/output/MarginIGR.md` harus disimpan sebagai generated
  artifact setelah implementasi?
