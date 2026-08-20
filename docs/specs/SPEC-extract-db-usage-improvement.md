# Spec: Perbaikan extract_db_usage.py

Status: Draft untuk review implementasi

## Objective

Meningkatkan extract_db_usage.py agar laporan pemakaian database dari controller
ASP.NET MVC dan data layer lebih akurat, dapat diaudit, dan tidak memberikan kesan
lengkap ketika input sebenarnya gagal dibaca.

Pengguna utama adalah developer atau reviewer yang membutuhkan laporan Markdown
tentang object database yang dibaca, ditulis, atau dipanggil oleh suatu controller.
Script tetap merupakan static analyzer; script tidak menjalankan kode C#, tidak
menjalankan SQL, dan tidak membuka koneksi ke Oracle.

File target implementasi berada di mapping/extract_db_usage.py. File tersebut
merupakan snapshot baseline pada tahap spec ini. Source root tidak diubah selama
tahap specification.

## Scope

Perbaikan mencakup:

- preservasi semua kombinasi schema.object;
- pemisahan target write dan source read pada DML;
- dukungan MERGE, WITH, CTE, subquery, dan dependency antar-CTE;
- deteksi komentar C# dan SQL tanpa false positive dari isi komentar/string;
- ownership class/method yang benar dan resolusi call graph yang lebih terkontrol;
- deteksi EF read/write dari controller dan data layer;
- ekstraksi function/procedure, termasuk nama yang qualified jika tersedia;
- parsing EDMX berbasis XML, bukan regex attribute-order-dependent;
- error/diagnostic yang terlihat untuk input yang tidak dapat dibaca atau SQL dinamis;
- pengurangan biaya scan melalui exclusion generated files, indexing yang tepat, dan
  penghapusan helper mati;
- regression test untuk seluruh perilaku di atas.

Di luar scope:

- perubahan terhadap controller, data layer, EDMX, database schema, atau stored
  procedure Oracle;
- koneksi ke database untuk memvalidasi object;
- penyelesaian penuh terhadap SQL dinamis yang nilainya hanya diketahui saat runtime;
- migrasi seluruh codebase ke parser C# atau SQL eksternal;
- perubahan format frontmatter yang tidak diperlukan untuk output yang valid.

## Assumptions

1. Runtime yang digunakan adalah Python 3.
2. Input utama tetap source C# ASP.NET MVC, file EDMX, dan object Oracle.
3. Standard library Python menjadi default; dependency baru memerlukan persetujuan.
4. Section lama Direct Read, Direct Write, dan Calls dipertahankan.
5. Section baru CTE / Logical Relations boleh ditambahkan tanpa menghapus section
   lama.
6. Direct Read dan Direct Write hanya berisi physical database object, bukan nama
   CTE.
7. File root extract_db_usage.py tidak diganti otomatis oleh file di mapping.

## Capability requirements

### 1. Analysis contract

Analyzer harus menggunakan representasi internal yang tidak kehilangan schema.
Physical object minimal memiliki:

    PhysicalObject(schema, name, kind)

kind dapat berupa table, view, unknown, atau nilai lain yang dapat ditentukan dari
input. Jika jenis object tidak diketahui, analyzer tidak boleh menebak sebagai table
secara diam-diam.

Call minimal memiliki nama, jenis (function atau procedure bila diketahui), dan
schema/package jika tersedia.

Logical CTE minimal memiliki:

    CteRelation(name, physical_reads, cte_dependencies, consumers)

Aturan klasifikasi CTE:

- CTE selalu dilacak sebagai logical relation.
- Nama CTE tidak otomatis masuk Direct Read.
- Physical table/view yang dipakai di dalam definisi CTE masuk Direct Read.
- CTE yang memakai CTE lain menyimpan dependency ke CTE tersebut.
- Jika CTE menjadi sumber INSERT, UPDATE, DELETE, atau MERGE, CTE dan physical
  source tetap merupakan read; target DML masuk Direct Write.
- Nama CTE yang sama dengan physical object harus tetap dibedakan berdasarkan
  namespace logical versus physical.

### 2. Source indexing

Analyzer harus:

- menghapus/memask source comment C# pada controller dan data layer sebelum
  ekstraksi class, method, entity, dan call;
- tetap mempertahankan string literal sehingga SQL dalam string tidak hilang;
- mempertahankan ownership file → namespace/class → method → body;
- tidak memasukkan semua method dalam satu file ke semua class dalam file;
- membedakan overload menggunakan signature atau identifier internal yang stabil;
- mencegah method call di comment, string biasa, atau dead text menjadi call graph;
- mendeteksi call static yang dapat dibuktikan dari class data layer yang terindeks;
- mencatat call yang tidak dapat di-resolve sebagai diagnostic, bukan silently ignored;
- mengecualikan bin, obj, node_modules, dan generated *.Designer.cs dari indexing
  default, dengan opsi eksplisit bila generated source memang diperlukan;
- menggunakan queue yang sesuai untuk traversal call graph dan mencegah loop melalui
  visited key yang stabil.

find_matching_brace harus mengabaikan string dan comment ketika menghitung nesting.
Method expression-bodied, generic method, dan signature yang tidak didukung harus
ditangani dengan diagnostic yang jelas atau aturan fallback yang terdokumentasi.

### 3. SQL extraction

Ekstraksi SQL harus memakai tahap lexical/token-aware sehingga identifier dalam SQL
comment atau quoted value tidak dianggap object/function.

Statement minimal yang harus didukung:

- SELECT;
- INSERT INTO ... SELECT;
- UPDATE dengan subquery;
- DELETE dengan EXISTS/subquery;
- MERGE INTO ... USING;
- WITH dan beberapa CTE;
- UNION dan nested query;
- schema-qualified dan quoted identifier sejauh dapat ditentukan secara aman.

Klasifikasi DML harus statement-aware:

- target INSERT, UPDATE, DELETE, dan MERGE masuk Direct Write;
- source pada SELECT, USING, subquery, dan CTE masuk Direct Read;
- satu statement tidak boleh membuat seluruh object yang disebutnya menjadi write;
- source dan target harus tetap dicatat walaupun berada pada statement yang sama.

CTE harus diproses sebelum nama CTE dianggap sebagai table. Output logical relation
harus memuat nama CTE, physical reads, dependency CTE, dan consumer bila informasi
tersebut tersedia.

Function/procedure extraction harus:

- mempertahankan schema/package untuk SCHEMA.FUNCTION atau PACKAGE.FUNCTION bila
  ditemukan;
- memakai daftar Oracle built-in yang dapat dirawat dan diuji;
- tidak menganggap function bawaan sebagai custom function;
- mengenali OracleCommand literal sederhana;
- mengenali assignment sederhana ke command text bila dapat dibuktikan secara statis;
- mencatat command/procedure dinamis sebagai unresolved diagnostic.

C# verbatim, regular, dan interpolated string harus tidak diekstrak dua kali. SQL
yang terpecah melalui concatenation boleh dianalisis sebagian, tetapi bagian yang
tidak dapat direkonstruksi harus dilaporkan sebagai unresolved.

### 4. EDMX metadata mapping

Parser EDMX harus memakai xml.etree.ElementTree atau parser standard library setara.
Parser harus tidak bergantung pada urutan attribute, prefix namespace, atau format
whitespace.

Mapping harus:

- membedakan conceptual entity dan store entity set;
- mengambil schema dan physical store name bila tersedia;
- melakukan lookup case-insensitive untuk entity yang berasal dari C#;
- memberikan diagnostic bila entity tidak memiliki mapping;
- gagal secara eksplisit atau memberikan warning yang terlihat jika EDMX tidak dapat
  dibaca.

### 5. Reporting dan CLI

Output Markdown mempertahankan frontmatter serta section berikut:

    # Direct Read
    - MCGDATA.SOURCE_TABLE

    # Direct Write
    - MCGDATA.TARGET_TABLE

    # Calls
    - MCGDATA.CUSTOM_FUNCTION

    # CTE / Logical Relations
    - ACTIVE_ITEMS
      - Reads: MCGDATA.SOURCE_TABLE
      - Depends on: OTHER_CTE
      - Consumers: OUTER_QUERY

Aturan rendering:

- semua schema untuk object dengan nama sama harus dicetak;
- hasil harus deterministic dan sorted;
- CTE tidak dicetak sebagai MCGDATA.CTE_NAME pada physical section;
- duplicate entry tidak boleh muncul;
- metadata id, name, dan url harus di-escape atau divalidasi agar tidak merusak
  frontmatter;
- diagnostic unresolved ditampilkan melalui stderr dan/atau section Analysis Notes;
- --strict harus tersedia untuk mengubah input fatal, seperti controller/EDMX/data
  root yang tidak dapat dibaca, menjadi exit code non-zero;
- mode normal tidak boleh menyembunyikan kegagalan input dengan diam-diam memakai
  MCGDATA sebagai fallback tanpa warning.

CLI lama tetap menerima --controller, --output, --name, --url, --id, --data-root, dan
--edmx.

### 6. Maintainability dan performance

Implementasi harus:

- memisahkan orchestration dari lexical extraction, metadata mapping, dan rendering;
- menghapus helper/return value yang tidak digunakan;
- tidak memindai generated file besar secara default;
- mengindeks data layer satu kali per proses analisis;
- menggunakan set/dict dengan key canonical untuk deduplication;
- tidak menambah dependency hanya untuk menggantikan helper standard library;
- menyediakan diagnostic yang dapat membantu investigasi hasil yang kosong atau
  tidak lengkap.

## Tech Stack

- Python 3
- Standard library: argparse, collections, os, re, dan xml.etree.ElementTree atau
  modul standard library lain yang relevan
- Input: C# ASP.NET MVC, Oracle SQL, EDMX
- Output: Markdown dengan YAML frontmatter
- Test framework: unittest standard library

## Commands

Perintah berikut menjadi command contract untuk implementasi dan verifikasi:

    # Unit dan regression test
    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'

    # Smoke test CLI; gunakan fixture controller dan output temporary
    rtk python3 -B mapping/extract_db_usage.py \
      --controller "mapping/fixtures/SampleController.cs" \
      --data-root "mapping/fixtures/IMMD.Data" \
      --edmx "mapping/fixtures/DbModel.edmx" \
      --output "mapping/fixtures/out.md" \
      --name "Sample" \
      --url "/Sample" \
      --strict

Sesuai aturan repository, dotnet build, dotnet run, atau command sejenis tidak menjadi
bagian dari verifikasi perubahan ini.

## Project Structure

    mapping/
    ├── CAPABILITY-MAP.md
    ├── docs/specs/SPEC-extract-db-usage-improvement.md
    ├── extract_db_usage.py          # snapshot baseline dan target implementasi
    ├── tests/                        # dibuat pada fase implementasi
    └── fixtures/                     # dibuat pada fase implementasi

File root extract_db_usage.py tetap di luar perubahan fase ini. Keputusan untuk
mengganti atau memindahkan source root harus dilakukan pada task terpisah setelah
hasil mapping direview.

## Code Style

Gunakan nama yang menjelaskan apakah data bersifat physical atau logical. Hindari
map yang menggabungkan nama object tanpa schema.

Contoh gaya yang diharapkan:

    usage.add_physical_read(schema="MCGDATA", name="T_SOURCE")
    usage.add_physical_write(schema="MCGDATA", name="T_TARGET")
    usage.add_cte(
        name="ACTIVE_ITEMS",
        physical_reads={("MCGDATA", "T_SOURCE")},
        cte_dependencies=set(),
    )

Konvensi:

- fungsi kecil memiliki satu tanggung jawab;
- normalisasi nama dilakukan di boundary input;
- data internal menggunakan tuple/set canonical untuk deduplication;
- error input dibedakan dari pola source yang belum didukung;
- comment hanya ditambahkan untuk menjelaskan keputusan non-obvious;
- setiap perubahan kode lebih dari satu baris mengikuti project marker yang diwajibkan
  repository: IPRO Revisi Header Laporan Trading Term.

## Testing Strategy

Test harus diletakkan di mapping/tests/ dan tidak memerlukan database maupun source
code production yang besar.

### Unit test wajib

- renderer mempertahankan dua atau lebih schema untuk nama object yang sama;
- INSERT ... SELECT memisahkan target write dan source read;
- MERGE INTO ... USING memisahkan target dan source;
- CTE menghasilkan logical relation dan physical read dependency;
- CTE yang memakai CTE lain menghasilkan dependency yang benar;
- CTE tidak muncul sebagai physical Direct Read;
- SQL comment dan quoted value tidak menghasilkan false table/function;
- C# comment pada controller dan data layer tidak menghasilkan usage;
- verbatim string tidak terdeteksi dua kali;
- dua class dalam satu file tidak saling menerima method;
- overload method tidak menghilangkan body yang relevan;
- direct EF insert/update/delete diklasifikasikan sebagai write;
- Oracle built-in tidak muncul sebagai custom call;
- qualified function/procedure mempertahankan qualification;
- EDMX attribute order dan namespace prefix yang berbeda tetap terbaca;
- file input yang hilang menghasilkan warning/strict failure;
- metadata Markdown yang mengandung newline atau karakter YAML khusus tidak merusak
  frontmatter.

### Integration/golden test

Satu fixture controller, data layer kecil, dan EDMX minimal harus menghasilkan Markdown
yang dibandingkan dengan golden output. Golden output harus memuat setidaknya satu
physical read, satu physical write, satu call, dan satu CTE.

### Quality gate

- Semua test pada mapping/tests harus lulus.
- Tidak boleh ada regression pada section lama Direct Read, Direct Write, dan Calls
  untuk fixture yang tidak menggunakan fitur baru.
- Semua physical output harus memiliki schema yang eksplisit.
- Tidak boleh ada silent fallback ketika input wajib tidak dapat dibaca.

## Implementation Plan and Tasks

### Phase 1 — Contract dan baseline

- [ ] Definisikan model physical object, call, CTE, diagnostic, dan usage aggregate.
  - Acceptance: schema tidak hilang dan CTE memiliki namespace logical sendiri.
  - Verify: unit test multi-schema dan CTE classification.
  - Files: mapping/extract_db_usage.py, mapping/tests/test_contract.py.

- [ ] Tetapkan format Markdown baru dengan section CTE / Logical Relations.
  - Acceptance: format lama tetap ada dan output baru deterministic.
  - Verify: golden output.
  - Files: mapping/extract_db_usage.py, fixture Markdown.

### Phase 2 — Metadata dan source indexing

- [ ] Ganti parsing EDMX regex dengan XML parser namespace-tolerant.
  - Acceptance: attribute order tidak memengaruhi mapping; error terlihat.
  - Verify: EDMX fixtures dengan variasi order/prefix.
  - Files: mapping/extract_db_usage.py, mapping/tests/test_edmx.py.

- [ ] Bangun lexical masking untuk C# dan method/class ownership.
  - Acceptance: comment/string tidak masuk call graph; method tetap berada pada class
    yang benar.
  - Verify: comment, brace, multi-class, overload fixtures.
  - Files: mapping/extract_db_usage.py, mapping/tests/test_source_index.py.

### Phase 3 — SQL dan CTE

- [ ] Implementasikan token-aware SQL extraction dan DML target/source model.
  - Acceptance: MERGE, WITH, subquery, INSERT ... SELECT, dan quoted/commented SQL
    menghasilkan klasifikasi yang benar.
  - Verify: table-driven SQL tests.
  - Files: mapping/extract_db_usage.py, mapping/tests/test_sql_extraction.py.

- [ ] Tambahkan CTE relation tracking dan dependency graph.
  - Acceptance: nama CTE tidak menjadi physical object; source table dan dependency
    tetap tersedia pada laporan.
  - Verify: single CTE, chained CTE, CTE sebagai DML source.
  - Files: mapping/extract_db_usage.py, mapping/tests/test_cte.py.

### Phase 4 — Integration, diagnostics, dan regression

- [ ] Perbaiki EF read/write detection dan static call resolution.
  - Acceptance: direct controller write, data-layer write, dan nested call terdeteksi
    tanpa mengambil comment/dead text.
  - Verify: controller/data-layer fixture.
  - Files: mapping/extract_db_usage.py, integration tests.

- [ ] Tambahkan diagnostics, strict mode, generated-file exclusion, dan cleanup helper.
  - Acceptance: input wajib yang hilang menghasilkan exit code non-zero pada strict
    mode; unresolved dynamic SQL terlihat.
  - Verify: CLI smoke tests dan missing-input tests.
  - Files: mapping/extract_db_usage.py, CLI tests.

- [ ] Jalankan golden/regression suite dan review output terhadap baseline.
  - Acceptance: semua test lulus, output lama tetap kompatibel, dan tidak ada schema
    atau CTE yang hilang.
  - Verify: command test contract di atas.
  - Files: mapping/tests/, mapping/fixtures/.

### Checkpoint

Setelah Phase 2 dan Phase 4, hasil harus direview sebelum melanjutkan. Review wajib
memeriksa classification read/write, CTE semantics, schema preservation, dan diagnostic
behavior.

## Boundaries

### Always

- Pertahankan semua schema dan logical CTE information.
- Jalankan focused Python tests sebelum commit implementasi.
- Gunakan standard library kecuali dependency baru disetujui.
- Jaga source C# dan database tetap read-only.
- Tambahkan project marker pada perubahan kode sesuai aturan repository.
- Dokumentasikan unsupported/dynamic pattern sebagai diagnostic.

### Ask first

- Mengganti atau menghapus file root extract_db_usage.py.
- Mengubah struktur frontmatter atau contract Markdown yang sudah dikonsumsi pihak lain.
- Menambahkan dependency Python baru.
- Mengubah aturan exclusion generated source.
- Mengubah definisi CTE dari logical relation menjadi physical object.

### Never

- Menjalankan SQL atau menghubungi database dari analyzer.
- Mengedit controller, data layer, atau EDMX sebagai bagian dari fitur ini.
- Mengabaikan CTE karena bukan physical table.
- Menghilangkan schema kedua atau memilih schema secara arbitrer.
- Menyembunyikan error input dengan fallback diam-diam.
- Menjalankan dotnet build atau dotnet run setelah perubahan sesuai aturan repository.

## Success Criteria

Implementasi dianggap memenuhi spec jika:

1. Object dengan nama sama pada dua schema dicetak sebagai dua entry.
2. INSERT ... SELECT mencetak target sebagai write dan source sebagai read.
3. MERGE INTO ... USING mencetak target sebagai write dan source sebagai read.
4. CTE dicetak pada CTE / Logical Relations dan tidak dicetak sebagai physical table.
5. Physical table/view yang dibaca CTE masuk Direct Read.
6. Dependency antar-CTE dan consumer tersedia bila dapat ditentukan statically.
7. SQL/C# comment tidak menghasilkan table, function, procedure, atau method call palsu.
8. Method dari class berbeda tidak tercampur hanya karena berada dalam file yang sama.
9. Direct EF write dari controller dan data layer masuk Direct Write.
10. EDMX tetap terbaca walaupun attribute order/namespace prefix berubah.
11. Function/procedure qualified tidak kehilangan qualification yang ditemukan.
12. Dynamic SQL/procedure yang tidak dapat di-resolve menghasilkan diagnostic.
13. Input wajib yang hilang terlihat jelas dan strict mode mengembalikan non-zero exit.
14. Output lama tetap memiliki section utama dan hasil deterministic.
15. Seluruh regression test lulus tanpa build/run aplikasi .NET.

## Open Questions

- Apakah setelah implementasi selesai mapping/extract_db_usage.py akan menggantikan
  file root, atau tetap menjadi tool terpisah?
- Apakah consumer Markdown membutuhkan section CTE / Logical Relations dengan nama persis
  tersebut, atau hanya membutuhkan informasi CTE tanpa ketergantungan pada judul?
- Seberapa jauh simple variable propagation untuk dynamic OracleCommand perlu dilakukan
  sebelum pola tersebut cukup diberi diagnostic?
