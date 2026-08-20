# Spec: Oracle Calls Filtering for SQL Function Extraction

Status: Approved dan diimplementasikan

Related controller: `IMMD.Web/Areas/Transaction/Controllers/ProposalHargaJualIndomaretController.cs`

Related data-layer method: `IMMD.Data/Managed/HGJUAL_IDM_NASIONAL_SQL.cs::Get_BY_SAT_PLU()`

## Objective

Memperbaiki section `Calls` pada hasil mapping agar hanya berisi procedure dan
function Oracle custom yang benar-benar menjadi dependency database.

Saat ini parser masih memasukkan dua jenis token yang bukan custom call:

- `C.KD_TIPE(+)` dan `D.FTKODE(+)`, yang merupakan sintaks old-style outer join;
- Oracle built-in seperti `LISTAGG` dan `LENGTHB`.

Perubahan harus mempertahankan custom function seperti
`MCGDATA.CARI_DESK_PRODUK(...)` dan custom procedure yang dipanggil melalui
`OracleCommand`.

## Confirmed intent

- `ALIAS.COLUMN(+)` bukan function/procedure dan harus diabaikan dari `Calls`.
- Oracle built-in function tidak perlu ditampilkan pada `Calls`.
- Built-in Oracle yang qualified melalui package/namespace bawaan Oracle juga
  diabaikan.
- Function/procedure custom, termasuk qualified custom function, tetap dicatat.
- `Direct Read`, `Direct Write`, CTE, EDMX mapping, dan aturan C# method tidak
  berubah.

## Current evidence

Pada `mapping/output/ProposalHargaJualIndomaret.md`, section `Calls` saat ini
memuat:

```text
- C.KD_TIPE
- D.FTKODE
- MCGDATA.LENGTHB
- MCGDATA.LISTAGG
```

Sumber `C.KD_TIPE(+)` dan `D.FTKODE(+)` berada di SQL pada method
`Get_BY_SAT_PLU()` dalam `HGJUAL_IDM_NASIONAL_SQL.cs`.

## Functional Requirements

### 1. Old-style outer join operands

Extractor function SQL harus mengenali pola berikut sebagai operand kolom,
bukan function call:

```sql
C.KD_TIPE(+)
D.FTKODE (+)
```

Aturannya:

- case-insensitive;
- whitespace antara nama kolom dan `(+)` boleh ada;
- token `schema.table.column(+)` atau bentuk qualified lain yang berakhir pada
  `(+)` tidak boleh ditambahkan ke `Calls`;
- function custom pada SQL yang sama tetap diproses.

### 2. Oracle built-in registry

Analyzer harus memiliki registry built-in Oracle yang terpusat, case-insensitive,
dan mudah diperluas. Registry minimal harus mencakup:

- `LISTAGG`;
- `LENGTHB`;
- function umum yang sudah dikenal analyzer seperti `NVL`, `TO_CHAR`, `TO_DATE`,
  `SUBSTR`, `ROUND`, `TRUNC`, `MAX`, `MIN`, dan `COUNT`;
- package/namespace bawaan Oracle yang diputuskan sebagai built-in, termasuk
  namespace `SYS` dan package bawaan berprefix `DBMS_`.

Nama function yang cocok dengan registry built-in tidak boleh masuk `Calls`, baik
dalam bentuk unqualified maupun qualified.

Nama function/procedure yang tidak cocok dengan registry built-in dianggap custom
dan tetap boleh masuk `Calls`.

### 3. Custom Oracle function dan procedure

Extractor harus tetap mencatat:

- function custom unqualified, misalnya `Get_Nilai_Perubahan(...)`;
- function custom qualified, misalnya `MCGDATA.CARI_DESK_PRODUK(...)`;
- procedure custom yang dipanggil melalui literal `OracleCommand`;
- custom package function/procedure yang bukan package built-in Oracle.

Filtering built-in tidak boleh menghapus custom call hanya karena call tersebut
berada dalam query yang sama dengan `LISTAGG`, `LENGTHB`, atau outer join.

### 4. Reporting compatibility

- `Calls` hanya menerima Oracle custom function/procedure yang lolos filtering.
- C# method seperti `GetByID()` atau `Updated()` tetap tidak masuk `Calls`.
- `Direct Read`, `Direct Write`, CTE, dan diagnostic lain tetap menggunakan jalur
  existing.
- Duplicate call tidak boleh muncul pada output.
- Nama call dinormalisasi dengan aturan existing tanpa mengubah schema custom.

## Acceptance criteria

### Unit behavior

- SQL dengan `C.KD_TIPE(+)` dan `D.FTKODE(+)` menghasilkan zero call untuk kedua
  token tersebut.
- SQL dengan `LISTAGG(...)` dan `LENGTHB(...)` tidak menghasilkan call untuk
  kedua built-in tersebut.
- SQL dengan `SYS.<built-in>` atau `DBMS_<package>.<function>` tidak menghasilkan
  call built-in.
- SQL yang memuat built-in dan custom function sekaligus tetap menghasilkan
  custom function saja.
- Custom procedure literal tetap terdeteksi.

### ProposalHargaJualIndomaret integration

Setelah analyzer dijalankan terhadap controller, data root, dan EDMX production:

- `C.KD_TIPE` tidak ada pada section `Calls`;
- `D.FTKODE` tidak ada pada section `Calls`;
- `MCGDATA.LENGTHB` tidak ada pada section `Calls`;
- `MCGDATA.LISTAGG` tidak ada pada section `Calls`;
- custom call seperti `MCGDATA.CARI_DESK_PRODUK` tetap ada jika dipanggil oleh
  execution path yang dianalisis;
- tidak ada perubahan yang tidak diharapkan pada `Direct Read`, `Direct Write`,
  dan `CTE / Logical Relations`.

## Tech stack

- Python 3 standard library;
- parser SQL/tokenizer yang sudah ada di `mapping/extract_db_usage.py`;
- `unittest` untuk unit dan integration test;
- Oracle SQL sebagai input yang dianalisis;
- tidak ada database connection saat test.

## Commands

Focused test:

```bash
python3 -B -m unittest mapping.tests.test_oracle_calls_filtering
```

Full regression:

```bash
python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'
```

Production verification:

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

Syntax check:

```bash
python3 -B -c "from pathlib import Path; compile(Path('mapping/extract_db_usage.py').read_text(encoding='utf-8'), 'mapping/extract_db_usage.py', 'exec')"
```

Tidak menjalankan `dotnet build`, `dotnet run`, atau command build/run .NET.

## Project structure

```text
mapping/
├── extract_db_usage.py                  # analyzer dan extractor Oracle Calls
├── tests/test_oracle_calls_filtering.py # focused unit/integration tests
└── output/ProposalHargaJualIndomaret.md # generated verification artifact
```

## Code style and implementation guidance

Gunakan registry immutable/set yang dinormalisasi lowercase dan filter sebelum
memanggil `DbUsage.add_call()`:

```python
normalized = normalize_oracle_call_name(name)
if is_old_outer_join_operand(normalized):
    continue
if is_oracle_builtin(normalized):
    continue
usage.add_call(normalized)
```

Aturan implementasi:

- gunakan helper terpisah untuk outer join detection dan built-in detection;
- jangan memakai nama function saja untuk mengubah `Direct Read` atau
  `Direct Write`;
- pertahankan project marker pada blok kode yang berubah;
- test harus membuktikan positive custom call dan negative built-in/outer join.

## Testing strategy

Test harus berada di `mapping/tests/test_oracle_calls_filtering.py` dan mencakup:

1. unit test ekstraksi outer join operand;
2. unit test built-in unqualified dan qualified;
3. unit test custom function yang berdampingan dengan built-in;
4. unit test custom Oracle procedure;
5. integration test `DbUsage` agar hanya custom call masuk ke `usage.calls`;
6. production artifact assertion untuk `ProposalHargaJualIndomaret.md`;
7. full regression untuk CTE, schema identity, SQL object extraction, dan
   behavior existing lain.

## Boundaries

- Always: gunakan registry case-insensitive, pertahankan custom call, deduplicate
  output, jalankan focused dan full test sebelum commit.
- Ask first: perubahan pada definisi custom-vs-built-in yang dapat menghapus call
  existing, perubahan format Markdown, perubahan EDMX/controller/data-layer, atau
  penambahan dependency.
- Never: memasukkan kembali old-style outer join sebagai call, mencatat Oracle
  built-in sebagai custom call, menghapus test yang gagal, atau menjalankan build/
  run .NET.

## Success criteria

- Focused tests untuk outer join, built-in, custom function, dan custom procedure
  lulus.
- Full regression suite lulus tanpa mengubah behavior Direct Read/Write dan CTE.
- Output `ProposalHargaJualIndomaret.md` tidak lagi memuat `C.KD_TIPE`,
  `D.FTKODE`, `MCGDATA.LENGTHB`, atau `MCGDATA.LISTAGG` pada `Calls`.
- Custom Oracle call yang valid tetap tercetak.
- Tidak ada perubahan pada controller, data-layer, EDMX, database, atau root
  `extract_db_usage.py`.

## Open questions

Tidak ada pertanyaan blocking berdasarkan hasil interview. Daftar built-in dapat
diperluas pada perubahan berikutnya jika ditemukan Oracle built-in baru, tetapi
function yang belum terdaftar tetap diperlakukan sebagai custom sesuai intent.
