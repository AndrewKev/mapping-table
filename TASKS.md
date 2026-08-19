# Task Breakdown: Perbaikan extract_db_usage.py

Status: Complete — T001–T021 implemented and verified
Plan: mapping/IMPLEMENTATION-PLAN.md
Spec: mapping/SPEC-extract-db-usage-improvement.md
Tracker: Tidak ada; checklist ini adalah task target.

Verification result:

- Full `unittest` discovery: 43 tests passed.
- CLI fixture smoke with `--strict`: passed.
- No .NET build/run command executed.
- Changed implementation, tests, and fixtures remain inside `mapping/`.

## Working rules

- Kerjakan task sesuai dependency dan urutan phase.
- Setiap task harus meninggalkan source dalam keadaan dapat diuji.
- Tulis test sebelum atau bersamaan dengan perubahan behavior.
- Semua perubahan kode pada mapping/extract_db_usage.py mengikuti project marker
  IPRO Revisi Header Laporan Trading Term.
- Jangan mengubah file root, controller, data layer, EDMX, atau database.
- Gunakan command test yang memakai standard library.
- Jangan menjalankan dotnet build, dotnet run, atau command build/run .NET lainnya.

## Phase 1 — Foundation and contract

### T001 — Buat unittest harness dan fixture convention

Module: verification-regression

Description: Buat struktur mapping/tests dan helper fixture minimal agar test dapat
dijalankan dengan unittest discovery tanpa database atau dependency tambahan.

Acceptance criteria:

- [ ] Command unittest discovery dapat menemukan dan menjalankan minimal satu test
      smoke yang lulus.
- [ ] Test dapat membaca fixture menggunakan path yang stabil relatif terhadap file
      test, bukan current working directory.
- [ ] Harness tidak mengimpor atau mengeksekusi source C# production.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'

Dependencies: None

Files likely touched:

- mapping/tests/test_support.py
- mapping/tests/test_smoke.py

Estimated scope: S

### T002 — Definisikan canonical physical object dan diagnostic identity

Module: analysis-contract

Description: Tambahkan model/helper internal untuk physical object, call, diagnostic,
dan canonical key tanpa mengubah output CLI terlebih dahulu.

Acceptance criteria:

- [ ] Physical identity selalu menyimpan schema dan name; kind tidak boleh
      menghilangkan identity utama.
- [ ] Diagnostic memiliki severity/code/message yang dapat diuji.
- [ ] Input kosong atau whitespace tidak menghasilkan object identity valid.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_contract.py'

Dependencies: T001

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_contract.py

Estimated scope: S

### T003 — Pertahankan seluruh schema pada usage aggregate dan sorting primitive

Module: analysis-contract

Description: Ubah penyimpanan dan helper sorting agar object yang sama pada beberapa
schema tetap menjadi beberapa physical entry.

Acceptance criteria:

- [ ] MCGDATA.T dan OTHER.T tetap tersimpan sebagai dua entry.
- [ ] Urutan output deterministic.
- [ ] Unqualified object tetap menggunakan default schema tanpa menghapus explicit
      schema lain.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_schema_identity.py'

Dependencies: T002

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_schema_identity.py

Estimated scope: S

### T004 — Definisikan model CTE/logical relation

Module: analysis-contract

Description: Tambahkan representasi CTE yang terpisah dari physical object dan
mendukung physical reads, dependency antar-CTE, serta consumer.

Acceptance criteria:

- [ ] CTE memiliki namespace logical dan tidak masuk physical read/write map.
- [ ] Physical reads, CTE dependencies, dan consumers dapat disimpan sebagai set
      canonical.
- [ ] Dua CTE dengan nama berbeda tidak saling menimpa.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_cte_model.py'

Dependencies: T002

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_cte_model.py

Estimated scope: S

### Checkpoint A — Contract

- [ ] T001–T004 selesai.
- [ ] Test harness, multi-schema identity, dan CTE model lulus.
- [ ] Reviewer menyetujui contract sebelum parser diubah.

## Phase 2 — Metadata and source indexing

### T005 — Ganti parser EDMX menjadi namespace/order tolerant

Module: metadata-mapping

Description: Ganti regex EntitySet dengan xml.etree.ElementTree dan normalisasi
attribute/namespace yang diperlukan untuk membaca store entity set.

Acceptance criteria:

- [ ] Attribute order dan whitespace tidak memengaruhi hasil mapping.
- [ ] Prefix namespace berbeda tetap dapat diproses.
- [ ] Schema dan physical store name terbaca bila tersedia.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_edmx.py'

Dependencies: T002

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_edmx.py
- mapping/fixtures/edmx_variants.xml

Estimated scope: M

### T006 — Tambahkan C# lexical masking untuk comment dan string

Module: source-indexing

Description: Bangun satu boundary masking yang dipakai controller dan data layer,
memisahkan comment dari string literal dan mempertahankan posisi/isi yang dibutuhkan
extractor.

Acceptance criteria:

- [ ] C# line/block comment tidak terbaca sebagai source code.
- [ ] Regular, verbatim, dan interpolated string tetap tersedia untuk SQL extraction.
- [ ] Brace atau SQL marker di dalam string tidak memengaruhi masking.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_csharp_mask.py'

Dependencies: T002

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_csharp_mask.py

Estimated scope: M

### T007 — Pertahankan ownership class/method dan brace matching

Module: source-indexing

Description: Ubah method extraction agar setiap method tetap terhubung ke class,
signature/overload tidak dicampur, dan brace matching mengabaikan comment/string.

Acceptance criteria:

- [ ] Method dari dua class dalam satu file tidak saling terasosiasi.
- [ ] Overload dapat disimpan tanpa kehilangan body.
- [ ] Brace di comment/string tidak memotong atau memperpanjang method body.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_source_index.py'

Dependencies: T006

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_source_index.py
- mapping/fixtures/multi_class.cs

Estimated scope: M

### T008 — Perketat static call graph dan unresolved call tracking

Module: source-indexing

Description: Batasi static call extraction pada call yang berada di source body
yang valid, gunakan traversal queue yang sesuai, dan catat call yang tidak dapat
di-resolve tanpa memasukkannya sebagai database usage.

Acceptance criteria:

- [ ] Call dari comment/string/dead text tidak masuk queue.
- [ ] Recursive call tidak menyebabkan infinite loop.
- [ ] Call yang class/method-nya tidak ditemukan menghasilkan diagnostic, bukan
      physical object palsu.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_call_graph.py'

Dependencies: T007

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_call_graph.py

Estimated scope: M

### Checkpoint B — Metadata and source

- [ ] T005–T008 selesai.
- [ ] EDMX variants, C# masking, multi-class, overload, dan call graph test lulus.
- [ ] Tidak ada diagnostic yang mengubah unresolved call menjadi database object.

## Phase 3 — SQL and CTE extraction

### T009 — Hilangkan duplicate dan false capture pada C# SQL literal

Module: sql-extraction

Description: Perbaiki extraction regular/verbatim/interpolated string agar literal
tidak diproses dua kali dan fragment yang jelas bukan SQL tidak masuk extractor.

Acceptance criteria:

- [ ] Verbatim string hanya menghasilkan satu literal.
- [ ] C# keyword seperti using di luar SQL tidak membuang SQL valid secara keliru.
- [ ] Fragment yang tidak dapat direkonstruksi menghasilkan diagnostic bila relevan.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_sql_literals.py'

Dependencies: T006

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_sql_literals.py

Estimated scope: M

### T010 — Bangun SQL lexical scanner untuk comment, quoted value, dan identifier

Module: sql-extraction

Description: Tambahkan tokenization minimal yang membedakan SQL comment, quoted
literal, identifier, keyword, punctuation, dan nested parenthesis.

Acceptance criteria:

- [ ] Identifier di SQL comment atau quoted value tidak dianggap table/function.
- [ ] Quoted/schema-qualified identifier yang didukung dapat dinormalisasi.
- [ ] Nested parenthesis tidak membuat scan berhenti pada delimiter yang salah.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_sql_lexer.py'

Dependencies: T009

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_sql_lexer.py

Estimated scope: M

### T011 — Ekstrak physical object dari SELECT, JOIN, subquery, dan CTE source

Module: sql-extraction

Description: Gunakan token hasil T010 untuk menemukan table/view physical object dari
SELECT, JOIN, EXISTS, IN, UNION, nested query, dan source CTE tanpa menjadikan nama
CTE sebagai physical table.

Acceptance criteria:

- [ ] FROM/JOIN/EXISTS/IN dan nested source terdeteksi.
- [ ] CTE name dikenali sebagai logical relation candidate, bukan physical object.
- [ ] Oracle builtin object seperti DUAL tetap tidak masuk physical output.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_sql_objects.py'

Dependencies: T010, T004

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_sql_objects.py

Estimated scope: M

### T012 — Implementasikan DML target/source classification

Module: sql-extraction

Description: Pisahkan physical target write dari physical source read untuk INSERT,
UPDATE, DELETE, dan MERGE.

Acceptance criteria:

- [ ] INSERT INTO target SELECT FROM source menghasilkan target write dan source read.
- [ ] MERGE INTO target USING source menghasilkan target write dan source read.
- [ ] UPDATE/DELETE dengan subquery tidak mengklasifikasikan subquery source sebagai
      write.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_dml_classification.py'

Dependencies: T011

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_dml_classification.py

Estimated scope: M

### T013 — Bangun CTE parser dan dependency graph

Module: sql-extraction

Description: Parse WITH clause, daftar CTE, physical reads di dalam definisi,
dependency antar-CTE, dan consumer pada query utama.

Acceptance criteria:

- [ ] Single CTE menghasilkan satu logical relation dan physical read dependency.
- [ ] Chained CTE menyimpan dependency graph yang benar.
- [ ] CTE yang digunakan sebagai source DML tetap logical/read, sedangkan target DML
      tetap physical/write.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_cte_extraction.py'

Dependencies: T011, T012, T004

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_cte_extraction.py

Estimated scope: M

### T014 — Perbaiki function/procedure extraction dan dynamic diagnostics

Module: sql-extraction

Description: Pertahankan schema/package pada function/procedure qualified, perluas
builtin filtering, dan laporkan command dinamis yang tidak dapat di-resolve.

Acceptance criteria:

- [ ] SCHEMA.FUNCTION atau PACKAGE.FUNCTION tidak kehilangan qualification.
- [ ] Oracle builtin yang terdaftar tidak muncul sebagai custom call.
- [ ] OracleCommand dengan variable/dynamic value menghasilkan unresolved diagnostic,
      bukan procedure name yang ditebak.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_calls.py'

Dependencies: T009, T010

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_calls.py

Estimated scope: M

### Checkpoint C — SQL and CTE

- [ ] T009–T014 selesai.
- [ ] SQL lexer, DML, CTE, function, dan procedure tests lulus.
- [ ] Semua test memastikan CTE tetap terpisah dari physical Direct Read/Write.

## Phase 4 — Integration, reporting, and operational behavior

### T015 — Tambahkan EF read/write detection yang konsisten

Module: source-indexing

Description: Satukan detection entity EF untuk controller dan data-layer sehingga
read dan InsertSave/UpdateSave/Delete write tidak bergantung pada lokasi pemanggilan.

Acceptance criteria:

- [ ] CurrentDataContext entity read tetap masuk Direct Read.
- [ ] Direct controller EF write masuk Direct Write.
- [ ] Data-layer InsertSave, UpdateSave, dan Delete masuk Direct Write tanpa duplicate.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_ef_usage.py'

Dependencies: T007, T012

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_ef_usage.py

Estimated scope: M

### T016 — Integrasikan analyzer orchestration dan nested method resolution

Module: source-indexing

Description: Hubungkan canonical model, metadata map, SQL extraction, EF detection, dan
call graph traversal dalam analyze_controller tanpa mengubah source root.

Acceptance criteria:

- [ ] Controller direct usage dan nested data-layer usage masuk aggregate yang sama.
- [ ] visited tracking mencegah loop dan duplicate body processing.
- [ ] class/method yang tidak dapat di-resolve menghasilkan diagnostic yang dapat
      ditampilkan CLI.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_analyzer_integration.py'

Dependencies: T005, T008, T013, T015

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_analyzer_integration.py

Estimated scope: M

### T017 — Render semua physical schema dan CTE section terpisah

Module: reporting-cli

Description: Pertahankan section lama, cetak seluruh physical schema, dan tambahkan
section CTE / Logical Relations tanpa memasukkan CTE sebagai physical object.

Acceptance criteria:

- [ ] Direct Read/Write mencetak semua schema tanpa collapse.
- [ ] Calls tetap deterministic dan duplicate-free.
- [ ] CTE tampil di section terpisah dengan Reads, Depends on, dan Consumers bila ada.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_rendering.py'

Dependencies: T003, T004, T014, T016

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_rendering.py

Estimated scope: M

### T018 — Tambahkan input validation, diagnostics, dan strict CLI mode

Module: reporting-cli

Description: Ubah silent read failure menjadi diagnostic, validasi metadata frontmatter,
dan tambahkan strict mode untuk input fatal.

Acceptance criteria:

- [ ] Missing controller/data-root/EDMX terlihat sebagai diagnostic.
- [ ] --strict mengembalikan non-zero exit untuk input wajib yang gagal dibaca.
- [ ] Metadata name/url/id yang invalid tidak merusak frontmatter output.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_cli_diagnostics.py'

Dependencies: T005, T016, T017

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_cli_diagnostics.py

Estimated scope: M

### T019 — Kurangi scan generated files dan hapus code mati

Module: maintainability-and-performance

Description: Keluarkan generated *.Designer.cs dari scan default, pastikan indexing
hanya dilakukan sekali per proses, dan hapus helper/return value yang tidak digunakan
setelah semua consumer diverifikasi.

Acceptance criteria:

- [ ] bin, obj, node_modules, dan generated Designer file tidak diproses secara
      default.
- [ ] Data-layer indexing tidak diulang untuk setiap nested call.
- [ ] resolve_method, class_entities, dan parameter/return value yang benar-benar
      tidak digunakan tidak tersisa tanpa alasan terdokumentasi.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_indexing_performance.py'

Dependencies: T008, T016

Files likely touched:

- mapping/extract_db_usage.py
- mapping/tests/test_indexing_performance.py

Estimated scope: S

### Checkpoint D — Integration and operational behavior

- [ ] T015–T019 selesai.
- [ ] Integration, rendering, diagnostics, strict mode, dan indexing tests lulus.
- [ ] Output legacy sections tetap tersedia.

## Phase 5 — Regression acceptance

### T020 — Buat integration fixture dan golden output

Module: verification-regression

Description: Buat fixture controller, data layer kecil, dan EDMX yang mencakup
physical read/write, function/procedure, nested call, dan CTE; tetapkan golden Markdown.

Acceptance criteria:

- [ ] Fixture memuat minimal satu physical read, write, call, dan CTE.
- [ ] Golden output memuat semua schema yang ditemukan.
- [ ] Golden output tidak menampilkan CTE sebagai physical table.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_golden_output.py'

Dependencies: T005, T013, T017, T018

Files likely touched:

- mapping/tests/test_golden_output.py
- mapping/fixtures/SampleController.cs
- mapping/fixtures/IMMD.Data/SampleRepository.cs
- mapping/fixtures/DbModel.edmx
- mapping/fixtures/expected.md

Estimated scope: M

### T021 — Jalankan full regression dan review acceptance criteria

Module: verification-regression

Description: Jalankan seluruh test suite, bandingkan output golden dengan contract spec,
dan dokumentasikan hasil/verifikasi sebelum implementasi dianggap siap direview.

Acceptance criteria:

- [ ] Semua test unittest discovery lulus.
- [ ] Seluruh 15 success criteria di spec memiliki test atau evidence yang jelas.
- [ ] Tidak ada perubahan di luar mapping dan tidak ada build/run .NET yang dijalankan.

Verification:

    rtk python3 -B -m unittest discover -s mapping/tests -p 'test_*.py'

Manual check: confirm from the execution log that no .NET build/run command was
executed and that the changed-file list is limited to mapping/.

Dependencies: T020

Files likely touched:

- mapping/TASKS.md
- mapping/IMPLEMENTATION-PLAN.md

Estimated scope: S

## Checkpoint E — Complete

- [ ] T001–T021 selesai atau memiliki deferment tertulis.
- [ ] Full focused Python test suite lulus.
- [ ] Spec success criteria seluruhnya ter-cover.
- [ ] Hasil siap untuk code review.
- [ ] Keputusan mengganti file root dibuat terpisah dan eksplisit.

## Task sizing summary

| Size | Tasks |
|---|---|
| S | T001, T002, T003, T004, T008, T019, T021 |
| M | T005, T006, T007, T009, T010, T011, T012, T013, T014, T015, T016, T017, T018, T020 |
| L/XL | Tidak ada |

## Deferred items

- Advanced C# parser atau SQL parser external.
- Full runtime data-flow analysis untuk dynamic SQL.
- Penggantian source root dengan mapping copy.
- Database connectivity validation.
