---
id: "MarginIGR"
name: "MarginIGR"
group: IMMD
url: "/Transaction/MarginIGR"
---

# Direct Read

- MCGDATA.IGR_MARGIN_DC
- MCGDATA.IGR_MARGIN_DEPT
- MCGDATA.IGR_MARGIN_KAT
- MCGDATA.IGR_MARGIN_PLU
- MCGDATA.M_PRODUK
- MCGDATA.T_CABANG
- MCGDATA.T_DEPT
- MCGDATA.T_KATEGORI

# Direct Write

- MCGDATA.IGR_MARGIN_DC
- MCGDATA.IGR_MARGIN_DEPT
- MCGDATA.IGR_MARGIN_KAT
- MCGDATA.IGR_MARGIN_PLU

# Calls

- MCGDATA.CARI_DESK_PRODUK

# Analysis Notes

- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT A.DC_IGR,(SELECT DISTINCT ftnama FROM T_CABANG WHERE ftkode = A.dc_igr) AS nama_igr, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT A.KD_KAT ,(SELECT DISTINCT FTNAMA FROM T_KATEGORI WHERE FTKODE = A.KD_KAT AND FTKDEP = A.KD_DEPT) AS FTNAMA , TO_CHAR(A.margin) MARGIN, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT DISTINCT TO_CHAR(A.KD_PLU) KD_PLU, Cari_Desk_Produk(A.KD_PLU) AS ftnama , TO_CHAR(A.margin) MARGIN, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT A.DC_IGR, (SELECT DISTINCT ftnama FROM T_CABANG WHERE ftkode = A.dc_igr) AS nama_igr, A.DC_IDM, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT DISTINCT A.KD_DEPT,(SELECT DISTINCT ftnama FROM T_DEPT WHERE ftkode = A.KD_DEPT) AS ftnama , to_char(A.margin) MARGIN, "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT to_char(A.FMKODE) FMKODE, A.FMMERK || ' ' || A.FMNAMA || ' ' || A.FMFLAV || ' ' || A.FMKMSN || ' ' || A.FMSIZE DESK FROM M_PRODUK A, T_CABANG C "
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: IGR_MARGIN_DC.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: IGR_MARGIN_DEPT.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: IGR_MARGIN_KAT.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: IGR_MARGIN_PLU.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_DEPT.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_KATEGORI.OrderBy

