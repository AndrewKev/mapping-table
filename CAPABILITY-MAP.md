# Capability Map: extract_db_usage

Status: Draft for implementation review

Tujuan inisiatif ini adalah meningkatkan akurasi dan keterlacakan static analyzer
database tanpa mengubah aplikasi ASP.NET MVC atau melakukan koneksi ke Oracle.

| Module id | Tanggung jawab | Depends on |
|---|---|---|
| analysis-contract | Model canonical untuk physical database object, CTE/logical relation, read, write, dan call | — |
| source-indexing | Lexical masking C#, comment handling, kepemilikan class/method, dan call graph data layer | analysis-contract |
| metadata-mapping | Parsing EDMX dan pemetaan entity ke schema/object secara robust | analysis-contract |
| sql-extraction | Ekstraksi SQL, DML target/source, CTE, function, procedure, dan schema-qualified name | analysis-contract, source-indexing |
| reporting-cli | Rendering Markdown, diagnostics, strict mode, dan kompatibilitas CLI | analysis-contract, metadata-mapping, sql-extraction |
| verification-regression | Unit test, fixture, golden output, dan regression coverage | Semua module |

## Build order

analysis-contract → (source-indexing dan metadata-mapping secara paralel) →
sql-extraction → reporting-cli → verification-regression

## Cross-cutting rules

- CTE adalah logical relation yang penting dan selalu dilacak pada section terpisah.
- CTE tidak otomatis dimasukkan ke Direct Read; object fisik yang dibaca oleh CTE
  masuk Direct Read.
- Semua schema yang ditemukan harus dipertahankan; tidak boleh memilih satu schema
  secara arbitrer.
- Analisis harus bersifat read-only terhadap source C# dan database.
- Implementasi menggunakan standard library Python kecuali ada persetujuan eksplisit
  untuk dependency baru.

