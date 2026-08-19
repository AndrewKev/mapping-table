# Database Usage Mapping Tool

Tool Python untuk menganalisis pemakaian object database dari controller ASP.NET
MVC, data-layer C#, dan metadata EDMX, lalu menghasilkan laporan Markdown.
Analyzer bersifat static analysis: tidak membuka koneksi database dan tidak
menjalankan SQL.

## Prasyarat

- Python 3.8 atau lebih baru.
- Tidak ada dependency Python tambahan; tool menggunakan standard library.
- File controller C#, folder data-layer, dan file EDMX harus dapat dibaca.

File yang dijalankan adalah `mapping/extract_db_usage.py`. File
`extract_db_usage.py` di root repository tidak diganti oleh tool ini.

## Quick start dengan fixture

Jalankan dari root repository:

```bash
python3 -B mapping/extract_db_usage.py \
  --controller "mapping/fixtures/SampleController.cs" \
  --data-root "mapping/fixtures/IMMD.Data" \
  --edmx "mapping/fixtures/DbModel.edmx" \
  --output "/tmp/sample-db-usage.md" \
  --name "Sample" \
  --url "/Sample" \
  --id "sample" \
  --strict
```

Output fixture tersebut memuat physical read, physical write, Oracle function,
Oracle procedure, dan CTE.

## Menjalankan pada source repository

Berikan path controller, data-layer, dan EDMX secara eksplisit. Contoh:

```bash
python3 -B mapping/extract_db_usage.py \
  --controller "Transaction/Controllers/SampleController.cs" \
  --data-root "IMMD.Data" \
  --edmx "IMMD.Data/DbModel.edmx" \
  --output "mapping/output/Sample.md" \
  --name "Sample" \
  --url "/Transaction/Sample" \
  --id "sample" \
  --strict
```

Pastikan folder parent output sudah tersedia. Tool menulis file output, tetapi
tidak membuat folder parent secara otomatis.

## Opsi CLI

| Opsi | Wajib | Keterangan |
|---|---:|---|
| `--controller` | Ya | File controller `.cs` yang menjadi entry point analisis. |
| `--data-root` | Tidak | Root folder data-layer `.cs`. Default mengikuti lokasi script (`mapping/IMMD.Data`). |
| `--edmx` | Tidak | File EDMX untuk mapping entity ke schema/store object. |
| `--output` | Ya | File Markdown tujuan. |
| `--name` | Tidak | Nama laporan pada frontmatter. |
| `--url` | Tidak | URL/rute pada frontmatter. |
| `--id` | Tidak | ID laporan pada frontmatter. |
| `--strict` | Tidak | Mengembalikan exit code non-zero jika input wajib hilang atau EDMX tidak valid. |

`--name`, `--url`, dan `--id` ditulis sebagai scalar YAML yang di-escape agar
newline atau karakter khusus tidak merusak frontmatter.

## Arti section laporan

### Direct Read

Berisi physical table/view yang dibaca secara langsung, termasuk physical source
di dalam SELECT, JOIN, subquery, MERGE `USING`, dan definisi CTE.

### Direct Write

Berisi physical target dari INSERT, UPDATE, DELETE, MERGE, serta entity write EF
seperti `InsertSave<T>`, `UpdateSave<T>`, dan `Delete<T>`.

### Calls

Berisi Oracle function custom yang ditemukan di SQL dan Oracle procedure dari
literal `OracleCommand` atau assignment sederhana ke `CommandText`. Oracle
built-in seperti `NVL`, `COUNT`, dan `ROW_NUMBER` tidak dilaporkan.

Pemanggilan method C# seperti `Repository.Load()` dipakai internal untuk
menelusuri data-layer, tetapi tidak dimasukkan ke section `Calls`.

### CTE / Logical Relations

CTE tetap dilaporkan sebagai logical relation terpisah, bukan sebagai physical
table pada Direct Read/Write. Bila tersedia, section ini mencantumkan:

- `Reads`: physical source yang dibaca definisi CTE;
- `Depends on`: CTE lain yang digunakan;
- `Consumers`: CTE atau query luar yang memakai CTE tersebut.

### Analysis Notes

Berisi diagnostic untuk unresolved method, dynamic SQL/procedure, entity tanpa
mapping EDMX, atau kegagalan input pada mode normal.

## Menjalankan test

Jalankan seluruh regression test:

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
```

Golden output tersedia di `mapping/fixtures/expected.md`. Test tersebut memastikan
section lama tetap ada, schema tidak hilang, dan CTE tidak masuk sebagai physical
object.

## Perilaku diagnostic dan `--strict`

- Mode normal tetap menghasilkan laporan dan menampilkan diagnostic pada stderr
  serta section `Analysis Notes`.
- `--strict` gagal untuk controller, data-root, atau EDMX yang tidak tersedia;
  EDMX yang tidak valid juga dianggap fatal.
- SQL/procedure dinamis tidak ditebak menjadi object. Bagian yang tidak dapat
  dibuktikan secara static dilaporkan sebagai diagnostic.

## Batasan

- Concatenation SQL yang melibatkan nilai dinamis hanya dianalisis sebagian dan
  menghasilkan diagnostic.
- Signature C# yang sangat kompleks atau expression-bodied method di luar pola
  extractor dapat memerlukan penanganan manual.
- Tool tidak melakukan validasi ke database dan tidak menggantikan review hasil
  mapping.
