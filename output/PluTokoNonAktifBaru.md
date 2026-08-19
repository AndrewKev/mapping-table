---
id: "PluTokoNonAktifBaru"
name: "PluTokoNonAktifBaru"
group: IMMD
url: "/Transaction/PluTokoNonAktifBaru"
---

# Direct Read

- MCGDATA.D_PLU_NONAKTIF
- MCGDATA.D_TOKO_PLU_NONAKTIF
- MCGDATA.D_WILAYAH_PLU_NONAKTIF
- MCGDATA.KETENTUAN_PLU_NONAKTIF
- MCGDATA.M_CATATAN_PLU_NONAKTIF
- MCGDATA.PLU_TOKO_NON_AKTIF_MV
- MCGDATA.TEMP_LAP_PLU_NONAKTIF
- MCGDATA.T_CABANG
- MCGDATA.T_DEPT
- MCGDATA.T_DIVISI
- MCGDATA.T_KATEGORI
- MCGDATA.T_TOKO
- MCGDATA.T_UNIT
- MCGDATA.T_WILAYAH
- MCGDATA.UNGGAH_TOKO_PLU_NONAKTIF
- MCGDATA.V_HAPUS_PLU_NONAKTIF
- MCGDATA.V_LAP_PLU_NONAKTIF

# Direct Write

- MCGDATA.D_PLU_NONAKTIF
- MCGDATA.D_TOKO_PLU_NONAKTIF
- MCGDATA.D_WILAYAH_PLU_NONAKTIF
- MCGDATA.M_PLU_NONAKTIF
- MCGDATA.UNGGAH_TOKO_PLU_NONAKTIF

# Calls

- MCGDATA.CARI_DESK_PRODUK
- MCGDATA.LAP_PLU_NONAKTIF
- MCGDATA.PLUTOKOUSERACTION
- MCGDATA.SIMPAN_PLU_TOKO_NON_AKTIF
- MCGDATA.VAL_UNGGAH_PLU_TOKO_NON_AKTIF

# Analysis Notes

- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM unggah_toko_plu_nonaktif where user_update = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE USER_UPDATE ='"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE VALIDASI <> 'VALID' AND USER_UPDATE ='"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE VALIDASI = 'VALID' AND USER_UPDATE ='"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT cari_desk_produk('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: <empty>
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"DELETE FROM D_TOKO_PLU_NONAKTIF B
                                                WHERE EXISTS (
                                                    SELECT 1
                                                    FROM d_wilayah_plu_nonaktif A
                                                    JOIN d_toko_plu_nonaktif B2 ON A.no_trans = B2.no_trans
                                                    JOIN d_plu_nonaktif C ON A.no_trans = C.no_trans
                                                    JOIN t_toko D ON B2.kd_toko = D.ftkode
                                                    WHERE A.tgl_akhir > SYSDATE
                                                    AND B.no_trans = A.no_trans
                                                    AND B.kd_toko = B2.kd_toko"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"DELETE FROM M_PLU_NONAKTIF M
                                            WHERE EXISTS (
                                                SELECT 1
                                                FROM d_wilayah_plu_nonaktif A
                                                JOIN d_toko_plu_nonaktif B ON A.no_trans = B.no_trans
                                                JOIN d_plu_nonaktif C ON A.no_trans = C.no_trans
                                                JOIN t_toko D ON B.kd_toko = D.ftkode
                                                WHERE A.tgl_akhir > SYSDATE
                                                AND M.no_trans = A.no_trans
                                                AND M.kd_toko = B.kd_toko
                                                AND M.plu = C.plu "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT
                                                d.ftkcab                         AS kode_dc,
                                                e.ftnama                          AS nama_dc,
                                                b.kd_toko                          AS kode_toko,
                                                d.ftnama                          AS nama_toko,
                                                TO_CHAR(c.plu)                     AS plu,
                                                Cari_Desk_Produk(c.plu)            AS deskripsi
                                            FROM d_toko_plu_nonaktif b, d_plu_nonaktif c,
	                                                t_toko d, t_cabang e
                                            WHERE b.no_trans = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT Cari_Desk_Produk(b.plu) FROM d_wilayah_plu_nonaktif a, d_plu_nonaktif b
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.plu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT c.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND opu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT count(*) FROM ketentuan_plu_nonaktif
                                                    WHERE INSTR(','||TRIM(USER_AKSES)|| ',', ','||'"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT d.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c, t_cabang d
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.kd_toko = c.ftkode 
                                            AND d.ftkode = c.ftkcab
                                            AND a.opu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT distinct c.ftkcab, d.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c, t_cabang d
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.kd_toko = c.ftkode 
                                            AND d.ftkode = c.ftkcab
                                            AND opu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT distinct c.ftkode, c.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND a.opu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query1
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query2
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query3
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: '
                          WHERE no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: ') FROM dual
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM D_TOKO_PLU_NONAKTIF B
                                                WHERE EXISTS (
                                                    SELECT 1
                                                    FROM d_wilayah_plu_nonaktif A
                                                    JOIN d_toko_plu_nonaktif B2 ON A.no_trans = B2.no_trans
                                                    JOIN d_plu_nonaktif C ON A.no_trans = C.no_trans
                                                    JOIN t_toko D ON B2.kd_toko = D.ftkode
                                                    WHERE A.tgl_akhir > SYSDATE
                                                    AND B.no_trans = A.no_trans
                                                    AND B.kd_toko = B2.kd_toko
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM M_PLU_NONAKTIF M
                                            WHERE EXISTS (
                                                SELECT 1
                                                FROM d_wilayah_plu_nonaktif A
                                                JOIN d_toko_plu_nonaktif B ON A.no_trans = B.no_trans
                                                JOIN d_plu_nonaktif C ON A.no_trans = C.no_trans
                                                JOIN t_toko D ON B.kd_toko = D.ftkode
                                                WHERE A.tgl_akhir > SYSDATE
                                                AND M.no_trans = A.no_trans
                                                AND M.kd_toko = B.kd_toko
                                                AND M.plu = C.plu 
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM d_plu_nonaktif WHERE no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM d_toko_plu_nonaktif WHERE no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM d_wilayah_plu_nonaktif WHERE no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM m_plu_nonaktif WHERE no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM unggah_toko_plu_nonaktif where user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT
                                                d.ftkcab                         AS kode_dc,
                                                e.ftnama                          AS nama_dc,
                                                b.kd_toko                          AS kode_toko,
                                                d.ftnama                          AS nama_toko,
                                                TO_CHAR(c.plu)                     AS plu,
                                                Cari_Desk_Produk(c.plu)            AS deskripsi
                                            FROM d_toko_plu_nonaktif b, d_plu_nonaktif c,
	                                                t_toko d, t_cabang e
                                            WHERE b.no_trans = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE USER_UPDATE ='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE VALIDASI <> 'VALID' AND USER_UPDATE ='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT COUNT(*) AS TOTAL FROM unggah_toko_plu_nonaktif WHERE VALIDASI = 'VALID' AND USER_UPDATE ='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT Cari_Desk_Produk(b.plu) FROM d_wilayah_plu_nonaktif a, d_plu_nonaktif b
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.plu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT FTKODE, FTNAMA FROM T_DEPT
                                          WHERE FTKDIV = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT FTKODE, FTNAMA FROM T_DEPT
                                          WHERE FTKDIV IN (
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT FTKODE, FTNAMA FROM T_KATEGORI
                                          WHERE FTKDEP = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT FTKODE, FTNAMA FROM T_KATEGORI
                                          WHERE FTKDEP IN(
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT c.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND opu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT cari_desk_produk('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT count(*) FROM ketentuan_plu_nonaktif
                                                    WHERE INSTR(','||TRIM(USER_AKSES)|| ',', ','||'
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT d.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c, t_cabang d
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.kd_toko = c.ftkode 
                                            AND d.ftkode = c.ftkcab
                                            AND a.opu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT distinct c.ftkcab, d.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c, t_cabang d
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND b.kd_toko = c.ftkode 
                                            AND d.ftkode = c.ftkcab
                                            AND opu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT distinct c.ftkode, c.ftnama FROM d_wilayah_plu_nonaktif a, d_toko_plu_nonaktif b,  t_toko c
                                            WHERE a.no_trans = b.no_trans
                                            AND a.tgl_akhir > SYSDATE
                                            AND a.opu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select no_trans, opu, kd_wilayah,
                                 tgl_awal, tgl_akhir, keterangan,
                                 catatan, status, kd_dc, nm_dc,
                                 kd_toko, nm_toko, plu, deskripsi
                          from temp_lap_plu_nonaktif
                          where user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: update d_wilayah_plu_nonaktif 
                          set keterangan = '
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_DIVISI.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_TOKO.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_UNIT.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_WILAYAH.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_WILAYAH.Where

