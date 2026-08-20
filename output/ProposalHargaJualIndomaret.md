---
id: "ProposalHargaJualIndomaret"
name: "ProposalHargaJualIndomaret"
group: IMMD
url: "/Transaction/ProposalHargaJualIndomaret"
---

# Direct Read

- MCGDATA.APPROVAL_PROP_HGJUAL_IDM
- MCGDATA.APPROVAL_RAFAKSI
- MCGDATA.BATAS_UBAH_HGJUAL
- MCGDATA.DATA_MD
- MCGDATA.DC_BY_WILAYAH
- MCGDATA.DC_PPN_KECUALI
- MCGDATA.D_PRODUCT_GROUP
- MCGDATA.D_RAFAKSI_HGJUAL
- MCGDATA.D_RAFAKSI_PARTISIPAN
- MCGDATA.HANDSONTABLE_VALIDATION
- MCGDATA.HGJUAL_IDM_NASIONAL
- MCGDATA.HGJUAL_IDM_PER_MD
- MCGDATA.HGJUAL_IDM_PER_MD_V
- MCGDATA.HO_TOKO_T
- MCGDATA.H_RAFAKSI
- MCGDATA.MSJABATAN
- MCGDATA.MSUSER
- MCGDATA.M_AKSES_PLU_HGJUAL
- MCGDATA.M_CURR_SUPP
- MCGDATA.M_KETENTUAN_HGJUAL_DIVDEPKAT
- MCGDATA.M_LAST_COST_PER_DC_AKTUAL_TEMP
- MCGDATA.M_LAST_COST_PER_DC_AKT_MD_TEMP
- MCGDATA.M_LAST_COST_PER_DC_MD_TEMP
- MCGDATA.M_LAST_COST_PER_DC_TEMP
- MCGDATA.M_LEVEL_HGJUAL_IDM
- MCGDATA.M_MDHGJUAL_USER_CBG
- MCGDATA.M_MD_HGJUAL
- MCGDATA.M_MD_HGJUAL_DC
- MCGDATA.M_PRODUCT_GROUP
- MCGDATA.M_PRODUK
- MCGDATA.M_PROMOSI
- MCGDATA.M_SELL_UNIT
- MCGDATA.M_STD_MARGIN_DIVDEPKAT
- MCGDATA.M_STD_MARGIN_PLU
- MCGDATA.M_STD_MARGIN_TIPEJUAL
- MCGDATA.M_SUBCLASS_HARGA_NEW
- MCGDATA.M_TIPE_HARGA_NEW
- MCGDATA.M_ZONA_HGJUAL_DTL
- MCGDATA.M_ZONA_HGJUAL_HDR
- MCGDATA.PRD_HGBELI_FLUKTUATIF
- MCGDATA.PRODUK_MARGIN_KHUSUS
- MCGDATA.PROP_GRUP_PRODUK_NAS_TEMP
- MCGDATA.PROP_GRUP_PRODUK_PER_MD_TEMP
- MCGDATA.PROP_HGJUAL_IDM_NASIONAL_TEMP
- MCGDATA.PROP_HGJUAL_IDM_PER_MD
- MCGDATA.PROP_HGJUAL_IDM_PER_MD_TEMP
- MCGDATA.TEMP_BULAN
- MCGDATA.TOKO_MURAH_HEADER
- MCGDATA.T_CABANG
- MCGDATA.T_MAIL_ATASAN
- MCGDATA.T_MAIL_BAWAHAN
- MCGDATA.T_PLU_NONAKTIF
- MCGDATA.VAL_SALIN_HARGA_TEMP
- MCGDATA.VU_M_LAST_COST_PER_DC_AKTUAL
- MCGDATA.V_M_PROD3UK_NEW
- MCGDATA.V_M_PROD3UK_NEW_2
- MCGDATA.V_PRODUCT_GROUP
- MCGDATA.V_PROP_HGJUAL_IDM_HEADER
- MCGDATA.V_SELLING_PRICE_MD
- MCGDATA.V_SELLING_PRICE_NAS

# Direct Write

- MCGDATA.DATA_MD
- MCGDATA.HANDSONTABLE_TEMP
- MCGDATA.M_LAST_COST_PER_DC_AKTUAL_TEMP
- MCGDATA.M_LAST_COST_PER_DC_MD_TEMP
- MCGDATA.M_LAST_COST_PER_DC_TEMP
- MCGDATA.PROP_GRUP_PRODUK_NAS_TEMP
- MCGDATA.PROP_GRUP_PRODUK_PER_MD_TEMP
- MCGDATA.PROP_HGJUAL_IDM_HEADER
- MCGDATA.PROP_HGJUAL_IDM_NASIONAL
- MCGDATA.PROP_HGJUAL_IDM_NASIONAL_TEMP
- MCGDATA.PROP_HGJUAL_IDM_PER_MD
- MCGDATA.PROP_HGJUAL_IDM_PER_MD_TEMP
- MCGDATA.TEMP_BULAN

# Calls

- MCGDATA.AMBIL_PPN
- MCGDATA.ATTACH_GLOBAL_USER_UPD
- MCGDATA.GENERATE_OTP_PROP_HGJUAL_NEW
- MCGDATA.GET_FLAG_BKL2
- MCGDATA.GET_MARKUP_MARGIN_LASTCOST_YLS
- MCGDATA.GET_NAMA_CAB_NKL
- MCGDATA.GET_NILAI_HARGA_JUAL
- MCGDATA.GET_NILAI_HARGA_JUAL_MD
- MCGDATA.GET_NILAI_PERUBAHAN
- MCGDATA.GET_NILAI_STD
- MCGDATA.LCOST_PER_DC_NAS1_YEL
- MCGDATA.LCOST_PER_DC_NAS2_YEL
- MCGDATA.LCOST_PER_DC_PER_MD1_YEL
- MCGDATA.LCOST_PER_DC_PER_MD2_YEL
- MCGDATA.PROP_UPD_HG_GRUP_NAS_YEL
- MCGDATA.PROP_UPD_HG_GRUP_PER_MD_TEST
- MCGDATA.SALIN_HGJUAL_IDM_YLS2
- MCGDATA.VALIDASI_TAMBAH_PROP_HGJUAL
- MCGDATA.VALIDASI_TAMBAH_PROP_HGJUAL2
- MCGDATA.VAL_SALIN_DATA
- MCGDATA.VAL_UPD_HG_GRUP_NAS_YEL
- MCGDATA.VAL_UPD_HG_GRUP_PER_MD_YEL

# CTE / Logical Relations

- NASIONAL
  - Reads: MCGDATA.HGJUAL_IDM_NASIONAL, MCGDATA.M_TIPE_HARGA_NEW

# Analysis Notes

- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "  INSERT INTO DATA_MD SELECT DISTINCT '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " DELETE  FROM DATA_MD "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " INSERT INTO PROP_HGJUAL_IDM_NASIONAL_TEMP (KD_PROP, KD_PLU, SAT_JUAL, KD_TIPE, TGL_BERLAKU_HGJUAL, HG_JUAL, MARGIN, LAST_MARGIN_HO,  "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " INSERT INTO PROP_HGJUAL_IDM_PER_MD_TEMP (KD_PROP, KD_PLU, KD_MD, SAT_JUAL, KD_TIPE, TGL_BERLAKU_HGJUAL, HG_JUAL, MARGIN, LAST_MARGIN_HO,  "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " INSERT INTO temp_bulan (menu, BULAN , nomor) "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT  TO_CHAR(SYSDATE, 'DDMMYY') || CASE LENGTHB(NVL(MAX(NOMOR), 0) + 1 ) WHEN 1 THEN '00000' || TO_CHAR(NVL(MAX(NOMOR), 0) + 1) WHEN 2 THEN '0000' || TO_CHAR(NVL(MAX(NOMOR), 0) + 1)  WHEN 3 THEN '000' || TO_CHAR(NVL(MAX(NOMOR), 0) + 1 ) "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT  c.kd_tipe, b.deskripsi,  TO_CHAR(c.sat_jual) sat_jual,  TO_CHAR(c.hg_jual) hg_jual, TO_CHAR(c.tgl_berlaku_hgjual, 'DD-MON-YYYY') tgl_berlaku, TO_CHAR(ROUND( c.margin,2)) margin, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT DISTINCT A.* FROM ( "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT DISTINCT A.* FROM M_MD_HGJUAL A, M_MDHGJUAL_USER_CBG B "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT TO_CHAR(KD_PLU)KD_PLU, TO_CHAR(SAT_JUAL)SAT_JUAL, TO_CHAR(KD_TIPE)KD_TIPE, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT TO_CHAR(KD_PROP) kd_prop, TO_CHAR(SAT_JUAL)SAT_JUAL, TO_CHAR(KD_TIPE) KD_TIPE, TO_CHAR(TGL_BERLAKU_HGJUAL, 'DD-MON-YYYY')TGL_BERLAKU_HGJUAL, TO_CHAR(HG_JUAL) HG_JUAL, TO_CHAR(MARGIN) MARGIN, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT distinct  A.ftkode, A.ftnama, A.ftkwil, TO_CHAR(ROUND(b.fmhgjl,2)) fmhgjl, TO_CHAR(ROUND( (b.fmhgjl/b.fmqtys),2)) AS harga_satuan, TO_CHAR(b.fmtgck, 'DD-MON-YYYY'), b.FMCHKR "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT distinct  c.kd_tipe, b.deskripsi,  TO_CHAR(c.sat_jual) sat_jual,  TO_CHAR(c.hg_jual) hg_jual, TO_CHAR(c.tgl_berlaku_hgjual, 'DD-MON-YYYY') tgl_berlaku, TO_CHAR(ROUND( c.margin,2)) margin, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT distinct A.ftkode, A.ftnama, A.ftkwil, TO_CHAR(ROUND(b.fmhgjl,2)) fmhgjl, TO_CHAR(ROUND( (b.fmhgjl/b.fmqtys),2)) AS harga_satuan, TO_CHAR(b.fmtgck, 'DD-MON-YYYY'), b.FMCHKR "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " UPDATE temp_bulan SET nomor = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from  PROP_GRUP_PRODUK_PER_MD_TEMP  where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from PROP_GRUP_PRODUK_NAS_TEMP where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from PROP_GRUP_PRODUK_PER_MD_TEMP where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from PROP_HGJUAL_IDM_NASIONAL_TEMP where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from PROP_HGJUAL_IDM_PER_MD_TEMP where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " delete from prop_grup_produk_per_md_temp where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " select DISTINCT A.* from ( SELECT  c.kd_tipe, b.deskripsi,  TO_CHAR(c.sat_jual) sat_jual,  TO_CHAR(c.hg_jual) hg_jual, TO_CHAR(c.tgl_berlaku_hgjual, 'DD-MON-YYYY') tgl_berlaku, TO_CHAR(ROUND( c.margin,2)) margin, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " select distinct * from M_LAST_COST_PER_DC_MD_TEMP where seq = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " select distinct * from M_LAST_COST_PER_DC_TEMP where seq = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " select get_nilai_harga_jual('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " select get_nilai_harga_jual_md('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM M_LAST_COST_PER_DC_AKTUAL_TEMP WHERE SEQ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM M_LAST_COST_PER_DC_MD_TEMP WHERE SEQ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM M_LAST_COST_PER_DC_TEMP WHERE SEQ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT   a.mail_a  FROM  T_MAIL_ATASAN a, T_MAIL_BAWAHAN b WHERE a.mail_a = b.mail_a AND b.user_log = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT * FROM V_PROP_HGJUAL_IDM_HEADER WHERE KD_PLU IN(SELECT FMKODE FROM V_M_PROD3UK_NEW WHERE FMKODE IN(SELECT KD_PLU FROM M_AKSES_PLU_HGJUAL WHERE USER_ID = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT * FROM V_SELLING_PRICE_MD WHERE kd_md = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT 1  FROM PROP_GRUP_PRODUK_NAS_TEMP WHERE user_update = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT 1  FROM PROP_GRUP_PRODUK_PER_MD_TEMP WHERE user_update = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT 1 FROM m_ketentuan_hgjual_divdepkat WHERE div||dept||katg = (SELECT fmkdiv||fmkdep||fmkatb FROM m_produk WHERE fmkode = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT Ambil_ppn('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT ID_JABATAN_SSO FROM M_LEVEL_HGJUAL_IDM WHERE \"LEVEL\" = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT PLU FROM PRD_HGBELI_FLUKTUATIF WHERE PLU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT margin FROM  produk_margin_khusus where kd_div = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT to_char(c.std_margin) FROM m_std_margin_tipejual a, m_std_margin_plu c WHERE a.kd_tipejual = c.kd_tipejual  AND c.kd_plu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "Select Get_Markup_Margin_Lastcost_YLS("
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from DATA_MD where seq = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from PROP_GRUP_PRODUK_NAS_TEMP  where sat_jual = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from PROP_GRUP_PRODUK_PER_MD_TEMP  where sat_jual = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from prop_hgjual_idm_header  where kd_prop = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from prop_hgjual_idm_nasional  where kd_prop = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from prop_hgjual_idm_nasional_temp  where KD_PLU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from prop_hgjual_idm_per_md  where kd_prop = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "delete from prop_hgjual_idm_per_md_temp  where KD_PLU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "insert into DATA_MD SELECT '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "insert into DATA_MD VALUES('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select * from V_SELLING_PRICE_NAS where kd_plu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select 1 from PROP_GRUP_PRODUK_NAS_TEMP where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select 1 from prop_grup_produk_per_md_temp where USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select distinct * from M_LAST_COST_PER_DC_AKTUAL_TEMP where SEQ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select distinct * from M_LAST_COST_PER_DC_AKT_MD_TEMP where SEQ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select get_nilai_STD('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select kd_dc from dc_ppn_kecuali where kd_dc = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: <empty>
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"
                                            SELECT 
                                                TO_CHAR(KD_PROP) KD_PROP, 
                                                TO_CHAR(LOKASI_APPROVAL) LOKASI_APP, 
                                                TO_CHAR(APPROVAL_ID) APPROVAL_ID,
                                                TO_CHAR(""LEVEL"") LEVEL_CHAR, 
                                                TO_CHAR(APPROVAL_STATUS) APPROVAL_STATUS, 
                                                TO_CHAR(KD_OTP) KD_OTP,
                                                TO_CHAR(TGL_EXPIRED_OTP, 'DD-MON-YYYY') TGL_EXPIRED_OTP, 
                                                USER_UPDATE, 
                                                TO_CHAR(TGL_UPDATE, 'DD-MON-YYYY') TGL_UPDATE,
                                                IP_ADDRESS, 
                                                BATAL
                                            FROM 
                                                APPROVAL_PROP_HGJUAL_IDM 
                                            WHERE 
                                                KD_PROP = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT 
                                             KD_PROP, KD_PLU, KD_MD, 
                                                SAT_JUAL, KD_TIPE, HG_JUAL, 
                                                TGL_BERLAKU_HGJUAL, KD_DC, KD_SUPPLIER, 
                                                HG_BELI, TGL_BERLAKU_HGBELI, USER_UPDATE, 
                                                TO_CHAR(TGL_UPDATE, 'DD-MON-YYYY'), JAM_UPDATE, VALIDASI, DESKRIPSI
                                             FROM VAL_SALIN_HARGA_TEMP WHERE USER_UPDATE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT DISTINCT TO_CHAR(A.hg_jual) hg_jual
                                            FROM HGJUAL_IDM_NASIONAL A , M_TIPE_HARGA_NEW C , T_CABANG D 
                                            WHERE A.TGL_BERLAKU_HGJUAL = (SELECT MAX(B.TGL_BERLAKU_HGJUAL) FROM HGJUAL_IDM_NASIONAL B 
	  				                                               WHERE A.KD_PLU = B.KD_PLU 
					                                               AND A.KD_TIPE = B.KD_TIPE 
					                                               AND A.SAT_JUAL = B.SAT_JUAL 
					                                               AND TGL_BERLAKU_HGJUAL <= TRUNC(SYSDATE)) 
                                            AND A.kd_tipe = c.kd_tipe (+) 
                                            AND kd_DC =  D.FTKODE(+) 
                                            AND A.SAT_JUAL = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT DISTINCT TO_CHAR(A.kd_prop) kd_prop,  TO_CHAR(A.kd_plu) KD_PLU, TO_CHAR(A.kd_tipe) kd_tipe,TO_CHAR(A.sat_jual) sat_jual,
                                            TO_CHAR(A.hg_jual) hg_jual,TO_CHAR(A.TGL_BERLAKU_HGJUAL, 'DD-MON-YYYY') TGL_BERLAKU_HGJUAL, TO_CHAR(a.margin) MARGIN,
                                            TO_CHAR(a.last_margin_ho) last_margin_ho, TO_CHAR(A.kd_supplier) kd_supplier,TO_CHAR(a.hg_beli) hg_beli, 
                                            TO_CHAR(Get_Nilai_Perubahan(TO_CHAR(A.kd_plu),a.last_margin_ho,a.margin))  AS perubahan_margin , c.deskripsi , 
                                            CASE WHEN A.KD_DC IS NOT NULL THEN A.KD_DC||' - '||Get_Nama_Cab_Nkl(A.KD_DC) ELSE '' END AS KD_DC, TO_CHAR(tgl_berlaku_hgbeli, 'DD-MON-YYYY') tgl_berlaku_hgbeli , 
                                            A.user_update, TO_CHAR(A.tgl_update, 'DD-MON-YYYY') TGL_UPDATE, C.URUTAN_TAMPIL
                                            FROM HGJUAL_IDM_NASIONAL A , M_TIPE_HARGA_NEW C , T_CABANG D 
                                            WHERE A.TGL_BERLAKU_HGJUAL = (SELECT MAX(B.TGL_BERLAKU_HGJUAL) FROM HGJUAL_IDM_NASIONAL B 
	  				                                               WHERE A.KD_PLU = B.KD_PLU 
					                                               AND A.KD_TIPE = B.KD_TIPE 
					                                               AND A.SAT_JUAL = B.SAT_JUAL 
					                                               AND TGL_BERLAKU_HGJUAL <= TRUNC(SYSDATE)) 
                                            AND A.kd_tipe = c.kd_tipe (+) 
                                            AND kd_DC =  D.FTKODE(+) 
                                            AND SAT_JUAL = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT DISTINCT b.status FROM h_rafaksi a, approval_rafaksi b, d_rafaksi_hgjual c, d_rafaksi_partisipan d 
                                         WHERE a.ID=b.ID 
                                         AND b.ID = c.ID 
                                         AND c.ID = d.ID 
                                         AND c.kd_plu = d.kd_plu
                                         AND a.tgl_awal > TRUNC(SYSDATE)
                                         AND nvl(a.flag_min_qty_beli, 'N') <> 'Y'
                                         AND c.kd_plu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT c.kd_tipe, b.deskripsi, TO_CHAR(c.hg_jual) hg_jual FROM prop_hgjual_idm_nasional_temp c, m_tipe_harga_new b WHERE b.kd_tipe = c.kd_tipe and c.user_update = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @" SELECT c.kd_tipe, b.deskripsi, TO_CHAR(c.hg_jual) hg_jual FROM prop_hgjual_idm_per_md_temp c, m_tipe_harga_new b WHERE b.kd_tipe = c.kd_tipe and c.user_update = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT A.* FROM (
	                                            SELECT * FROM V_M_PROD3UK_NEW_2 B  
	                                            WHERE EXISTS (SELECT 1 
		  		                                              FROM M_AKSES_PLU_HGJUAL A 
				                                              WHERE user_id = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT A.KD_DC, B.FTNAMA FROM M_MD_HGJUAL_DC A, T_CABANG B
                                             WHERE A.kd_dc = B.FTKODE
                                             AND A.kd_md = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT A.KD_DC, B.FTNAMA,  A.kd_md FROM M_MD_HGJUAL_DC A, T_CABANG B, DATA_MD C
                                             WHERE A.kd_dc = B.FTKODE and A.kd_md = C.kd_md and c.seq = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT DISTINCT A.FMKODE, A.FMKDIV, A.FMKDEP, A.FMKATB, A.FMKODE_CHAR, A.DESKRIPSI
                                            FROM V_M_PROD3UK_NEW A, M_PRODUK B
                                            WHERE A.FMKODE = B.FMKODE AND A.FMKODE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT count(1) FROM HGJUAL_IDM_NASIONAL WHERE KD_PLU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"SELECT to_char(b.std_margin) FROM m_std_margin_tipejual a, m_std_margin_divdepkat b, M_PRODUK D 
                                                   WHERE a.kd_tipejual = b.kd_tipejual 
                                                   AND b.kd_div = D.fmkdiv 
                                                   AND b.kd_dept = D.fmkdep 
                                                   AND b.kd_katg = D.fmkatb 
                                                   AND D.fmkode = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"select * from M_MD_HGJUAL b
                                            where kd_md in(
                                                     select distinct kd_md 
                                                     from PROP_HGJUAL_IDM_PER_MD_TEMP 
                                                     where kd_plu = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: procName
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query_md
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"SELECT FMTSJL, FMFDIS, FMKCAB, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER, FMKTKO || '-' || f.tok_name
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"SELECT FMTSJL, FMFDIS, FMKWIL, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"SELECT FMTSJL, FMFDIS, FMKWIL, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER, FMKCAB
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: 
                                            SELECT 
                                                TO_CHAR(KD_PROP) KD_PROP, 
                                                TO_CHAR(LOKASI_APPROVAL) LOKASI_APP, 
                                                TO_CHAR(APPROVAL_ID) APPROVAL_ID,
                                                TO_CHAR("LEVEL") LEVEL_CHAR, 
                                                TO_CHAR(APPROVAL_STATUS) APPROVAL_STATUS, 
                                                TO_CHAR(KD_OTP) KD_OTP,
                                                TO_CHAR(TGL_EXPIRED_OTP, 'DD-MON-YYYY') TGL_EXPIRED_OTP, 
                                                USER_UPDATE, 
                                                TO_CHAR(TGL_UPDATE, 'DD-MON-YYYY') TGL_UPDATE,
                                                IP_ADDRESS, 
                                                BATAL
                                            FROM 
                                                APPROVAL_PROP_HGJUAL_IDM 
                                            WHERE 
                                                KD_PROP = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:   INSERT INTO DATA_MD SELECT DISTINCT '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT 
                                             KD_PROP, KD_PLU, KD_MD, 
                                                SAT_JUAL, KD_TIPE, HG_JUAL, 
                                                TGL_BERLAKU_HGJUAL, KD_DC, KD_SUPPLIER, 
                                                HG_BELI, TGL_BERLAKU_HGBELI, USER_UPDATE, 
                                                TO_CHAR(TGL_UPDATE, 'DD-MON-YYYY'), JAM_UPDATE, VALIDASI, DESKRIPSI
                                             FROM VAL_SALIN_HARGA_TEMP WHERE USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT DISTINCT TO_CHAR(A.hg_jual) hg_jual
                                            FROM HGJUAL_IDM_NASIONAL A , M_TIPE_HARGA_NEW C , T_CABANG D 
                                            WHERE A.TGL_BERLAKU_HGJUAL = (SELECT MAX(B.TGL_BERLAKU_HGJUAL) FROM HGJUAL_IDM_NASIONAL B 
	  				                                               WHERE A.KD_PLU = B.KD_PLU 
					                                               AND A.KD_TIPE = B.KD_TIPE 
					                                               AND A.SAT_JUAL = B.SAT_JUAL 
					                                               AND TGL_BERLAKU_HGJUAL <= TRUNC(SYSDATE)) 
                                            AND A.kd_tipe = c.kd_tipe (+) 
                                            AND kd_DC =  D.FTKODE(+) 
                                            AND A.SAT_JUAL = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT DISTINCT TO_CHAR(A.kd_prop) kd_prop,  TO_CHAR(A.kd_plu) KD_PLU, TO_CHAR(A.kd_tipe) kd_tipe,TO_CHAR(A.sat_jual) sat_jual,
                                            TO_CHAR(A.hg_jual) hg_jual,TO_CHAR(A.TGL_BERLAKU_HGJUAL, 'DD-MON-YYYY') TGL_BERLAKU_HGJUAL, TO_CHAR(a.margin) MARGIN,
                                            TO_CHAR(a.last_margin_ho) last_margin_ho, TO_CHAR(A.kd_supplier) kd_supplier,TO_CHAR(a.hg_beli) hg_beli, 
                                            TO_CHAR(Get_Nilai_Perubahan(TO_CHAR(A.kd_plu),a.last_margin_ho,a.margin))  AS perubahan_margin , c.deskripsi , 
                                            CASE WHEN A.KD_DC IS NOT NULL THEN A.KD_DC||' - '||Get_Nama_Cab_Nkl(A.KD_DC) ELSE '' END AS KD_DC, TO_CHAR(tgl_berlaku_hgbeli, 'DD-MON-YYYY') tgl_berlaku_hgbeli , 
                                            A.user_update, TO_CHAR(A.tgl_update, 'DD-MON-YYYY') TGL_UPDATE, C.URUTAN_TAMPIL
                                            FROM HGJUAL_IDM_NASIONAL A , M_TIPE_HARGA_NEW C , T_CABANG D 
                                            WHERE A.TGL_BERLAKU_HGJUAL = (SELECT MAX(B.TGL_BERLAKU_HGJUAL) FROM HGJUAL_IDM_NASIONAL B 
	  				                                               WHERE A.KD_PLU = B.KD_PLU 
					                                               AND A.KD_TIPE = B.KD_TIPE 
					                                               AND A.SAT_JUAL = B.SAT_JUAL 
					                                               AND TGL_BERLAKU_HGJUAL <= TRUNC(SYSDATE)) 
                                            AND A.kd_tipe = c.kd_tipe (+) 
                                            AND kd_DC =  D.FTKODE(+) 
                                            AND SAT_JUAL = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT DISTINCT b.status FROM h_rafaksi a, approval_rafaksi b, d_rafaksi_hgjual c, d_rafaksi_partisipan d 
                                         WHERE a.ID=b.ID 
                                         AND b.ID = c.ID 
                                         AND c.ID = d.ID 
                                         AND c.kd_plu = d.kd_plu
                                         AND a.tgl_awal > TRUNC(SYSDATE)
                                         AND nvl(a.flag_min_qty_beli, 'N') <> 'Y'
                                         AND c.kd_plu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT FMKODE FROM V_M_PROD3UK_NEW WHERE FMKDIV||FMKDEP||FMKATB IN(SELECT DIVDEPKAT FROM M_AKSES_PLU_HGJUAL WHERE USER_ID = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT KD_PROP,'
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT c.kd_tipe, b.deskripsi, TO_CHAR(c.hg_jual) hg_jual FROM prop_hgjual_idm_nasional_temp c, m_tipe_harga_new b WHERE b.kd_tipe = c.kd_tipe and c.user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT c.kd_tipe, b.deskripsi, TO_CHAR(c.hg_jual) hg_jual FROM prop_hgjual_idm_per_md_temp c, m_tipe_harga_new b WHERE b.kd_tipe = c.kd_tipe and c.user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from  PROP_GRUP_PRODUK_PER_MD_TEMP  where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from PROP_GRUP_PRODUK_NAS_TEMP where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from PROP_GRUP_PRODUK_PER_MD_TEMP where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from PROP_HGJUAL_IDM_NASIONAL_TEMP where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from PROP_HGJUAL_IDM_PER_MD_TEMP where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  delete from prop_grup_produk_per_md_temp where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  select distinct * from M_LAST_COST_PER_DC_MD_TEMP where seq = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  select distinct * from M_LAST_COST_PER_DC_TEMP where seq = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  select get_nilai_harga_jual('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  select get_nilai_harga_jual_md('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM M_LAST_COST_PER_DC_AKTUAL_TEMP WHERE SEQ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM M_LAST_COST_PER_DC_MD_TEMP WHERE SEQ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM M_LAST_COST_PER_DC_TEMP WHERE SEQ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT   a.mail_a  FROM  T_MAIL_ATASAN a, T_MAIL_BAWAHAN b WHERE a.mail_a = b.mail_a AND b.user_log = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT "KD_JAB", "NMJABATAN" FROM "MSJABATAN" WHERE "ID" = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT * FROM V_PROP_HGJUAL_IDM_HEADER WHERE KD_PLU IN(SELECT FMKODE FROM V_M_PROD3UK_NEW WHERE FMKODE IN(SELECT KD_PLU FROM M_AKSES_PLU_HGJUAL WHERE USER_ID = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT * FROM V_SELLING_PRICE_MD WHERE kd_md = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT 1  FROM PROP_GRUP_PRODUK_NAS_TEMP WHERE user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT 1  FROM PROP_GRUP_PRODUK_PER_MD_TEMP WHERE user_update = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT 1 FROM m_ketentuan_hgjual_divdepkat 
                             WHERE lokasi = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT 1 FROM m_ketentuan_hgjual_divdepkat WHERE div||dept||katg = (SELECT fmkdiv||fmkdep||fmkatb FROM m_produk WHERE fmkode = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT A.* FROM (
	                                            SELECT * FROM V_M_PROD3UK_NEW_2 B  
	                                            WHERE EXISTS (SELECT 1 
		  		                                              FROM M_AKSES_PLU_HGJUAL A 
				                                              WHERE user_id = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT A.KD_DC, B.FTNAMA FROM M_MD_HGJUAL_DC A, T_CABANG B
                                             WHERE A.kd_dc = B.FTKODE
                                             AND A.kd_md = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT A.KD_DC, B.FTNAMA,  A.kd_md FROM M_MD_HGJUAL_DC A, T_CABANG B, DATA_MD C
                                             WHERE A.kd_dc = B.FTKODE and A.kd_md = C.kd_md and c.seq = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT A.kd_md,A.deskripsi, NVL(b.kd_md, '1') status  FROM M_MD_HGJUAL A, DATA_MD B  
                              --WHERE A.kd_md <> '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT Ambil_ppn('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT
						    CASE 
						        WHEN q1.user_id IN (SELECT user_id FROM m_mdhgjual_user_cbg 
						 WHERE jabatan_id IN(SELECT id_jabatan_sso FROM m_level_hgjual_idm WHERE lokasi = '1')
						 AND KD_MD = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT A.FMKODE, A.FMKDIV, A.FMKDEP, A.FMKATB, A.FMKODE_CHAR, A.DESKRIPSI
                                            FROM V_M_PROD3UK_NEW A, M_PRODUK B
                                            WHERE A.FMKODE = B.FMKODE AND A.FMKODE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT A.kd_md,A.deskripsi, NVL(b.kd_md, '1') status  FROM M_MD_HGJUAL A, DATA_MD B, M_ZONA_HGJUAL_HDR c, M_ZONA_HGJUAL_DTL D   
                                WHERE A.kd_md <> '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT DISTINCT b.kd_prop, a.fdkplu, a.deskripsi 
		                  FROM v_product_group a, 
		  	                   prop_grup_produk_per_md_temp b, 
			                   prop_grup_produk_nas_temp c 
		                  WHERE fdksbu = '3' 
                                AND fdkode IN (SELECT aa.fmkode  FROM M_PRODUCT_GROUP aa, D_PRODUCT_GROUP bb
				                WHERE aa.fmkode = bb.FDKODE 
				                AND aa.fmksbu = '3' 
				                AND aa.fmkode = bb.FDKODE 
				                AND aa.fmksbu = bb.fdksbu
				                AND bb.fdkode IN (SELECT bbb.fdkode FROM D_PRODUCT_GROUP bbb WHERE bbb.fdkplu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FMTSJL, FMFDIS, FMKCAB, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER, FMKTKO || '-' || f.tok_name 
                                                          FROM m_promosi e INNER JOIN HO_TOKO_T@MARKETING f ON e.fmktko=f.tok_code 
                                                          WHERE e.fmktko <> 'x' AND e.fmksbu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FMTSJL, FMFDIS, FMKWIL, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER
                                                          FROM m_promosi e 
                                                          WHERE e.fmkcab = 'x' AND e.fmktko = 'x' AND  e.fmksbu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FMTSJL, FMFDIS, FMKWIL, FMMKUP, FMHJLK, FMDIPK, FMDIRK, FMTGMK, FMTGAK, FMJAMK, FMJAAK, FMTGUP, FMUSER, FMKCAB
                                                          FROM m_promosi e 
                                                          WHERE e.fmkcab <> 'x' AND e.fmktko = 'x'  AND e.fmksbu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT ID_JABATAN_SSO FROM M_LEVEL_HGJUAL_IDM WHERE "LEVEL" = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT LISTAGG(a.nm_zona, ', ') WITHIN GROUP (ORDER BY a.nm_zona) AS nm_zona
                                            FROM m_zona_hgjual_hdr a
                                            JOIN m_zona_hgjual_dtl b 
                                                ON a.username = b.username 
                                                AND a.kd_zona = b.kd_zona
                                            WHERE b.kd_md = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT LISTAGG(a.nm_zona, ', ') WITHIN GROUP (ORDER BY a.nm_zona) AS nm_zona
                                            FROM m_zona_hgjual_hdr a
                                            JOIN m_zona_hgjual_dtl b 
                                              ON a.username = b.username 
                                             AND a.kd_zona = b.kd_zona
                                            WHERE b.kd_md = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT LISTAGG(a.nm_zona, ', ') WITHIN GROUP (ORDER BY a.nm_zona) AS nm_zona
                                        FROM m_zona_hgjual_hdr a
                                        JOIN m_zona_hgjual_dtl b 
                                          ON a.username = b.username 
                                         AND a.kd_zona = b.kd_zona
                                        WHERE b.kd_md = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT PLU FROM PRD_HGBELI_FLUKTUATIF WHERE PLU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT count(1) FROM HGJUAL_IDM_NASIONAL WHERE KD_PLU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT level_approval_cabang, level_approval_ho FROM m_ketentuan_hgjual_divdepkat 
                        WHERE lokasi =  '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT margin FROM  produk_margin_khusus where kd_div = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT to_char(b.std_margin) FROM m_std_margin_tipejual a, m_std_margin_divdepkat b, M_PRODUK D 
                                                   WHERE a.kd_tipejual = b.kd_tipejual 
                                                   AND b.kd_div = D.fmkdiv 
                                                   AND b.kd_dept = D.fmkdep 
                                                   AND b.kd_katg = D.fmkatb 
                                                   AND D.fmkode = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT to_char(c.std_margin) FROM m_std_margin_tipejual a, m_std_margin_plu c WHERE a.kd_tipejual = c.kd_tipejual  AND c.kd_plu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT xy.kd_md,xy.deskripsi,  NVL(b.kd_md, '1') status FROM M_MD_HGJUAL xy, DATA_MD B  
                                --WHERE xy.kd_md =  Get_Kd_Md('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: Select Get_Markup_Margin_Lastcost_YLS(
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: WITH NASIONAL AS (
                                    SELECT 
                                        'National' AS NOTES,
                                        A.KD_PLU,
                                        NULL AS KD_MD,
                                        A.KD_TIPE,
                                        A.SAT_JUAL,
                                        A.HG_JUAL,
                                        A.MARGIN,
                                        A.LAST_MARGIN_HO,
                                        A.KD_SUPPLIER,
                                        A.HG_BELI,
                                        Get_Nilai_Perubahan(TO_CHAR(A.KD_PLU), A.LAST_MARGIN_HO, A.MARGIN) AS PERUBAHAN_MARGIN,
                                        C.DESKRIPSI,
                                        NULL AS KD_DC,
                                        A.TGL_BERLAKU_HGBELI,
                                        A.KD_PROP,
                                        A.USER_UPDATE,
                                        A.TGL_UPDATE,
                                        A.TGL_BERLAKU_HGJUAL,
                                        C.URUTAN_TAMPIL
                                    FROM HGJUAL_IDM_NASIONAL A
                                         JOIN M_TIPE_HARGA_NEW C ON A.KD_TIPE = C.KD_TIPE
                                    WHERE A.KD_PLU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from DATA_MD where seq = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from PROP_GRUP_PRODUK_NAS_TEMP  where sat_jual = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from PROP_GRUP_PRODUK_PER_MD_TEMP  where sat_jual = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from prop_hgjual_idm_header  where kd_prop = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from prop_hgjual_idm_nasional  where kd_prop = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from prop_hgjual_idm_nasional_temp  where KD_PLU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from prop_hgjual_idm_per_md  where kd_prop = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: delete from prop_hgjual_idm_per_md_temp  where KD_PLU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: insert into DATA_MD 
                                          SELECT '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: insert into DATA_MD SELECT '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: insert into DATA_MD VALUES('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select * from M_MD_HGJUAL b
                                            where kd_md in(
                                                     select distinct kd_md 
                                                     from PROP_HGJUAL_IDM_PER_MD_TEMP 
                                                     where kd_plu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select * from V_SELLING_PRICE_NAS where kd_plu = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select 1 from PROP_GRUP_PRODUK_NAS_TEMP where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select 1 from prop_grup_produk_per_md_temp where USER_UPDATE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select distinct * from M_LAST_COST_PER_DC_AKTUAL_TEMP where SEQ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select distinct * from M_LAST_COST_PER_DC_AKT_MD_TEMP where SEQ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select get_nilai_STD('
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select kd_dc from dc_ppn_kecuali where kd_dc = '
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: APPROVAL_PROP_HGJUAL_IDM.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: DC_BY_WILAYAH.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PRODUCT_GROUP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: HANDSONTABLE_VALIDATION.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: HANDSONTABLE_VALIDATION.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: HGJUAL_IDM_PER_MD.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: HGJUAL_IDM_PER_MD_V.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: MSUSER.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_AKSES_PLU_HGJUAL.Select
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_AKSES_PLU_HGJUAL.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_MDHGJUAL_USER_CBG.Contains
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_MDHGJUAL_USER_CBG.Select
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_MDHGJUAL_USER_CBG.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_PRODUCT_GROUP.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_SELL_UNIT.Any
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_SELL_UNIT.Distinct
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_SELL_UNIT.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_SELL_UNIT.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_TIPE_HARGA_NEW.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_NASIONAL_TEMP.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_PER_MD.Contains
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_PER_MD.Count
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_PER_MD.Select
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_PER_MD.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: PROP_HGJUAL_IDM_PER_MD_TEMP.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: Produk_Phi.Count
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: Produk_Phi.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: TBL_M_LAST_COST.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_PLU_NONAKTIF.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW_2.Count
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW_2.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW_2.OrderByDescending
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW_2.Skip
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_M_PROD3UK_NEW_2.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PRODUCT_GROUP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PROP_HGJUAL_IDM_HEADER.Count
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PROP_HGJUAL_IDM_HEADER.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PROP_HGJUAL_IDM_HEADER.OrderByDescending
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PROP_HGJUAL_IDM_HEADER.Skip
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_PROP_HGJUAL_IDM_HEADER.Where

