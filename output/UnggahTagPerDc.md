---
id: "UnggahTagPerDc"
name: "UnggahTagPerDc"
group: IMMD
url: "/Transaction/UnggahTagPerDc"
---

# Direct Read

- MCGDATA.D_PRODUK_E
- MCGDATA.M_CURR_SUPP
- MCGDATA.M_HGBELI
- MCGDATA.M_PRODUK
- MCGDATA.TAG_PER_DC
- MCGDATA.T_CABANG
- MCGDATA.T_STATUS
- MCGDATA.UNGGAH_TAG_PER_DC_TEMP
- MCGDATA.V_M_PRODUK_OPU_CHAR

# Direct Write

- MCGDATA.UNGGAH_TAG_PER_DC_RAW_TEMP
- MCGDATA.UNGGAH_TAG_PER_DC_TEMP

# Calls

- MCGDATA.CARI_DESK_PRODUK
- MCGDATA.PLU_SEDANG_PROMOSI
- MCGDATA.TAG_DICONTINUESTRING
- MCGDATA.UNGGAH_TAG_PER_DC_NKL
- MCGDATA.UNGGAH_TAG_PER_DC_VAL

# Analysis Notes

- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT 1 FROM TAG_PER_DC WHERE PLU='"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: " SELECT NVL(fmkdsb, '')fmkdsb FROM m_hgbeli "
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "DELETE FROM UNGGAH_TAG_PER_DC_TEMP WHERE USER_RANDOM='"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "SELECT c.FMKDIV||'-'||c.FMKDEP||'-'||c.FMKATB||'-'||Cari_Desk_Produk(a.PLU)||'-'||d.FTNAMA||'-'||a.TAG FROM  TAG_PER_DC a,M_PRODUK c, T_CABANG d WHERE a.PLU = c.FMKODE AND a.KD_DC = d.FTKODE AND a.PLU="
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select Cari_Desk_Produk("
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select plu_sedang_promosi('3', '"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: "select tag_DicontinueString('"
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: <empty>
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: query
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format("select fmkdsb from m_hgbeli A where A.fmkode = '{0}' and exists (select 1 from m_curr_supp b where b.fmksbu = '{1}' and b.fmkode = '{0}' and b.fmksup = a.fmksup and b.fmjnsh = a.fmjnsh) and a.fmtgbu = (select max (c.fmtgbu) from m_hgbeli c where c.fmkode = a.fmkode and c.fmksup = a.fmksup and c.fmjnsh = a.fmjnsh and c.fmtgbu <= sysdate)", plu, opu)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"  DELETE FROM UNGGAH_TAG_PER_DC_RAW_TEMP WHERE USER_RANDOM = '{0}' ", user_random)
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"  INSERT INTO UNGGAH_TAG_PER_DC_RAW_TEMP (
- [warning] DYNAMIC_PROCEDURE: OracleCommand procedure argument is dynamic: string.Format(@"  select fmksup, fmjnsh
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value:  SELECT 1 FROM TAG_PER_DC WHERE PLU='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: DELETE FROM UNGGAH_TAG_PER_DC_TEMP WHERE USER_RANDOM='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT PLU, KD_WILAYAH, KD_DC, TAG,KET FROM UNGGAH_TAG_PER_DC_TEMP WHERE USER_RANDOM='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT PLU, KD_WILAYAH, KD_DC, TAG,KET FROM UNGGAH_TAG_PER_DC_TEMP WHERE user_random='
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: SELECT c.FMKDIV||'-'||c.FMKDEP||'-'||c.FMKATB||'-'||Cari_Desk_Produk(a.PLU)||'-'||d.FTNAMA||'-'||a.TAG FROM  TAG_PER_DC a,M_PRODUK c, T_CABANG d WHERE a.PLU = c.FMKODE AND a.KD_DC = d.FTKODE AND a.PLU=
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select Cari_Desk_Produk(
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select flag_ecommerce from D_PRODUK_E where kd_plu =
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select plu_sedang_promosi('3', '
- [warning] DYNAMIC_SQL: SQL literal is concatenated with a dynamic value: select tag_DicontinueString('
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: TAG_PER_DC.FirstOrDefault
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.OrderBy
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_CABANG.Where
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_STATUS.Count
- [warning] UNRESOLVED_METHOD: Data-layer method cannot be resolved: T_STATUS.FirstOrDefault

