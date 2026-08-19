---
id: "SupplierProposal"
name: "SupplierProposal"
group: IMMD
url: "/Transaction/SupplierProposal"
---

# Direct Read

- MCGDATA.BANK_SUPPLIER_PROP
- MCGDATA.DAFTAR_HARI
- MCGDATA.D_PROPOSAL_CONTACT_P
- MCGDATA.D_PROPOSAL_GUDANG
- MCGDATA.D_PROPOSAL_JKIRIM
- MCGDATA.D_PROPOSAL_NPWP
- MCGDATA.D_PROPOSAL_ORD_NON_MNG
- MCGDATA.D_PROPOSAL_PERWAKILAN_LK
- MCGDATA.D_SUPPLIER_NOFAX_PROP
- MCGDATA.D_SUPP_PROPOSAL_REGION
- MCGDATA.D_SUPP_PROPOSAL_TOP
- MCGDATA.D_SUPP_SENTRALISASI_PROPOSAL
- MCGDATA.D_SUPP_SENTRALISASI_PROPOSAL_V
- MCGDATA.LAPORAN_BANK_SUPPLIER_PROP
- MCGDATA.MS_BANK
- MCGDATA.M_BENTUK_USAHA
- MCGDATA.M_FLAG_SUPP
- MCGDATA.SELECT_HARI
- MCGDATA.SUP_BANK_TGL_BERLAKU
- MCGDATA.T_CABANG
- MCGDATA.T_FLAG_SUPP_PROP
- MCGDATA.T_GROUP_SUPPLIER
- MCGDATA.T_JNS_SUPPLIER
- MCGDATA.T_LEAD_TIME
- MCGDATA.T_NEGARA
- MCGDATA.T_OPTION_PAYMENT
- MCGDATA.T_PENANGANAN_BRG
- MCGDATA.T_SUPPLIER
- MCGDATA.T_SUPPLIER_PROPOSAL
- MCGDATA.T_SUPPLIER_PROPOSAL_VIEW
- MCGDATA.T_UNIT
- MCGDATA.T_WILAYAH
- MCGDATA.V3_M_PRODUK
- MCGDATA.V_SUPPLIER_PROPOSAL

# Direct Write

- MCGDATA.D_PROPOSAL_GUDANG
- MCGDATA.D_PROPOSAL_JKIRIM
- MCGDATA.D_PROPOSAL_NPWP
- MCGDATA.D_PROPOSAL_ORD_NON_MNG
- MCGDATA.D_SUPPLIER_NOFAX_PROP
- MCGDATA.D_SUPP_SENTRALISASI_PROPOSAL
- MCGDATA.SELECT_HARI
- MCGDATA.T_SUPPLIER_PROPOSAL

# Calls

- MCGDATA.CARI_DESK_PRODUK
- MCGDATA.DELETE_SELECT_HARI
- MCGDATA.GET_HARI
- MCGDATA.LAP_BANK_SUPPLIER_PROP1
- MCGDATA.LOAD_SELECT_HARI1
- MCGDATA.SUPPLIER_APPROVED_PROCESS
- MCGDATA.SUPPLIER_PROPOSAL_NUMBER_GET1

# Analysis Notes

- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM D_PROPOSAL_GUDANG WHERE FDKODE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM D_PROPOSAL_JKIRIM WHERE FDKSBU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM D_PROPOSAL_NPWP WHERE FDKODE = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT JUMLAH_HARI FROM SUP_BANK_TGL_BERLAKU WHERE SBU = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "UPDATE D_PROPOSAL_JKIRIM SET FDHRKJ = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "UPDATE T_SUPPLIER_PROPOSAL SET FTSFRP = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select Cari_Desk_Produk("
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: <empty>
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: @"
                                UPDATE T_SUPPLIER_PROPOSAL SET 
                                    FTNAMA = '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: sql
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_PROPOSAL_ORD_NON_MNG WHERE FDKODE = '{0}' ", kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_PROPOSAL_ORD_NON_MNG WHERE FDKODE = '{0}' AND FDKPLU = '{1}'", kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_SUPPLIER_NOFAX_PROP WHERE KD_PROPOSAL =  '{0}' ", kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_SUPPLIER_NOFAX_PROP WHERE KD_PROPOSAL = '{0}' AND NO_FAX = '{1}'", kode, fax)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_SUPP_SENTRALISASI_PROPOSAL WHERE FDKODE =  '{0}' ", kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("DELETE FROM D_SUPP_SENTRALISASI_PROPOSAL WHERE FDKODE =  '{0}' && FDKCAB = '{1}' ", kode, cab)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("INSERT INTO D_SUPPLIER_NOFAX_PROP VALUES('{0}', '{1}', '{2}', '{3}', '{4}') ", kode, fax, tglupd, userupd, ipupd)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("INSERT INTO D_SUPP_SENTRALISASI_PROPOSAL VALUES('{0}', '{1}', '{2}', '{3}')", kode, cab, ttf, rcid)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT FDKODE, FDKPLU, FDFKRM, FDJWPB, FDTGOR, FDTGKR FROM D_PROPOSAL_ORD_NON_MNG WHERE FDKODE = '{0}' AND FDKPLU = '{1}'", kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT FDKODE, FDKPLU, FDFKRM, FDJWPB, FDTGOR, FDTGKR, FDTGUP, FDUSER FROM D_PROPOSAL_ORD_NON_MNG WHERE FDKODE = '{0}' ", kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT FLAG_SUPPLIER FROM M_FLAG_SUPP")
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT KD_PROPOSAL, NO_FAX FROM D_SUPPLIER_NOFAX_PROP WHERE KD_PROPOSAL = '{0}' AND NO_FAX = '{1}'", kode, fax)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT KD_PROPOSAL, NO_FAX, TGL_UPDATE, KD_USER, IP_ADDRESS FROM D_SUPPLIER_NOFAX_PROP WHERE KD_PROPOSAL = '{0}' ", kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("SELECT MAX(tgl_berlaku) FROM BANK_SUPPLIER_PROP where tgl_berlaku <= '{0}' and unit = '{1}' and kode_prop = '{2}'", hariini, unit, kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_PROPOSAL_ORD_NON_MNG SET FDFKRM = '{0}', FDJWPB = '{1}', FDTGKR = '{2}', FDUSER = '{3}', FDTGUP = '{4}' WHERE FDKODE = '{5}' AND FDKPLU = '{6}' ", delivery, leadtime, kirim, userupd, tglupd, kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_PROPOSAL_ORD_NON_MNG SET FDFKRM = '{0}', FDJWPB = '{1}', FDTGOR = '{2}', FDTGKR = '{3}', FDUSER = '{4}', FDTGUP = '{5}' WHERE FDKODE = '{6}' AND FDKPLU = '{7}' ", delivery, leadtime, order, kirim, userupd, tglupd, kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_PROPOSAL_ORD_NON_MNG SET FDFKRM = '{0}', FDJWPB = '{1}', FDTGOR = '{2}', FDUSER = '{3}', FDTGUP = '{4}' WHERE FDKODE = '{5}' AND FDKPLU = '{6}' ", delivery, leadtime, order, userupd, tglupd, kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_PROPOSAL_ORD_NON_MNG SET FDFKRM = '{0}', FDJWPB = '{1}', FDUSER = '{2}', FDTGUP = '{3}' WHERE FDKODE = '{4}' AND FDKPLU = '{5}' ", delivery, leadtime, userupd, tglupd, kode, plu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_SUPPLIER_NOFAX_PROP SET NO_FAX = '{0}', TGL_UPDATE = '{1}', KD_USER = '{2}', IP_ADDRESS = '{3}' WHERE KD_PROPOSAL = '{4}' ", fax, tglupd, userupd, ipupd, kode)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_SUPPLIER_NOFAX_PROP SET NO_FAX = '{0}', TGL_UPDATE = '{1}', KD_USER = '{2}', IP_ADDRESS = '{3}' WHERE KD_PROPOSAL = '{4}' AND NO_FAX = '{5}' ", fax, tglupd, userupd, ipupd, kode, oldfax)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_SUPP_SENTRALISASI_PROPOSAL SET FDTGTF = '', FDRCID = '{0}' WHERE FDKODE = '{1}' AND FDKCAB = '{2}' ", rcid, kode, cab)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_SUPP_SENTRALISASI_PROPOSAL SET FDTGTF = '{0}', FDRCID = '{1}' WHERE FDKODE = '{2}' AND FDKCAB = '{3}' ", ttf, rcid, kode, cab)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE D_SUPP_SENTRALISASI_PROPOSAL SET FDTGTF = TO_DATE('{0}','DD/MM/YYYY'), FDRCID = '{1}' WHERE FDKODE = '{2}' AND FDKCAB = '{3}' ", ttf, rcid, kode, cab)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE SELECT_HARI SET SELECT_ID = 'N' WHERE IP_ADDRESS = '{0}' AND DATE_ACCESS = TO_DATE('{1}', 'DD/MM/YYYY')  AND DIGUNAKAN_UNTUK = '{2}'", ipAddress, date.ToString("dd/MM/yyyy"), use)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("UPDATE SELECT_HARI SET SELECT_ID = 'Y' WHERE IP_ADDRESS = '{0}' AND DATE_ACCESS = TO_DATE('{1}', 'DD/MM/YYYY')  AND DIGUNAKAN_UNTUK = '{2}'", ipAddress, date.ToString("dd/MM/yyyy"), use)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("insert into D_PROPOSAL_ORD_NON_MNG VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}') ", kode, plu, delivery, leadtime, order, kirim, tglupd, userupd)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("insert into D_PROPOSAL_ORD_NON_MNG(FDKODE, FDKPLU, FDFKRM, FDJWPB, FDTGKR, FTTGUP, FTUSER) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}') ", kode, plu, delivery, leadtime, kirim, tglupd, userupd)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("insert into D_PROPOSAL_ORD_NON_MNG(FDKODE, FDKPLU, FDFKRM, FDJWPB, FDTGOR, FTTGUP, FTUSER) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}') ", kode, plu, delivery, leadtime, order, tglupd, userupd)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("insert into D_PROPOSAL_ORD_NON_MNG(FDKODE, FDKPLU, FDFKRM, FDJWPB, FTTGUP, FTUSER) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}') ", kode, plu, delivery, leadtime, tglupd, userupd)
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM D_PROPOSAL_GUDANG WHERE FDKODE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM D_PROPOSAL_JKIRIM WHERE FDKSBU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM D_PROPOSAL_NPWP WHERE FDKODE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FTKODE, KD_DC, FDTGTF, FLAG, FTKWIL, FDRCID
                                    FROM D_SUPP_SENTRALISASI_PROPOSAL_V 
                                    WHERE FTKODE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FTKWIL, FTSTAT, TO_CHAR(FTKSUP) FTKSUP, FTNAMA, FTKODE, TO_CHAR(FTTGAD,'DD-MON-YYYY') FTTGAD FROM V_SUPPLIER_PROPOSAL WHERE FTTGAD > '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT FTNAMA FROM T_SUPPLIER WHERE FTKODE = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT JUMLAH_HARI FROM SUP_BANK_TGL_BERLAKU WHERE SBU = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: UPDATE D_PROPOSAL_JKIRIM SET FDHRKJ = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: UPDATE T_SUPPLIER_PROPOSAL SET FTSFRP = '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select Cari_Desk_Produk(
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: BANK_SUPPLIER_PROP.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: BANK_SUPPLIER_PROP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: DAFTAR_HARI.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_CONTACT_P.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_CONTACT_P.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_GUDANG.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_JKIRIM.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_JKIRIM.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_NPWP.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_PERWAKILAN_LK.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_PROPOSAL_PERWAKILAN_LK.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_PROPOSAL_REGION.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_PROPOSAL_REGION.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_PROPOSAL_TOP.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_PROPOSAL_TOP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_SENTRALISASI_PROPOSAL.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_SENTRALISASI_PROPOSAL.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: D_SUPP_SENTRALISASI_PROPOSAL_V.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: LAPORAN_BANK_SUPPLIER_PROP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: MS_BANK.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: M_BENTUK_USAHA.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: SELECT_HARI.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: SELECT_HARI.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_FLAG_SUPP_PROP.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_FLAG_SUPP_PROP.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_GROUP_SUPPLIER.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_GROUP_SUPPLIER.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_JNS_SUPPLIER.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_LEAD_TIME.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_NEGARA.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_OPTION_PAYMENT.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_PENANGANAN_BRG.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_PENANGANAN_BRG.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_SUPPLIER_PROPOSAL.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_SUPPLIER_PROPOSAL_VIEW.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_UNIT.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_UNIT.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_WILAYAH.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_WILAYAH.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: V_SUPPLIER_PROPOSAL.FirstOrDefault

